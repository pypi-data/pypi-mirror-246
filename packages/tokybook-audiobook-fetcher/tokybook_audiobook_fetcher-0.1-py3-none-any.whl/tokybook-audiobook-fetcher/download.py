import logging
import os

import requests
import tqdm
from scrape import get_audiobook_title, extract_and_format_download_links


def create_audiobook_file(response, chapter_counter, audiobook_title):
    directory_name = audiobook_title
    desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop")
    file_name = f"Chapter{chapter_counter}.mp3"
    file_path = os.path.join(desktop_directory, directory_name)

    # Check if directory already exists, if not, create it
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    download_path = os.path.join(file_path, file_name)

    write_response_to_file(response, download_path)


def download_audiobook_data(audiobook_links, audiobook_title):
    # Skip the first link since it's an advertisement
    download_links = audiobook_links[1:]

    logging.basicConfig(level=logging.INFO)
    with tqdm.tqdm(total=len(download_links), desc=f"Downloading {audiobook_title}", unit="chapter") as progress_bar:

        for chapter_counter, download_link in enumerate(download_links, start=1):
            try:
                response = requests.get(download_link, allow_redirects=True)
                create_audiobook_file(response, chapter_counter, audiobook_title)
            except requests.RequestException as e:
                print(f"Error downloading chapter {chapter_counter}: {e}")

            progress_bar.update(1)

    logging.info(" Audiobook download complete!")


def write_response_to_file(response, file_path):
    try:
        with open(file_path, 'wb') as output_file:
            output_file.write(response.content)
    except Exception as e:
        print(f"Error writing to file: {e}")


def download_audiobook(audiobook_url):
    audiobook_title = get_audiobook_title(audiobook_url)
    download_links = extract_and_format_download_links(audiobook_url)
    download_audiobook_data(download_links, audiobook_title)
