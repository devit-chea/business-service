FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first (to leverage Docker's layer caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install gunicorn
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Expose the port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8001", "service_business.wsgi:application"]
