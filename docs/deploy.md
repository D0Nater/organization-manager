# Docker Compose Deployment Guide

This guide will walk you through the process of deploying your application using `docker compose`, which relies on a `docker-compose.yml` and an environment file (`.env`).

## Configure the Environment Variables

Your project uses an `.env.example` file to show you what environment variables are needed. Before starting the application, you must create your own `.env` file and fill it with your specific configuration.

1. Copy the example environment file:
   
   ```bash
   cp .env.example .env
   ```
- Open the newly created `.env` file in a text editor.

- Go through the file and replace the placeholder values with your desired settings.

- Save and close the `.env` file.

## Run the Application in Detached Mode

Once your `.env` file is configured, you can start the application with Docker Compose in detached mode (`-d`). This will run all services in the background.

1. Navigate to the directory containing your `docker-compose.yml` file.
2. Execute the following command:
   
   ```bash
   docker compose up -d
   ```
- If any image needs to be built, Docker Compose will handle this automatically before starting the containers in the background.

## Stop the Application

To stop all services and remove the containers, use the following command:

```bash
docker compose down
```
