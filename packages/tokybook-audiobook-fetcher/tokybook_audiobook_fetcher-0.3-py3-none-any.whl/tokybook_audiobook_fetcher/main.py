import sys

from tokybook_audiobook_fetcher.download import download_audiobook

if __name__ == "__main__":
    download_audiobook(sys.argv[1])