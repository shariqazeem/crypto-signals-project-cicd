FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Update the system and install required dependencies
RUN apt-get update && \
    apt-get install -y libmysqlclient-dev build-essential

# Copy the requirements.txt file to the container
COPY requirements.txt requirements.txt

# Install dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Copy the entire app directory from the host to the container
COPY . .

# Define the command to run your app
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
