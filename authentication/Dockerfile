# Pull official latest Python Docker image (Pulished with version 3.10.12)
FROM --platform=linux/amd64 python:3.10.12

# Set the working directory
WORKDIR /usr/authentication

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

# Switch on virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the server port
EXPOSE 8000

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

# Copy entrypoint.sh for auto connection with account_db service
COPY ./entrypoint.sh .
RUN chmod +x /usr/authentication/entrypoint.sh

# Execute entrypoint.sh
ENTRYPOINT ["/usr/authentication/entrypoint.sh" ]

# Start up the authentication server
# CMD uvicorn src.main:app --reload --workers 4 --host 0.0.0.0 --port 8000
# CMD bash
