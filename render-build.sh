#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Use Render's pre-installed Chromium (instead of installing Chrome)
export CHROME_BIN=/opt/render/project/chromium/chrome
export CHROMEDRIVER_BIN=/opt/render/project/chromium/chromedriver

echo "✅ Build setup complete!"
