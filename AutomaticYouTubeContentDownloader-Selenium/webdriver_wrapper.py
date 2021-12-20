import sys
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Please make sure to install selenium first. Use 'pip install selenium' command")
    sys.exit()


class WebDriverWrapper():
    def __init__(self, driver_path: str):
        options = self.__init_chrome_options()
        self.web_driver = webdriver.Chrome(driver_path, chrome_options = options)
        self.waiting_timer = WebDriverWait(self.web_driver, 10)
        self.is_present = EC.presence_of_element_located
        self.is_visible = EC.visibility_of_element_located
        self.locate_by = By


    def __init_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument('--no-sandbox')
        options.add_argument('--verbose')
        options.add_argument('--disable-software-rasterizer')
        options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})

        return options
