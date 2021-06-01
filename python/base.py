from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class OwaBase:
    def __init__(self, domainname, ex, owa_version):
        self.webdriver = self.__create_chrome_driver()

        split_str = domainname.split('.', 1)
        self.domainname = domainname
        self.domain = split_str[0]
        self.islogin = False
        self.loginuser = ""
        self.currentuser = ""
        self.ex_server = ex
        self.loginuser_email = ""
        self.owa_version = owa_version

        url = "https://" + self.ex_server + "/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2f" + self.ex_server + "%2fowa"
        # url = "https://" + self.ex_server + "/owa/"
        self.browser().get(url)

    def avtar_button(self):
        paths = [
            "//div[contains(@class,'ms-Icon--person')]",
            "..//..//.."
        ]
        return self.find_element_by_xpath_block(paths)
        # div = self.webdriver.find_element_by_xpath("//div[contains(@class,'ms-Icon--person')]")
        # return div.find_element_by_xpath('..//..//..')

    def signout_button(self):
        return self.__find_button_from_avtar("Sign out")

    def __open_another_mailbox_button(self):
        return self.__find_button_from_avtar("Open another mailbox")

    def __close_all_other_windows(self, driver):
        current_window = driver.current_window_handle
        allwindows = driver.window_handles

        for win in allwindows:
            if win != current_window:
                driver.switch_to_window(win)
                driver.close()

        driver.switch_to_window(current_window)
        driver.refresh()

    def open_another_mailbox_1(self, user):  # user@domain
        mail_address = user + "@" + self.domainname
        print("open another mailbox: " + mail_address)

        self.__close_all_other_windows(self.webdriver)

        button = self.__open_another_mailbox_button()
        button.click()

        paths = [
            "//input[contains(@class, 'hideClearButton')]",
        ]
        email_input = self.find_element_by_xpath_block(paths)
        email_input.send_keys(mail_address)
        # email_input.send_keys(Keys.ENTER)

        paths = [
            "//span[contains(text(), 'Search Directory')]",
        ]
        self.find_element_by_xpath_block(paths) # check the 'Search Directory' item popup

        paths = [
            "//span[text()='" + user + "']",
        ]
        self.find_element_by_xpath_block(paths)

        paths = [
            "//span[text()='Open']",
            ".."
        ]
        self.find_element_by_xpath_block(paths).click()
        self.currentuser = user

    def __find_button_from_avtar(self, text, count=60):
        while True:
            count = count - 1
            try:
                avtar = self.avtar_button().click()
                print(avtar)

                paths = [
                    "//span[contains(text(),'" + text + "')]",
                    "../.."
                ]
                return self.find_element_by_xpath(paths)
            except BaseException as e:
                print("do not found element: " + text)
                if count == 0:
                    print("__find_button_from_avtar, do not found. current url:<" + self.current_url() + ">")
                    raise e
                sleep(1)

    def find_element_by_xpath(self, paths):
        element = self.webdriver
        for path in paths:
            element = element.find_element_by_xpath(path)
        #print(element)
        return element

    def find_element_by_xpath_no_exception(self, paths):
        print("find_element_by_xpath_no_exception ---> ")
        print(paths)
        try:
            return self.find_element_by_xpath(paths)
        except BaseException:
            print("find_element_by_xpath_no_exception, do not found. current url:<" + self.current_url() + ">")
            return None

    def find_element_by_xpath_block(self, paths, count=60):
        print("find_element_by_xpath_block ---> ")
        print(paths)
        while True:
            try:
                return self.find_element_by_xpath(paths)
            except NoSuchElementException as e:
                print("do not found element: ")
                sleep(1)
                count = count - 1
                if count == 0:
                    print("find_element_by_xpath_block, do not found. current url:<" + self.current_url() + ">")
                    raise e

    def find_element_by_id_block(self, name):
        print("find_element_by_id_block ---> ")
        print(name)
        count = 120
        while True:
            try:
                return self.webdriver.find_element_by_id(name)
            except BaseException as e:
                print("do not found element by id: ")
                sleep(1)
                count = count - 1
                if count == 0:
                    print("find_element_by_id_block, do not found. current url:<" + self.current_url() + ">")
                    raise e

    def is_login(self):
        return self.islogin

    def login_user(self):
        return self.loginuser

    def current_user(self):
        return self.currentuser

    def domain_name(self):
        return self.domainname;

    def login(self, user):
        self.islogin = True
        self.loginuser = user
        self.currentuser = user
        self.loginuser_email = user + "@" + self.domain_name()

    def logout(self):
        self.loginuser = ""
        self.currentuser = ""
        self.islogin = False

    def browser(self):
        return self.webdriver

    def quit(self):
        try:
            self.webdriver.quit()
        except:
            print("quit")

    def get_url(self, url, tries=3):
        while True:
            self.webdriver.get(url)
            sleep(5)

            try:
                self.find_element_by_xpath_block(["//div[text()='Something went wrong']"], 5)
            except:
                return

            tries = tries - 1
            if tries <= 0:
                raise Exception('get url failed')


    def current_url(self):
        return self.webdriver.current_url;

    def __create_chrome_driver(self):
        # driver_file = r'C:\SeleniumDriver\geckodriver.exe'
        # firefox_options = webdriver.ChromeOptions()
        # firefox_options.add_argument("--headless")
        # firefox_options.add_argument("--disable-gpu")
        # firefox_options.add_argument("--disable-images")
        # web_driver = webdriver.Chrome(options=firefox_options)
        web_driver = webdriver.Chrome()

        web_driver.set_window_size(800, 600)
        web_driver.maximize_window()

        return web_driver

    def open_url(self, user_email, feature):
        current_url = self.current_url().lower()
        print("current_url:<" + current_url + ">")

        url = "https://" + self.ex_server + "/owa/" + user_email + "/?offline=disabled#path=/" + feature
        url = url.lower()
        keyword = "/owa/" + user_email + "/?offline=disabled#path=/"

        if self.loginuser_email.lower() == user_email.lower():
            if "owa/#path" in current_url or keyword in current_url:
                print("owner user, do not reopen")
            else:
                print("owner open_url: get url:<" + url + ">")
                self.get_url(url)
        elif keyword.lower() in current_url:
            print("open_url: current url is:<" + current_url + ">, do not reopen")
        else:
            print("open_url: get url:<" + url + ">")
            self.get_url(url)

    def open_folder(self, user_email, feature, folder, wait=3):
        print("open folder: <" + user_email + ">, <" + feature + ">, <" + folder + ">")
        self.open_url(user_email, feature)

        element = self.find_element_by_xpath_block(["//span[contains(text(),'" + folder + "') and @title='" + folder + "']"])
        ActionChains(self.browser()).click(element).perform()

        print("after open folder, current_url:<" + self.current_url() + ">")
        sleep(wait)

        return element



