#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install Chromium & Chromedriver (Render doesn't support sudo)
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > chrome.deb
apt-get update && apt-get install -y ./chrome.deb
rm chrome.deb

# Get the correct version of Chromedriver
CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d '.' -f 1)
wget -q "https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)/chromedriver_linux64.zip" -O /tmp/chromedriver.zip

# Extract and move Chromedriver
unzip /tmp/chromedriver.zip -d /usr/bin/
chmod +x /usr/bin/chromedriver

echo "✅ Build setup complete!"
