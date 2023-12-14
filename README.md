# SynoImageSD
Using stable diffusion with synology chat

Only tested on Windows 10, builds on llama-ccp-python

Install

install visual studio community 2022 (I checked python development and C++ developement)

clone repository

create virtual envirement in folder

python -m venv venv
activate virual envirement
venv/Scripts/activate
install the requirements
pip install -r requirements.txt
Setup

setup a new bot in your synology chat app

the outgoing URL in synology integration will be http://IP_ADDRESS:FLASK_PORT/SynoImage change IP_ADDRESS and FLASK_PORT to what it is on your local PC your running the model on

copy the synology Token and the incoming URL to the settings file

Create and place your huggingface token for the HUGGINGFACE_TOKEN variable in settings

Set the IP address of your PC in the settings file for LOCAL_HOST_IP

Set the correct file locations for IMAGE_SAVE_LOCATION and MODEL_DIRECTORY ie D:/SynoImage/model and D:/SynoImage/Images

In the settings for IMAGE_MODEL I have some of the models I have tested on my laptop, you can use those or try something else it may work depending on your system.

All the other settings can be changed to your preference

Use either SynoImageSD.bat file or command

python SynoImageSD.py

Features

load image models at various degrees of ram usage
seed set to random initially but can be changed to a set number 

Commands

/seed can set seed a number or use 'random' for a random number
