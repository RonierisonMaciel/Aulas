from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

target = "https://www.demo.com.br"
base_dir = "/wp-content/"
directories = [
    'uploads/2015/10/', 'uploads/2015/11/', 'uploads/2015/12/',
    'uploads/2016/01/', 'uploads/2016/02/', 'uploads/2016/03/',
    'uploads/2016/04/', 'uploads/2016/05/', 'uploads/2016/06/',
    'uploads/2016/07/', 'uploads/2016/08/', 'uploads/2016/09/',
    'uploads/2016/10/', 'uploads/2016/11/', 'uploads/2016/12/'
]

file = ['.jpg', '.png', 'txt', 'docx', '.pdf']

browser = webdriver.FirefoxOptions()
browser.headless = True 
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=browser)

def get_links(url):
    driver.get(url)
    time.sleep(5)
    elements = driver.find_elements(By.TAG_NAME, 'a')
    return [element.get_attribute('href') for element in elements if element.get_attribute('href') is not None]


def is_file_link(link):
    return any(link.endswith(ft) for ft in file)


def crawler_directory(directory_url):
    for link in get_links(directory_url):
        if is_file_link(link):
            print(f"Arquivo encontrado: {link}")

try:
    for directory in directories:
        path_direct = target + base_dir + directory
        crawler_directory(path_direct)
finally:
    driver.quit()
