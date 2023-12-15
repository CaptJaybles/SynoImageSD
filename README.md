# SynoImageSD
Using stable diffusion with synology chat

Only tested on Windows 10

Install

  1) clone repository

  2) create virtual envirement in folder

    python -m venv venv
    
  3) activate virual envirement

    venv/Scripts/activate

  4) install the requirements

    pip install -r requirements.txt
    
Setup

  1) setup a new bot in your synology chat app

  2) the outgoing URL in synology integration will be http://IP_ADDRESS:FLASK_PORT/SynoImage change IP_ADDRESS and FLASK_PORT to what it is on your local PC your running the model on

  3) copy the synology Token and the incoming URL to the settings file

  4) Create and place your huggingface token for the HUGGINGFACE_TOKEN variable in settings

  5) Set the IP address of your PC in the settings file for LOCAL_HOST_IP

  6) Set the correct file locations for IMAGE_SAVE_LOCATION and MODEL_DIRECTORY ie D:/SynoImage/model and D:/SynoImage/Images

  7) In the settings for IMAGE_MODEL I have some of the models I have tested on my laptop, you can use those or try something else it may work depending on your system.

  8) All the other settings can be changed to your preference

  9) Use either SynoImageSD.bat file or command

    python SynoImageSD.py

Features

  1) load image models at various degrees of ram usage
  2) seed set to random initially but can be changed to a set number 

Commands

  1) /seed can set seed to a number or use 'random' for a random number
