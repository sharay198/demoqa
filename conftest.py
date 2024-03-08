import os
from pathlib import Path
import pytest
from fake_useragent import UserAgent
from selenium import webdriver
import subprocess


def get_firefox_profile():
    for pth in paths_to_profile:
        if os.path.exists(pth):
            return pth


def create_profile(name='testing'):
    for obj in os.listdir(path_to_profile):
        if not obj.split('testing'):
            return subprocess.check_output(f'firefox --createprofile {name}', shell=True)


home = os.path.expanduser('~')

paths_to_profile = [f'{home}/snap/firefox/common/.mozilla/firefox/',
                    f'{home}/.var/app/org.mozilla.firefox/.mozilla/firefox/',
                    f'{home}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
                    ]

ua_chrome = UserAgent().chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'user-agent={ua_chrome}')

path_to_profile = get_firefox_profile()

ua_firefox = UserAgent().firefox
options = webdriver.FirefoxOptions()
options.add_argument(f'user-agent={ua_firefox}')
options.add_argument('-profile')
options.add_argument(path_to_profile)


@pytest.fixture(params=[webdriver.Firefox(options=options), webdriver.Chrome(options=chrome_options)])
def driver(request):
    driver = request.param
    driver.implicitly_wait(10)
    if driver.caps['browserName'] != 'chrome':
        create_profile()
    yield driver
    driver.close()

