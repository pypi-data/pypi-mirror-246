import sys

from tokybook_audiobook_fetcher.download import download_audiobook


def main_function():
    download_audiobook(sys.argv[1])


if __name__ == "__main__":
    download_audiobook(sys.argv[1])
