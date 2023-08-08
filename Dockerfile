FROM python:3

# Set the working directory inside the container
WORKDIR /usr/src/app

# Update the system clock and install system dependencies
RUN apt-get update

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory from the host to the container
COPY . .

# Define the command to run your app
CMD ["python", "app.py"]
