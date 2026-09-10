FROM python:3.10-slim

# Install system dependencies required to compile LibreDWG
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    tar \
    texinfo \
    && rm -rf /var/lib/apt/lists/*

# Download, compile, and install LibreDWG in Low-Memory mode
RUN wget https://ftp.gnu.org/gnu/libredwg/libredwg-0.12.4.tar.gz \
    && tar -xvzf libredwg-0.12.4.tar.gz \
    && cd libredwg-0.12.4 \
    && CFLAGS="-O0" CXXFLAGS="-O0" ./configure --disable-bindings --disable-shared \
    && make \
    && make install \
    && ldconfig \
    && cd .. \
    && rm -rf libredwg-0.12.4*

# Set up the Python API
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Expose the port and start the server
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
