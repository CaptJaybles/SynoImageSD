from flask import Flask, request
import requests
import threading
import queue
import random
import os
import json
import gc
import torch
from synology import OutgoingWebhook
from settings import *
from diffusers import AutoPipelineForText2Image
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from huggingface_hub import login

app = Flask(__name__)
login(token=HUGGINGFACE_TOKEN)
task_queue = queue.Queue()
processing_semaphore = threading.Semaphore(value=1)

#NSFW setting
if NSFW_ON is True:
   # NSFW is now On
    pipe = AutoPipelineForText2Image.from_pretrained(
        IMAGE_MODEL,
        torch_dtype=torch.float16,
        variant='fp16',
        add_watermarker=False,
        use_safetensors=USE_SAFETENSORS,
        cache_dir=MODEL_DIRECTORY,
    )
elif NSFW_ON is False:
    # enjoy NSFW content
    pipe = AutoPipelineForText2Image.from_pretrained(
        IMAGE_MODEL,
        torch_dtype=torch.float16,
        variant='fp16',
        use_safetensors=USE_SAFETENSORS,
        safety_checker=None,
        requires_safety_checker=False,
        add_watermarker=False,
        cache_dir=MODEL_DIRECTORY,
    )
else:
    raise ValueError("NSFW_ON must be True or False")

def flush_pipe():
    global pipe
    del pipe
    pipe=None
    gc.collect()
    torch.cuda.empty_cache()

#VRAM USAGE
def set_pipe_vram():
    global pipe
    if VRAM_MODE == 'low':
        pipe.enable_sequential_cpu_offload()
        pipe.enable_attention_slicing()
    elif VRAM_MODE == 'mid':
        pipe.enable_model_cpu_offload()
        pipe.enable_attention_slicing()
    elif VRAM_MODE == 'high':
        pipe.to("cuda")
    else:
        raise ValueError("VRAM_MODE must be set to 'low' 'mid' or 'high'")
set_pipe_vram()


#send response back to synology chat
def send_back_response(prompt, user_id, seed=None, image_url=None):
    if image_url is None:
        payload = 'payload=' + json.dumps({
            'text': f"{prompt}",
            "user_ids": [int(user_id)]
        })
    else:
        payload = 'payload=' + json.dumps({
            'text': f"{prompt}, seed({seed})",
            'file_url': f"{image_url}",
            "user_ids": [int(user_id)]
        })
    try:
        response = requests.post(INCOMING_WEBHOOK_URL, payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return "Error", 500
    finally:
        task_queue.task_done()
        processing_semaphore.release()
    return "success"

#generate image
def generate_image(message, user_id):  
    global SEED   
    if message.startswith("/seed"):
        input = message.replace("/seed", "").strip()
        try:
            int(input)
            SEED = input
            output=f"Seed is now set to {SEED}"
        except ValueError:
            SEED = 'random'
            output=f"Seed is now set to random"
        return send_back_response(output, user_id)
    else:
        try:   
            if SEED == 'random':
                seed = random.randint(0,759458189)
            else:
                seed = SEED
        except:
            pass
        prompt = f"{message}"
        def generate_message():
            global pipe
            generator = torch.manual_seed(seed)
            image = pipe(prompt=prompt, negative_prompt=NEGATIVE_PROMPT, height=HEIGHT, width=WIDTH, generator=generator, num_inference_steps=NUM_INFERENCE_STEPS, guidance_scale=GUIDANCE_SCALE).images[0]
            image_path = f"{IMAGE_SAVE_LOCATION}/ai_image.jpg"
            image.save(image_path)
            image_url = f"http://{LOCAL_HOST_IP}:8000/ai_image.jpg"
            send_back_response(prompt, user_id, seed, image_url)
        threading.Thread(target=generate_message).start()
        return "..."

#webserver hosting image to send back to chat
def run_web_server(directory, port=8000):
    os.chdir(directory)
    handler = SimpleHTTPRequestHandler
    httpd = TCPServer(('0.0.0.0', port), handler)
    print(f"Image server running at http://{LOCAL_HOST_IP}:{port}")
    httpd.serve_forever()

@app.route('/SynoImage', methods=['POST'])
def imagebot():
    token = SYNOCHAT_TOKEN
    webhook = OutgoingWebhook(request.form, token)
    if not webhook.authenticate(token):
        return webhook.createResponse('Outgoing Webhook authentication failed: Token mismatch.')
    message = webhook.text
    user_id = webhook.user_id
    task_queue.put((message, user_id))
    return "Task queued for processing"

def process_tasks():
    while True:
        processing_semaphore.acquire()
        try:
            message, user_id = task_queue.get()
            generate_image(message, user_id)
        finally:
            pass

processing_thread = threading.Thread(target=process_tasks, daemon=True)
processing_thread.start()

web_server_thread = threading.Thread(target=run_web_server, daemon=True, args=(f"{IMAGE_SAVE_LOCATION}",))
web_server_thread.start()

if __name__ == '__main__':
    app.run('0.0.0.0', port=FLASK_PORT, debug=False, threaded=True)
flush_pipe()