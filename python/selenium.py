from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from enum import Enum


class OwaBase:
    def __init__(self, domainname):
        self.webdriver = self.__create_chrome_driver()

        split_str = domainname.split('.', 1)
        self.domainname = domainname
        self.domain = split_str[0]
        self.islogin = False
        self.loginuser = ""
        self.currentuser = ""

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

    def open_another_mailbox(self, user):  # user@domain
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

    def __find_button_from_avtar(self, text):
        while True:
            try:
                avtar = self.avtar_button().click()
                print(avtar)

                paths = [
                    "//span[contains(text(),'" + text + "')]",
                    "../.."
                ]
                return self.find_element_by_xpath(paths)
            except BaseException:
                print("do not found element: " + text)
                sleep(1)

    def find_element_by_xpath(self, paths):
        element = self.webdriver
        for path in paths:
            element = element.find_element_by_xpath(path)
        print(element)
        return element

    def find_element_by_xpath_no_exception(self, paths):
        print("find_element_by_xpath_no_exception ---> ")
        print(paths)
        try:
            return self.find_element_by_xpath(paths)
        except BaseException:
            print("find_element_by_xpath_no_exception, do not found.")
            return None

    def find_element_by_xpath_block(self, paths):
        print("find_element_by_xpath_block ---> ")
        print(paths)
        while True:
            try:
                return self.find_element_by_xpath(paths)
            except BaseException:
                print("do not found element: ")
                print(paths)
                sleep(1)

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

    def logout(self):
        self.loginuser = ""
        self.currentuser = ""
        self.islogin = False

    def browser(self):
        return self.webdriver

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


class OwaLogon(OwaBase):
    def __init__(self, domain_name):
        super().__init__(domain_name)

    def login(self, machine, username, password):
        print("login: " + self.domain + "/" + username + "<" + password + ">")
        url = "https://" + machine + "/owa/"
        self.browser().get(url)

        self.browser().find_element_by_id("username").send_keys(self.domain + "/" + username)
        self.browser().find_element_by_id("password").send_keys(password)
        self.browser().find_element_by_class_name("signinbutton").click()

        super().login(username)
        # mailbox open
        #msgfolder = "https://ex2019/owa/" + username + "@" + self.domain_name() + "/?offline=disabled#path=/mail/msgfolderroot"
        #self.browser().get(msgfolder)
        
    def logout(self):
        print("logout")
        self.signout_button().click()
        super().logout()

    def open_another_mailbox(self, user):
        super().open_another_mailbox(user)

        # mailbox open
        msgfolder = "https://ex2019/owa/" + user + "@" + self.domain_name() + "/?offline=disabled#path=/mail/msgfolderroot"
        print("open msgfloder:" + msgfolder)
        self.browser().get(msgfolder)


class OwaMessage(OwaLogon):
    def __init__(self, domainname):
        super().__init__(domainname)

    def create_message(self, to, subject):
        browser = self.browser()
        print("create message, To<" + to + ">, Subject<" + subject + ">")
        mail_address = "https://ex2019/owa/" + self.current_user() + "@" + self.domain_name() + "/?offline=disabled#path=/mail/inbox"
        print("mail address: " + mail_address);

        print("current url: " + browser.current_url)
        browser.get(mail_address)
        print("new url: " + browser.current_url)

        # must maximize window
        self.find_element_by_xpath_block(["//span[text()='New']", "..//.."]).click()
        self.find_element_by_xpath_block(["//input[@aria-label='To']"]).send_keys(to + "@" + self.domain_name())
        self.find_element_by_xpath_block(["//span[contains(text(), 'Use this address:')]", ".."]).click()
        self.find_element_by_xpath_block(["//input[@placeholder='Add a subject']"]).send_keys(subject)
        self.find_element_by_xpath_block(["//button[@aria-label='Send']"]).click()

    def delete_message(self, subject):
        print("delete message")

    def clear_folder(self, folder):
        print("clear folder: " + folder)

        self.find_element_by_xpath_block(["//span[contains(text(), '" + folder + "')]"]).click()

        checkbox = self.find_element_by_xpath_block(["//button[@role = 'checkbox']"])
        print(checkbox)
        checkbox.click()

def create_owa_logon(domain_name):
    return OwaLogon(domain_name)

def main():
    print('this message is from main function')
    #owaLogin = OwaMessage("ca.aws")
    #mailbox = owaLogin.login("ex2019", "administrator", "Password123")
    #print(mailbox)
    #owaLogin.logout()
    #sleep(4)

    owaMessage = OwaMessage("ca.aws")
    owaMessage.login("ex2019", "administrator", "Password123")
    #owaMessage.create_message("administrator", "This is a test")

    #sleep(4)
    owaMessage.clear_folder("Sent Items")

    #owaLogin.open_another_mailbox("SharedMailbox")
    #sleep(10)

    #owaLogin.open_another_mailbox("SecondUser")
    #sleep(10)

    #owaLogin.logout()
    sleep(30)

if __name__ == '__main__':
    main()
