# Pull official latest Python Docker image (Pulished with version 3.10.12)
FROM --platform=linux/amd64 python:3.10.12

# Set the working directory
WORKDIR /usr/product

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

# Switch on virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the server port
EXPOSE $SERVER_PORT

# Install system dependencies
RUN apt-get update \
    && apt-get -y install gcc postgresql \
    && apt-get clean

RUN apt install -y netcat-traditional

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy all files
COPY . .

# Make entrypoint.sh executable
RUN chmod +x /usr/product/entrypoint.sh

# Execute entrypoint.sh
CMD ["/usr/product/entrypoint.sh" ]
