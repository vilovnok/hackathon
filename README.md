# Aillustrate
A service for image generation without industrial engineering.

## Pipeline
![Pipeline](photo/scheme.png "Pipeline")

## How To Deploy

### Clone repo to server
```
richie@gur:~$ git clone https://github.com/Aillustrate/bootcamp-hackathon.git
```
## The first way
### Run application from docker-compose.yaml
```
richie@gur:~$ docker-compose up  
``` 

## The second way 
### Run application from root folder aillustrate
```
richie@gur:~$ cd aillustrate/ 
richie@gur:~$ ng serve 
```
### Install requirements.txt from root folder /restapi/
```
richie@gur:~$ pip3 install -r requirements.txt
```
### Run application from root folder /restapi/src/
```
richie@gur:~$ cd /restapi/src/
richie@gur:~$ uvicorn main:app --port 8000 --reload 
richie@gur:~$ uvicorn main:app --port 8000 --reload 
```