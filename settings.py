SYNOCHAT_TOKEN = "Synology Token"
INCOMING_WEBHOOK_URL = "Bot Incoming Webhook Url"
FLASK_PORT = 5020

LOCAL_HOST_IP = '192.168.1.X' #ie 192.168.1.2 #PC ip address
IMAGE_SAVE_LOCATION = 'D:/SynoImage/Images' 
MODEL_DIRECTORY = "D:/SynoImage/models"
HUGGINGFACE_TOKEN = "Huggingface_Token"

#IMAGE_MODEL = "CompVis/stable-diffusion-v1-4"
IMAGE_MODEL = "runwayml/stable-diffusion-v1-5"
#IMAGE_MODEL = "Kernel/sd-nsfw"
#IMAGE_MODEL = "prompthero/openjourney-v4"
#IMAGE_MODEL = "segmind/SSD-1B"
#IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

NSFW_ON = False #True or False
VRAM_MODE = 'mid' #'low' 'mid' 'high'

SEED = 'random' #specify number or use 'random'
HEIGHT = 512
WIDTH =  512
USE_SAFETENSORS = True
NUM_INFERENCE_STEPS = 50
NEGATIVE_PROMPT = "ugly, blurry, poor quality, unrealistic"
GUIDANCE_SCALE = 7.5




