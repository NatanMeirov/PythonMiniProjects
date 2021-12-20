import argparse
import sys
import os
import logging
from youtube_content_downloader import YouTubeContentDownloader


def get_driver_songs_and_videos_to_download():
    parser = argparse.ArgumentParser(description="Auto YouTube Songs and Videos Downloader:\nUse -s/--songs option to add Songs and -v/--videos to add videos.\n(Each of them must be one long comma separated input string. Use '-' key to separate words of each item included in this comma separated string.)")
    parser.add_argument("path_to_driver", type = str, help = "Path to the Chrome Driver executable")
    parser.add_argument("-s", "--songs", dest = "songs", type = str, help = "Songs to download from YouTube in MP3 format. Input should be given as a long string separeted by commas")
    parser.add_argument("-v", "--videos", dest = "videos", type = str, help = "Videos to download from YouTube in MP4 format. Input should be given as a long string separeted by commas")
    arguments = parser.parse_args()

    try:
        if os.path.split(arguments.path_to_driver)[1] != "chromedriver.exe": # Tail of the path (meaning the input path was the directory of the chrome driver executable)
            driver_path = f"{arguments.path_to_driver}{os.sep}chromedriver.exe"
        else:
            driver_path = arguments.path_to_driver

        if not os.path.exists(arguments.path_to_driver):
            raise IOError("Error - Wrong Input (path_to_driver): The path to the Chrome Driver is incorrect. \nPlease make sure to install Chrome Driver and give the correct path to the Chrome Driver executable installation (e.g: chromedriver.exe).")

        if not arguments.songs and not arguments.videos:
            raise IOError("Error - Wrong Input: No songs or videos was found. \nPlease give at least one of these two options.")

    except IOError as err:
        print(err)
        sys.exit()

    if arguments.songs:
        songs = arguments.songs.replace("-", " ").split(",") # Replace every "-" from the item's name for " " (space) to use the real name of the item (to search in YouTube), than splits the whole string to a list of separate items names
    else:
        songs = []

    if arguments.videos:
        videos = arguments.videos.replace("-", " ").split(",") # Replace every "-" from the item's name for " " (space) to use the real name of the item (to search in YouTube), than splits the whole string to a list of separate items names
    else:
        videos = []

    return driver_path, songs, videos


def initialize_logger():
    logger = logging.getLogger("YouTubeContentDownloaderLogger")
    file_handler = logging.StreamHandler(stream = "youtube_content_downloader.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def main():
    logger = initialize_logger()
    driver_path, songs, videos = get_driver_songs_and_videos_to_download()
    downloader = YouTubeContentDownloader(driver_path, songs, videos, logger)
    downloader.download_content()


if __name__ == "__main__":
    main()
