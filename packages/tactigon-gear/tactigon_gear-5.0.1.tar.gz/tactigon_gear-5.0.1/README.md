# Tactigon Gear

![The tactigon team](https://avatars.githubusercontent.com/u/63020285?s=200&v=4)

This package enables the wearable device Tactigon Skin to connect to your python project using Bluetooth Low Energy.

## Architecture

Tactigon Gear environment has the following architecture:

Server is located on the cloud and it is manteined by Next Industries s.r.l.
Server has a web interface where you can handle your profile and your data (models and gestures)

Provided Tactigon Gear SDK is the implementation of Tactigon Gear environment client side

Tactigon Gear SDK is used for collecting new raw data, send the data to server,
ask server to train a model using the raw data, and download the model from server. 
Finally use the model for testing real-time gesture recognition.

![Tactigon Gear architecture definition](https://www.thetactigon.com/wp/wp-content/uploads/2023/11/Architecture_Tactigon_Gear.png "Tactigon Gear architecture definition")  

## Prerequisites
In order to use the Tactigon Gear SDK the following prerequisites needs to be observed:

* Python version: following versions has been used and tested. It is STRONGLY recommended to use these ones depending on platform.
  * Win10: 3.8.7
  * Linux: 3.8.5
  * Mac osx: 3.8.10
  * Raspberry: 3.7.3

* It is recommended to create a dedicated python virtual environment and install the packages into the virtual environment:  
  * `python -m venv venv`
  * `pip install tactigon-gear`

* Depending on your installation (Linux, Raspberry, Mac users) you may need to use `python3` and `pip3` instead of `python` and `pip` respectively

## Licensing

In order to perform new training and download them you need to register on following web side:
`https://www.thetactigon.com/ai/web/`
Once registration is done you can go to Profile section and click on `Json File` button to download file user_data.json
The use of this file is described later in this doc.