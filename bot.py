# standard library imports
import time
import os
import sys
from pathlib import Path
import http.client as httplib

# related third party imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# local application/library specific imports
import constants as c
from util import split_birthday


class ValidateWebPage:
    # This class control the automation practice web page validation
    def __init__(self, url, user_profile):
        """
        Constructor to initialize the Class
        :param url: Web page url
        :param user_profile: User class
        """
        self.url = url
        self.abs_path = os.path.abspath(os.path.dirname(__file__))
        self.downloads_path = str(os.path.join(Path.home(), "Downloads"))
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": self.downloads_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # Set the webdriver for chrome
        self.browser = webdriver.Chrome(
            executable_path=self.resource_path(c.CHROME_DRIVER),
            chrome_options=options
        )

        self.browser.maximize_window()
        self.browser.get(self.url)
        self.user = user_profile

    def wait_until_presence_of_element_by_xpath(self, xpath):
        """
        Wait until the xpath element is visible
        :param xpath: xpath element to find in the web page
        :return:
        """
        WebDriverWait(self.browser, 60).until(ec.presence_of_element_located((By.XPATH, xpath)))

    def load_login_page(self):
        """
        Click to log in button
        :return:
        """
        WebDriverWait(self.browser, 60).until(ec.presence_of_element_located((By.NAME, c.SEARCH_QUERY)))
        self.browser.find_element(By.CLASS_NAME, c.LOGIN).click()

    def validate_email(self):
        """
        Access to log in section, write the email and press the submit function to validate the email
        and continue with the creation account
        :return:
        """
        self.load_login_page()
        WebDriverWait(self.browser, 60).until(ec.presence_of_element_located((By.NAME, c.SUBMIT_CREATE)))
        self.fill_field_by_id(c.EMAIL_CREATE, self.user.email)
        self.browser.find_element(By.NAME, c.SUBMIT_CREATE).click()

    def fill_field_by_id(self, id, field_value):
        """
        Fill HTML field using ID
        :return:
        """
        self.browser.find_element(By.ID, id).send_keys(field_value)

    def click_element_by_id(self, id):
        """
        Click in HTML element using ID
        :return:
        """
        self.browser.find_element(By.ID, id).click()

    def click_element_by_name(self, name):
        """
        Click in HTML element using ID
        :return:
        """
        self.browser.find_element(By.NAME, name).click()

    def click_element_by_xpath(self, name):
        """
        Click in HTML element using xpath
        :return:
        """
        self.browser.find_element(By.XPATH, name).click()

    def fill_account_fields(self):
        """
        Fill all the fields for the user account creation
        :return:
        """
        WebDriverWait(self.browser, 60).until(ec.presence_of_element_located((By.NAME, c.FIRST_NAME)))

        # Select user gender
        if self.user.gender == "mr":
            self.click_element_by_id(c.MR)
        else:
            self.click_element_by_id(c.MRS)

        # ---Start to fill first section about personal information---
        self.fill_field_by_id(c.CUSTOMER_FIRSTNAME, self.user.first_name)
        self.fill_field_by_id(c.CUSTOMER_LASTNAME, self.user.last_name)
        self.fill_field_by_id(c.PASSWORD, self.user.password)

        # Get Date elements and fill the Birthday elements
        year, month, day = split_birthday(self.user.birthday)
        self.fill_field_by_id(c.YEAR, year)
        self.fill_field_by_id(c.MONTH, month)
        self.fill_field_by_id(c.DAY, day)

        if self.user.sing_up:
            self.click_element_by_id(c.SING_UP)
            time.sleep(5)

        if self.user.receive_info:
            self.click_element_by_id(c.RECEIVE_INFO)
            time.sleep(5)

        # ---End to fill first section about personal information---

        # Dictionary to store the basic Fields and Values
        basic_fields = {
            c.FIRST_NAME: self.user.first_name,
            c.LAST_NAME: self.user.last_name,
            c.COMPANY: self.user.company,
            c.ADDRESS_ONE: self.user.address_one,
            c.ADDRESS_TWO: self.user.address_two,
            c.CITY: self.user.city,
            c.STATE: self.user.state,
            c.POST_CODE: self.user.post_code,
            c.COUNTRY: self.user.country,
            c.ADDITIONAL_INFO: self.user.additional_info,
            c.PHONE: self.user.phone,
            c.PHONE_MOBILE: self.user.phone_mobile,
            c.ALIAS: self.user.alias
        }

        # Fill the basic fields
        for key, value in basic_fields.items():
            self.fill_field_by_id(key, value)

        # Click in submit button to complete the account creation
        self.click_element_by_id(c.SUBMIT_ACCOUNT)

        time.sleep(40)

    def create_account(self):
        """
        This function create a new user account
        :return:
        """
        self.validate_email()
        self.fill_account_fields()

    def open_t_shirt_section(self):
        """
        This function open t-shirt section
        :return:
        """
        self.click_element_by_xpath(c.T_SHIRTS_SECTION_XPATH)

    def open_dresses_section(self):
        pass

    def open_women_section(self):
        pass

    def open_cart(self):
        """
        This function open the cart
        :return
        """
        self.browser.find_element(By.XPATH, c.OPEN_CART_BUTTON_XPATH).click()

    def sign_out(self):
        self.click_element_by_xpath(c.SING_OUT_ACCOUNT)
        time.sleep(15)

    def add_item_to_cart(self):
        self.open_t_shirt_section()
        self.click_element_by_xpath(c.PRODUCT_XPATH)

        time.sleep(5)
        self.click_element_by_xpath(c.ADD_TO_CART_XPATH)

        time.sleep(5)
        self.click_element_by_xpath(c.CLOSE_BUTTON_XPATH)
        time.sleep(9)

    def check_out(self):
        self.open_cart()
        self.click_element_by_xpath(c.CHECKOUT_BUTTON_XPATH)
        time.sleep(3)
        self.click_element_by_name(c.PROCESS_ADDRESS)
        time.sleep(3)
        self.click_element_by_id(c.TERMS_OF_USE)
        time.sleep(3)
        self.click_element_by_name(c.PROCESS_CARRIER)
        time.sleep(3)
        self.click_element_by_xpath(c.BANK_WIRE)
        time.sleep(3)
        self.click_element_by_xpath(c.CONFIRM_ORDER)
        time.sleep(5)

    def sign_in(self):
        self.load_login_page()
        self.fill_field_by_id(c.EMAIL, self.user.email)
        self.fill_field_by_id(c.PASSWORD, self.user.password)
        self.click_element_by_id(c.SUBMIT_LOGIN)
        time.sleep(10)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

    def have_internet(self):
        conn = httplib.HTTPConnection("www.google.com", timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except:
            conn.close()
            return False