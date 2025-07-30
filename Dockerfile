# Use a specific, slim Python base image for security and size
FROM python:3.9-slim

# Set environment variables to improve Python's behavior in Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the default port for the application. This can be overridden at runtime.
ENV PORT=8080

# Set the working directory in the container
WORKDIR /app

# Create a non-root user and group for security
# Running as a non-root user is a security best practice
RUN addgroup --system app && adduser --system --group app

# Copy only the requirements file to leverage Docker's layer caching
COPY requirements.txt .

# Install dependencies using pip
# --no-cache-dir reduces the image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# A .dockerignore file should be used to exclude unnecessary files
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port the app will run on. This is for documentation and tooling.
# The actual port is determined by the PORT environment variable.
EXPOSE 8080

# Command to run the application using Gunicorn, a production-grade WSGI server.
# It binds to all network interfaces on the port specified by the PORT env var.
# The 'exec' form is used so that Gunicorn becomes PID 1 and handles signals correctly.
CMD exec gunicorn --bind 0.0.0.0:$PORT app:app