# Stage 1: Grab a pre-compiled LibreDWG image from DockerHub
FROM kuzoncby/libredwg:latest AS libredwg_builder

# Stage 2: Build your actual Python API
FROM python:3.10-slim

# Copy the pre-compiled LibreDWG tools directly into this image!
COPY --from=libredwg_builder /usr/local/bin/ /usr/local/bin/
COPY --from=libredwg_builder /usr/local/lib/ /usr/local/lib/
RUN ldconfig

# Set up the Python API
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Expose the port and start the server
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
