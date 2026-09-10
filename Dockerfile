FROM python:3.10-slim

# Install system libraries needed by the pre-compiled binary
RUN apt-get update && apt-get install -y libpcre2-8-0 && rm -rf /var/lib/apt/lists/*

# Copy the pre-compiled binaries into the Linux system
COPY dxf2dwg /usr/local/bin/dxf2dwg
COPY libredwg.so.0 /usr/local/lib/libredwg.so.0
RUN chmod +x /usr/local/bin/dxf2dwg && ldconfig

# Set up the Python API
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Expose the port and start the server
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
