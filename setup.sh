#!/bin/bash

# Update and install required packages
sudo apt update
sudo apt install -y python3 python3-venv python3-pip docker-compose

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat <<EOF > .env
KAFKA_BROKER_URL=localhost:9092
EOF

# Build and start Docker containers
docker-compose up -d

echo "Setup complete. Access the API at http://localhost:8000/hello"