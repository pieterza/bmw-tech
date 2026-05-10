FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose Flask default port
EXPOSE 8000

# Run Flask development server
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000", "--reload"]
