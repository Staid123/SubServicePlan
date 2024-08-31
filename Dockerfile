FROM python:3.10

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create directory for the application and set the working directory
RUN mkdir /service
WORKDIR /service

# Set PYTHONPATH to ensure modules can be found
ENV PYTHONPATH=/service

# Copy dependency files
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY service/ .

# Expose ports
EXPOSE 8000
