import time
import os

import pytest
from selenium.webdriver.common.by import By

cur_dir = os.getcwd()
path_chrome = f'{os.getcwd()}/chrome_driver/chromedriver'

base_url = 'https://demoqa.com/'
elements_url = base_url + 'elements'
check_box_url = base_url + 'checkbox'

elements_class = 'card-body'
check_box_id = 'item-1'

downloads_xpath = '//*[@id="tree-node"]/ol/li/ol/li[3]/span/button'
home_xpath = '//*[@id="tree-node"]/ol/li/span/button'
word_file_xpath = '//*[@id="tree-node"]/ol/li/ol/li[3]/ol/li[1]/span/label'
result_xpath = '//*[@id="result"]/span[1]'

separators = ['-', ' ', '_']  # Возможные символы, используемые как разделители  в строках


def clean_str(string: str):
    """Функция удаляет символы '-', ' ', '_' в строке"""
    for sep in separators:
        if sep in string:
            string = string.replace(sep, '')
    return string


def custom_find_element(driver, value: str):
    """Ищет элемент на странице, в зависимости от переданного значения строки"""
    by = None
    if value.startswith('#'):
        by = By.CSS_SELECTOR
    elif value.startswith('/'):
        by = By.XPATH
    else:
        joined_value = clean_str(value)
        if joined_value.isalpha():
            by = By.CLASS_NAME
        elif joined_value.isalnum():
            by = By.ID

    return driver.find_element(by, value)


def test_page(driver):
    driver.get(base_url)
    elements = custom_find_element(driver, elements_class)
    assert driver.current_url == base_url
    assert elements.is_displayed()

    elements.click()
    driver.save_screenshot('demoqa.com/elements is open.png')
    time.sleep(3)  # Ждем некоторое время, чтобы удедиться, что всё работает
    check_box = custom_find_element(driver, check_box_id)

    assert check_box.is_displayed()
    assert driver.current_url == elements_url
    check_box.click()
    time.sleep(3)

    home = custom_find_element(driver, home_xpath)
    assert home.is_displayed()
    assert driver.current_url == check_box_url
    home.click()
    time.sleep(3)

    downloads = custom_find_element(driver, downloads_xpath)
    assert home.is_displayed()
    downloads.click()
    time.sleep(3)

    word_file = driver.find_element(By.XPATH, word_file_xpath)
    assert word_file.text == 'Word File.doc'
    word_file.click()
    result = custom_find_element(driver, result_xpath)
    assert result.is_displayed()
    assert result.text == 'You have selected :'
    time.sleep(3)


