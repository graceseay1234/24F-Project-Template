# Welcome to the HuskyNet project repository!

Welcome to HuskyNet — the dedicated networking platform designed exclusively for Northeastern University students and
alumni. Unlike generic networking sites, HuskyNet leverages data-driven insights to create meaningful connections 
tailored to your unique academic and professional journey. Major functions include:

- **Alumni Tracking** : Universities can monitor and engage with alumni more effectively.

- **Data Insights** : Gain valuable analytics on student career paths and outcomes.

- **Professional Connections** : Students can filter by major and find alumni in their field.
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

## Contributers:
- Addison Seay
- Blake Waldner
- Amir Marat
- Anne Hu	
- Lucas Rouaix

 
