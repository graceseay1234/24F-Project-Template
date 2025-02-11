# Welcome to the HuskyNet project repository!

Welcome to HuskyNet — the dedicated networking platform designed exclusively for Northeastern University students and
alumni. Unlike generic networking sites, HuskyNet leverages data-driven insights to create meaningful connections 
tailored to your unique academic and professional journey. Major functions include:

- **Alumni Tracking** : Universities can monitor and engage with alumni more effectively.

- **Data Insights** : Gain valuable analytics on student career paths and outcomes.

- **Professional Connections** : Students can filter by major and find alumni in their field.

<img width="1408" alt="Screenshot 2024-12-04 at 5 23 45 PM" src="https://github.com/user-attachments/assets/7e7bf2f0-ac4b-4793-83a4-d6415a3874b6" />

## Prerequisites

- Docker desktop must be installed on your laptop.
- A distribution of Python running on your laptop (Choco (for Windows), brew (for Macs), miniconda, Anaconda, etc). 

## Current Project Components

Currently, there are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for the data model and database in the `./database-files` directory

## Setting up the Containers
1. Clone this repository to your local machine.
2. Inside the backend folder, duplicate the .env file to contain your own password.
3. Open a terminal or command prompt and navigate to the directory containing the docker-compose.yml file.
4. Build the Docker images by running the following command:
`docker compose build`
Start the containers by executing:
`docker compose up `
To run the containers in detached mode, use:
`docker compose up -d`

## Controlling the Containers

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them. 

## Contributers
- Addison Seay
- Blake Waldner
- Amir Marat
- Anne Hu	
- Lucas Rouaix

## Walk Through Video
- Dropbox: 
https://www.dropbox.com/scl/fi/8fqrbz9awyq5sgowgwkoa/CS3200FHuskyNet.mp4?rlkey=u3f93r0we3i6gnrlzn4ilbqsg&st=dyzu1h8q&dl=0
- Google Drive:
https://drive.google.com/file/d/1PKPn2Ot0QStw9uL49_v0Uj_CR0x5VXFX/view?usp=sharing

 
