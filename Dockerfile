FROM python:3.10-slim

# Install system libraries and patchelf
RUN apt-get update && apt-get install -y libpcre2-8-0 patchelf && rm -rf /var/lib/apt/lists/*

COPY dxf2dwg /usr/local/bin/dxf2dwg
COPY libredwg.so.0 /usr/local/lib/libredwg.so.0

# Patch the binary so it uses the standard Linux linker
RUN chmod +x /usr/local/bin/dxf2dwg \
    && patchelf --set-interpreter /lib64/ld-linux-x86-64.so.2 /usr/local/bin/dxf2dwg \
    && ldconfig

# Set up the Python API
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Expose the port and start the server
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
