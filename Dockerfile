# Base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose HTTP port
EXPOSE 80

# Run the application with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "--timeout", "720","app:app"]
