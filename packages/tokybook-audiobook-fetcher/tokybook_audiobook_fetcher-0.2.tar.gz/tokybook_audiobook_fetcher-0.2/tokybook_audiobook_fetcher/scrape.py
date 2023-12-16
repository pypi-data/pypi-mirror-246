import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import re


def get_audiobook_title(url):
    return url.rsplit("/", 1)[1].replace('-', ' ').title()


def fetch_audiobook_script_content(audiobook_url):
    try:
        page = requests.get(audiobook_url)
        soup = BeautifulSoup(page.content, "html.parser")
        script_tags = soup.find_all("script")

        script_contents = [tag.string for tag in script_tags if tag.string]

        return script_contents

    except requests.RequestException as e:
        print(f"Error fetching audiobook script content: {e}")
        return None


def extract_and_format_download_links(audiobook_url):
    script_contents = fetch_audiobook_script_content(audiobook_url)

    if script_contents:
        link_pattern = re.compile(r'"chapter_link_dropbox"\s*:\s*"(.*?)",')
        download_links = []

        for script_content in script_contents:
            matches = re.findall(link_pattern, script_content)

            for match in matches:
                formatted_link = quote(match, safe='/:')
                formatted_link = formatted_link.replace('%5C', '/')
                full_link = urljoin("https://files02.tokybook.com/audio/", formatted_link)
                download_links.append(full_link)

        return download_links
    else:
        return []
