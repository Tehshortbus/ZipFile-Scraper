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
        if href and href.endswith('.zip'):
            links.append(urljoin(url, href))
    return links

# Function to display zip file names in batches
def display_zip_files(zip_links):
    for i in range(0, len(zip_links), 100):
        batch = zip_links[i:i + 100]
        print(f"\nBatch {i // 100 + 1}:")
        for link in batch:
            filename = os.path.basename(urlparse(link).path)
            print(filename)
        
        if i + 100 < len(zip_links):
            user_input = input("Press Enter to view the next batch or 'X' to quit: ")
            if user_input.strip().lower() == 'x':
                break

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

    display_zip_files(zip_links)

    # Confirm download
    confirm = input("Do you want to download these files? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Aborting download.")
    else:
        download_files(zip_links, download_folder)
        print("All files downloaded successfully.")
