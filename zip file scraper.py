import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve

# Function to get all links to zip files from a webpage
def get_zip_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.zip'):
            links.append(urljoin(url, href))
    return links

# Function to download files to a specified folder
def download_files(links, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    total_files = len(links)

    for index, link in enumerate(links, start=1):
        filename = os.path.basename(urlparse(link).path)
        filepath = os.path.join(download_folder, filename)

        if os.path.exists(filepath):
            print(f"{filename} already exists. Skipping download.")
        else:
            print(f"Downloading {filename} ({index} of {total_files})...")
            urlretrieve(link, filepath)
            print(f"Downloaded {filename}")

if __name__ == "__main__":
    # Ask for the download directory first
    download_folder = input("Enter the path of the download folder: ")

    # Check for the 'addy' file
    addy_file = os.path.join(download_folder, 'addy.txt')
    if os.path.exists(addy_file):
        with open(addy_file, 'r') as f:
            url = f.read().strip()
        print(f"Using website from 'addy.txt': {url}")
    else:
        url = input("Enter the URL of the website: ")
        with open(addy_file, 'w') as f:
            f.write(url)
        print(f"Website recorded in 'addy.txt': {url}")

    zip_links = get_zip_links(url)
    print(f"Total ZIP files found: {len(zip_links)}")

    download_files(zip_links, download_folder)

    print("All files downloaded successfully.")
