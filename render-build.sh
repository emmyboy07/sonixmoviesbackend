#!/bin/bash
# Install Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable

# Install ChromeDriver
CHROME_VERSION=$(google-chrome-stable --version | cut -d ' ' -f 3 | cut -d '.' -f 1)
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.0.0/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip -d /usr/bin/
chmod +x /usr/bin/chromedriver
