# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy .env file into the container
COPY .env .env

# Set environment variables from .env file
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
ENV TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
ENV MONGODB_CONNECTION_STRING=${MONGODB_CONNECTION_STRING}
ENV GMAIL_USER=${GMAIL_USER}
ENV GMAIL_PASSWORD=${GMAIL_PASSWORD}

# Make port 8088 available to the world outside this container
EXPOSE 8088

# Run app.py when the container launches
CMD ["python", "app.py"]
