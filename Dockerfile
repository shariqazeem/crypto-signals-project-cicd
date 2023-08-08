FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory from the host to the container
COPY . /app

# Expose port 5000
EXPOSE 5000

# Define the command to run your app
CMD ["python", "app.py"]
