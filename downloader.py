'''
Main downloader, XU Zhengyi, 2020/05/05
'''
import base64
import logging
import os
import random
import time
from io import BytesIO
from PIL import ImageOps

import PIL.Image as pil_image
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

# DO NOT REMOVE THIS LINE. Used for __subclasses__()
from website_actions import *
from website_actions.abstract_website_actions import WebsiteActions

logging.basicConfig(format='[%(levelname)s](%(name)s) %(asctime)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def get_cookie_dict(cookies):
    cookies_split = cookies.split('; ')
    if len(cookies_split) == 1:
        cookies_split = cookies.split(';')
    cookies_dict = {}
    for i in cookies_split:
        if i == '':
            continue
        kv = i.split('=')
        cookies_dict[kv[0]] = '='.join(kv[1:])
    return cookies_dict


def add_cookies(driver, cookies):
    for i in cookies:
        driver.add_cookie({'name': i, 'value': cookies[i]})


class Downloader:
    '''
    Main download class
    '''

    def __init__(
            self, manga_url=None, cookies=None, imgdir=None, res=None, sleep_time=1, loading_wait_time=20,
            cut_image=None, file_name_prefix='', number_of_digits=3, start_page=None,
            end_page=None,
            chrome_binary=None,  # 新增：Chrome浏览器路径
            chromedriver_path=None  # 新增：ChromeDriver路径
    ):
        '''
        Initialize parameters
        '''
        
        # GUI传入的新参数
        self.chrome_binary = chrome_binary  # Chrome浏览器路径
        self.chromedriver_path = chromedriver_path  # ChromeDriver路径

        self.manga_url = manga_url
        self.cookies = get_cookie_dict(cookies)
        self.imgdir = imgdir
        self.res = res
        self.sleep_time = sleep_time
        self.loading_wait_time = loading_wait_time
        self.cut_image = cut_image
        self.file_name_model = '/'
        if len(file_name_prefix) != 0:
            self.file_name_model += file_name_prefix + '_'

        self.file_name_model += '%%0%dd.png' % number_of_digits
        self.start_page = start_page - 1 if start_page and start_page > 0 else 0
        self.end_page = end_page
        self.image_box = None

        self.init_function()

    def check_implementation(self, this_manga_url):
        is_implemented_website = False
        for temp_actions_class in WebsiteActions.__subclasses__():
            if temp_actions_class.check_url(this_manga_url):
                is_implemented_website = True
                self.actions_class = temp_actions_class()
                logging.info('Find action class, use %s class.',
                             self.actions_class.get_class_name())
                break

        if not is_implemented_website:
            logging.error('This website has not been added...')
            raise NotImplementedError

    def str_to_data_uri(self, str):
        return ("data:text/plain;charset=utf-8;base64,%s" %
                base64.b64encode(bytes(str, 'utf-8')).decode('ascii'))

    def get_driver(self):
        '''
        Get a webdriver
        '''
        option = uc.ChromeOptions()
        # This is mandatory for Mangafox
        option.add_argument(f'--window-size={self.res[0]},{self.res[1]}')
        
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-extensions')
        option.add_argument('--disable-software-rasterizer')
        option.add_argument('--disable-features=VizDisplayCompositor')
        
        # 如果设置了Chrome路径，则使用指定的路径
        if self.chrome_binary:
            option.binary_location = self.chrome_binary
        
        # 如果设置了ChromeDriver路径，则使用指定的路径
        if self.chromedriver_path:
            self.driver = uc.Chrome(executable_path=self.chromedriver_path, options=option)
        else:
            self.driver = uc.Chrome(options=option)
        self.driver.set_window_size(self.res[0], self.res[1])
        viewport_dimensions = self.driver.execute_script("return [window.innerWidth, window.innerHeight];")
        logging.info('Viewport dimensions %s', viewport_dimensions)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
              Object.defineProperty(navigator, 'webdriver', {
                get: () => false
              })
              window.navigator.chrome = undefined;
              Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
              });
              Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
              });
              const originalQuery = window.navigator.permissions.query;
              window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
              );
            """
        })

    def init_function(self):
        if self.cut_image is not None and self.cut_image != 'dynamic':
            self.left, self.upper, self.right, self.lower = self.cut_image
        self.get_driver()
        random.seed()

    def login(self):
        logging.info('Login...')
        driver = self.driver
        driver.get(self.actions_class.login_url)
        driver.delete_all_cookies()
        add_cookies(driver, self.cookies)
        logging.info('Login finished...')

    def prepare_download(self, this_image_dir, this_manga_url):
        if not os.path.isdir(this_image_dir):
            os.mkdir(this_image_dir)
        logging.info('Loading Book page...')
        driver = self.driver
        driver.get(this_manga_url)
        logging.info('Book page Loaded...')
        logging.info('Preparing for downloading...')
        time.sleep(self.loading_wait_time)

    def download_book(self, this_image_dir):
        driver = self.driver
        logging.info('Run before downloading...')
        self.actions_class.before_download(driver)
        logging.info('Start download...')
        try:
            page_count = self.actions_class.get_sum_page_count(driver)
            logging.info('Has %d pages.', page_count)
            end_page = page_count
            if self.end_page and self.end_page <= page_count:
                end_page = self.end_page
            self.actions_class.move_to_page(driver, self.start_page)

            time.sleep(self.sleep_time)

            for i in range(self.start_page, end_page):
                self.actions_class.wait_loading(driver)
                image_data = self.actions_class.get_imgdata(driver, i + 1)
                with open(this_image_dir + self.file_name_model % i, 'wb') as img_file:
                    if self.cut_image is None:
                        img_file.write(image_data)
                    elif self.cut_image == "dynamic":
                        org_img = pil_image.open(BytesIO(image_data))
                        if self.image_box is None:
                            org_img.load()
                            invert_im = org_img.convert("RGB")
                            invert_im = ImageOps.invert(invert_im)
                            self.image_box = invert_im.getbbox()
                        org_img.crop(self.image_box).save(img_file, format='PNG')
                    else:
                        org_img = pil_image.open(BytesIO(image_data))
                        width, height = org_img.size
                        org_img.crop(
                            (self.left, self.upper, width - self.right, height - self.lower)).save(img_file, format='PNG')

                logging.info('Page %d Downloaded', i + 1)
                if i == page_count - 1:
                    logging.info('Finished.')
                    self.image_box = None
                    return

                self.actions_class.move_to_page(driver, i + 1)

                WebDriverWait(driver, 300).until_not(
                    lambda x: self.actions_class.get_now_page(x) == i + 1)

                time.sleep(self.sleep_time + random.random() * 2)
        except Exception as err:
            with open("error.html", "w", encoding="utf-8") as err_source:
                err_source.write(driver.page_source)
            driver.save_screenshot('./error.png')
            logging.error('Something wrong or download finished,Please check the error.png to see the web page.\r\nNormally, you should logout and login, then renew the cookies to solve this problem.')
            logging.error(err)
            self.image_box = None
            return

    def download(self):
        total_manga = len(self.manga_url)
        total_dir = len(self.imgdir)
        if total_manga != total_dir:
            logging.error('Total manga urls given not equal to imgdir.')
            return

        for i in range(total_manga):
            t_manga_url = self.manga_url[i]
            t_img_dir = self.imgdir[i]
            self.check_implementation(t_manga_url)
            if i == 0:
                self.login()
            logging.info("Starting download manga %d, imgdir: %s",
                         i + 1, t_img_dir)
            self.prepare_download(t_img_dir, t_manga_url)
            self.download_book(t_img_dir)
            logging.info("Finished download manga %d, imgdir: %s",
                         i + 1, t_img_dir)
            time.sleep(2)
        self.driver.close()
        self.driver.quit()
