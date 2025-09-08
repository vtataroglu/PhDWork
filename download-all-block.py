import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_and_parse_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print("Failed to retrieve the webpage")
        return None

def extract_links(soup):
    links = soup.find_all('a')
    filtered_links = [
        (link.text.strip(), link.get('href'))
        for link in links 
        if link.get('href') and "blockchair_bitcoin_blocks" in link.get('href')
    ]
    return filtered_links

def download_file(url, href):
    try:
        response = requests.get(url + href)
        if response.status_code == 200:
            file_path = href.split("/")[-1]  # Basic example to name the file
            with open(file_path, "wb") as file:
                file.write(response.content)
            return href, True
    except Exception as e:
        print(f"22Failed to download {href}: {e}")
    return href, False

def main():
    url = 'https://gz.blockchair.com/bitcoin/blocks/'
    soup = fetch_and_parse_url(url)
    if soup:
        links = extract_links(soup)
        # Filter out files that have already been downloaded
        links_to_download = [(text, href) for text, href in links if not os.path.exists(href.split("/")[-1])]

        total_links = len(links_to_download)
        print(f"{len(links)} but Attempting to download {total_links} filtered links.")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(download_file, url, href) for _, href in links_to_download}
            for future in as_completed(futures):
                href, success = future.result()
                print(f"{'Successfully' if success else 'Failed to'} download {href}")

if __name__ == "__main__":
    main()
