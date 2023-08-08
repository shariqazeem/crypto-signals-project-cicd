FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt requirements.txt

# Install dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Copy the entire app directory from the host to the container
COPY . .

EXPOSE 5000

# Define the command to run your app
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
