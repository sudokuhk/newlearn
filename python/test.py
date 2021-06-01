from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

class OwaBase:
    def __init__(self, webdriver):
        self.webdriver = webdriver

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
				
    def open_another_mailbox(self, mail_address):
        print("open another mailbox")
        
        self.__close_all_other_windows(self.webdriver)
        
        button = self.__open_another_mailbox_button()
        button.click()

        paths = [
            "//input[contains(@class, 'hideClearButton')]",
        ]
        email_input = self.find_element_by_xpath_block(paths)
        email_input.send_keys(mail_address)
        #email_input.send_keys(Keys.ENTER)

        paths = [
            "//span[contains(text(), 'Search Directory')]",
            ]
        self.find_element_by_xpath_block(paths)
        email_input.send_keys(Keys.ENTER)

        paths = [
            "//span[text()='Open']",
            ".."
            ]
        self.find_element_by_xpath_block(paths).click()

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
        return element

    def find_element_by_xpath_block(self, paths):
        while True:
            try:
                return self.find_element_by_xpath(paths)
            except BaseException:
                print("do not found element: ")
                print(paths)
                sleep(1)



class OwaLogon(OwaBase):
    def __init__(self, webdriver):
        super().__init__(webdriver)

    def login(self, machine, domain, username, password):
        print("login: " + domain + "/" + username + "<" + password + ">")
        url = "https://" + machine + "/owa/"
        self.webdriver.get(url)

        self.webdriver.find_element_by_id("username").send_keys(domain + "/" + username)
        self.webdriver.find_element_by_id("password").send_keys(password)
        self.webdriver.find_element_by_class_name("signinbutton").click()

    def logout(self):
        print("logout")
        self.signout_button().click()

def create_chrome_driver():
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

def main(chrome):
    print('this message is from main function')
    owaLogin = OwaLogon(chrome)
    mailbox = owaLogin.login("ex2019", "ca", "administrator", "Password123")
    print(mailbox)
    print(chrome.current_window_handle)

    owaLogin.open_another_mailbox("SharedMailbox@ca.aws")
    sleep(4)

    owaLogin.open_another_mailbox("SecondUser@ca.aws")
    sleep(4)
    
    owaLogin.logout()
    sleep(4)

    chrome.quit()

if __name__ == '__main__':
    chrome = create_chrome_driver()
    main(chrome)
                                                 
