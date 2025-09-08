# Use a slim Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY ./app /app

# Expose the port your application runs on
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]