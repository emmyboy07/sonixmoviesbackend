from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests
from threading import Thread

app = Flask(__name__)

# Dictionary to track download progress and status
downloads = {}

# Configure Selenium WebDriver (Headless Chrome)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service("/usr/bin/chromedriver")  # Update this path if needed
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape FzMovies for a download link using Selenium
def scrape_fzmovies(movie_name, release_year):
    search_url = f"https://fzmovies.net/search.php?searchname={movie_name.replace(' ', '+')}&searchby=name"
    driver.get(search_url)
    time.sleep(2)  # Allow page to load

    # Find all movie links on search results page
    movie_links = driver.find_elements(By.TAG_NAME, "a")

    for link in movie_links:
        if str(release_year) in link.text:
            link.click()  # Open movie page
            time.sleep(2)

            # Find the download button
            try:
                download_link = driver.find_element(By.LINK_TEXT, "Download")
                return download_link.get_attribute("href")
            except:
                return None
    
    return None

# Function to download a movie
def stream_download(url, download_id):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    downloads[download_id] = {"progress": 0, "status": "active"}

    with open(f"downloads/{download_id}.mp4", "wb") as file:
        for chunk in response.iter_content(1024):
            if not chunk:
                break

            while downloads[download_id]["status"] == "paused":
                time.sleep(1)

            file.write(chunk)
            downloaded += len(chunk)
            progress = (downloaded / total_size) * 100
            downloads[download_id]["progress"] = progress

    downloads[download_id]["status"] = "completed"

@app.route('/start-download', methods=['POST'])
def start_download():
    data = request.json
    movie_name = data.get('movie_name')
    release_year = data.get('release_year')

    if not movie_name or not release_year:
        return jsonify({'error': 'Missing parameters'}), 400

    download_url = scrape_fzmovies(movie_name, release_year)
    
    if not download_url:
        return jsonify({'error': 'Movie not found'}), 404

    download_id = f"{movie_name}_{release_year}"
    downloads[download_id] = {"progress": 0, "status": "active"}
    
    thread = Thread(target=stream_download, args=(download_url, download_id))
    thread.start()

    return jsonify({'message': 'Download started', 'id': download_id, 'url': download_url})

@app.route('/pause-download', methods=['POST'])
def pause_download():
    data = request.json
    download_id = data.get('id')

    if download_id in downloads and downloads[download_id]["status"] == "active":
        downloads[download_id]["status"] = "paused"
        return jsonify({'message': 'Download paused', 'id': download_id})
    return jsonify({'error': 'Download not found or already paused'}), 400

@app.route('/resume-download', methods=['POST'])
def resume_download():
    data = request.json
    download_id = data.get('id')

    if download_id in downloads and downloads[download_id]["status"] == "paused":
        downloads[download_id]["status"] = "active"
        return jsonify({'message': 'Download resumed', 'id': download_id})
    return jsonify({'error': 'Download not found or not paused'}), 400

@app.route('/download-progress', methods=['GET'])
def get_progress():
    return jsonify(downloads)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
