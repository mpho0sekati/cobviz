# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install git (required by GitPython)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Suppress GitPython warning and potential boot issues
ENV GIT_PYTHON_REFRESH=quiet

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the application package
RUN pip install --no-cache-dir .

# Render uses $PORT environment variable
EXPOSE 5000

# Run gunicorn
# Use shell form to expand $PORT
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} cobviz.web:app
