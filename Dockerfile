# Use the official Python 3.12 image.
FROM python:3.12-slim

# Set environment variables to optimize Python runtime in Docker.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code to the container.
COPY . .

# Expose port 5000 to be accessible from the host.
EXPOSE 5000

# Define the command to run your application.
CMD ["flask", "run", "--host=0.0.0.0"]
