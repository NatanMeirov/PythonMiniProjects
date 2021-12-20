import threading
import time
import logging
from webdriver_wrapper import WebDriverWrapper
import youtube_content_downloader_utils


# TODO:
# 1) Fix bugs (Unwanted behaviors (strange and inconsistent element selection))
# 2) Add logging for each important step (using LOCK to avoid conflicts)
# 3) Add try/except blocks for each critical step
class YouTubeContentDownloader():

    YOUTUBE_URL = r"https://www.youtube.com"
    WEB_CONVERTERS_URL = [
        r"https://down4me.net",
        r"https://www.ytdown.net"
    ]
    JS_CLICK_COMMAND = "arguments[0].click();" # Uses: webdriver.execute_script("arguments[0].click();", element) -> Using JS click method instead of regular click method for better and faster scraping

    def __init__(self, driver_path: str, songs: list, videos: list, logger: logging.Logger):
        self.__driver_path = driver_path
        self.__songs = songs
        self.__videos = videos
        self.__logger = logger


    def __create_driver(self) -> WebDriverWrapper:
        return WebDriverWrapper(self.__driver_path)


    def __collect_all_items_from_page(self, driver_wrapper: WebDriverWrapper) -> list:
        # Page loads while scrolling down => Slows the scraping
        # current_state = driver_wrapper.web_driver.execute_script("return document.documentElement.scrollHeight;")
        # while True:
        #     previous_state = driver_wrapper.web_driver.execute_script("return document.documentElement.scrollHeight;")
        #     driver_wrapper.web_driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        #     time.sleep(1)
        #     current_state = driver_wrapper.web_driver.execute_script("return document.documentElement.scrollHeight;")
        #     if previous_state == current_state:
        #         break
        time.sleep(3)
        return list(driver_wrapper.web_driver.find_elements_by_xpath('//*[@id="video-title"]')) # all visible elements


    def __extract_titles_from_youtube_items(self, page_items: list) -> list:
        return [str(item.get_attribute("title")) for item in page_items]


    def __get_youtube_content_url(self, driver_wrapper: WebDriverWrapper, item: str) -> str:
        # The "shorter way":
        # driver.web_driver.get(f"{self.YOUTUBE_URL}/results?search_query={item}")
        # ...
        ############################################
        # The "longer way" using Selenium WebDriver:
        driver_wrapper.web_driver.get(self.YOUTUBE_URL)

        driver_wrapper.waiting_timer.until(driver_wrapper.is_visible((driver_wrapper.locate_by.CSS_SELECTOR, "#search-input.ytd-searchbox-spt input")))
        search_text_box = driver_wrapper.web_driver.find_element_by_css_selector("#search-input.ytd-searchbox-spt input")
        driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, search_text_box)
        search_text_box.send_keys(item)

        search_submit_button = driver_wrapper.web_driver.find_element_by_id("search-icon-legacy")
        driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, search_submit_button)

        driver_wrapper.waiting_timer.until(driver_wrapper.is_visible((driver_wrapper.locate_by.CSS_SELECTOR, "#video-title"))) # At least one is visible
        ### New Code: ###
        all_page_items = self.__collect_all_items_from_page(driver_wrapper)
        wanted_elements = [all_page_items[0], all_page_items[1], all_page_items[2]]
        wanted_elements_titles = self.__extract_titles_from_youtube_items(wanted_elements)
        index = youtube_content_downloader_utils.find_correct_item_element_index_by_title(wanted_elements_titles, item) # Matching Algorithm
        print(index)
        driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, wanted_elements[index]) # Using the index
        # print(wanted_element)
        ### End of New Code ###

        ### Old Code: ###
        # all_page_items = self.__collect_all_items_from_page(driver_wrapper)
        # all_titles = self.__extract_titles_from_youtube_items(all_page_items)
        # index = youtube_content_downloader_utils.find_correct_item_element_index_by_title(all_titles, item) # Matching Algorithm
        # print(index)
        # driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, all_page_items[index]) # Using the index
        ### End of Old Code ###

        # driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, wanted_element)
        driver_wrapper.waiting_timer.until(driver_wrapper.is_visible((driver_wrapper.locate_by.TAG_NAME, "video")))

        correct_content_url = driver_wrapper.web_driver.current_url
        print(correct_content_url)
        return correct_content_url


    def __convert_and_download(self, driver_wrapper: WebDriverWrapper, content_url: str, item_format: str) -> None:
        try:
            driver_wrapper.web_driver.get(self.WEB_CONVERTERS_URL[0])
        except:
            driver_wrapper.web_driver.get(self.WEB_CONVERTERS_URL[1])

        driver_wrapper.waiting_timer.until(driver_wrapper.is_visible((driver_wrapper.locate_by.XPATH, f'//*[@id="{item_format}"]')))
        format_button = driver_wrapper.web_driver.find_element_by_xpath(f'//*[@id="{item_format}"]') # mp3 for songs or mp4 for videos
        driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, format_button)

        driver_wrapper.waiting_timer.until(driver_wrapper.is_visible((driver_wrapper.locate_by.XPATH, '//*[@id="input"]')))
        url_content_input_field = driver_wrapper.web_driver.find_element_by_xpath('//*[@id="input"]')
        driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, url_content_input_field)
        url_content_input_field.send_keys(content_url)

        converter_submit_button = driver_wrapper.web_driver.find_element_by_xpath('//*[@id="submit"]')
        driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, converter_submit_button)

        driver_wrapper.waiting_timer.until(driver_wrapper.is_visible((driver_wrapper.locate_by.XPATH, '//*[@id="download"]'))) # Until the element is visible to the user - the convertion had finished
        download_button = driver_wrapper.web_driver.find_element_by_xpath('//*[@id="download"]')
        driver_wrapper.web_driver.execute_script(self.JS_CLICK_COMMAND, download_button)


    def __download_single_item(self, item: str, item_format: str) -> None:
        driver_wrapper = self.__create_driver()
        content_url = self.__get_youtube_content_url(driver_wrapper, item)
        self.__convert_and_download(driver_wrapper, content_url, item_format)


    def download_content(self) -> None:
        if self.__songs:
            for song in self.__songs:
                t = threading.Thread(target = self.__download_single_item, args = (song, "mp3"))
                t.start()

        if self.__videos:
            for video in self.__videos:
                t = threading.Thread(target = self.__download_single_item, args = (video, "mp4"))
                t.start()
                # Log (with LOCK to avoid conflicts)