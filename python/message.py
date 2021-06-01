from selenium import webdriver
from time import sleep
from .logon import OwaLogon
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class OwaMessage(OwaLogon):
    def __init__(self, domainname, ex_server, owa_version):
        super().__init__(domainname, ex_server, owa_version)

    def send_message(self, from_, to, subject):
        self.open_folder(from_, "mail", "Inbox")

        # must maximize window
        if self.owa_version > 2013:
            self.find_element_by_xpath_block(["//span[text()='New']", "..//.."]).click()
            self.find_element_by_xpath_block(["//input[@aria-label='To']"]).send_keys(to)
            self.find_element_by_xpath_block(["//span[contains(text(), 'Use this address:')]", ".."]).click()
            self.find_element_by_xpath_block(["//input[@placeholder='Add a subject']"]).send_keys(subject)
        else:
            self.find_element_by_xpath_block(["//span[contains(text(),'New mail')]", "..//.."]).click()
            self.find_element_by_xpath_block(["//input[starts-with(@aria-label,'To')]"]).send_keys(to)
            self.find_element_by_xpath_block(["//span[contains(text(), 'Use this address:')]", ".."]).click()
            self.find_element_by_xpath_block(["//input[@aria-labelledby='MailCompose.SubjectWellLabel']"]).send_keys(
                subject)
        self.find_element_by_xpath_block(["//button[@aria-label='Send']"]).click()

    def read_message(self, user_email, folder, subject):
        print("read_message")
        self.marked_message_as_read(user_email, folder, subject)

    def __get_item_from_menu(self, user_email, folder, subject, itemname, count=10):  # max wait 1min
        while True:
            try:
                self.open_folder(user_email, "mail", folder, 5)

                path = [
                    "//span[contains(text(),'" + subject + "')]",
                    "..//..//..//.."
                ]
                email = self.find_element_by_xpath_block(path, 3)
                print(email.get_attribute('textContent'))
                ActionChains(self.browser()).move_to_element(email)
                ActionChains(self.browser()).click(email).perform()
                ActionChains(self.browser()).context_click(email).perform()

                print("get context menu")
                menu = self.find_element_by_xpath_block(["//div[@aria-label='Context menu']"], 3)
                content = menu.get_attribute('textContent')
                print(content)

                print("get item:<" + itemname + ">")
                item = menu.find_element_by_xpath(".//span[contains(text(),'" + itemname + "')]")
                return item, content

            except Exception as e:
                print(e)
                print("do not found email:<" + subject + ">, retry")
                count = count - 1

                if count <= 0:
                    print("do not found email for max tries")
                    raise e
                self.browser().refresh()

    def is_read(self, user_email, folder, subject):
        item, content = self.__get_item_from_menu(user_email, folder, subject, 'Mark as unread', 1)

        if 'Mark as unread' in content:
            return False
        else:
            return True

    def marked_message_as_unread(self, user_email, folder, subject):
        print("marked_message_as_unread")
        if self.is_read(user_email, folder, subject):
            self.marked_message(user_email, folder, subject, False)
        self.marked_message(user_email, folder, subject, True)

    def marked_message_as_read(self, user_email, folder, subject):
        print("marked_message_as_read")
        if not self.is_read(user_email, folder, subject):
            self.marked_message(user_email, folder, subject, True)
        self.marked_message(user_email, folder, subject, False)

    def marked_message(self, user_email, folder, subject, unread):
        if unread:
            item, content = self.__get_item_from_menu(user_email, folder, subject, 'Mark as unread')
            ActionChains(self.browser()).click(item).perform()
        else:
            item, content = self.__get_item_from_menu(user_email, folder, subject, 'Mark as read')
            ActionChains(self.browser()).click(item).perform()

    def flag_message(self, user_email, folder, subject):
        item, content = self.__get_item_from_menu(user_email, folder, subject, 'Flag')
        ActionChains(self.browser()).click(item).perform()

    def move_message(self, user_email, src_folder, dest_folder, subject):
        print("move message<" + user_email + "> from <" + src_folder + "> To <" + dest_folder + ">")

        item, content = self.__get_item_from_menu(user_email, src_folder, subject, 'Move')
        ActionChains(self.browser()).click(item).perform()

        if self.owa_version > 2013:
            move = self.find_element_by_xpath_block(["//span[contains(text(), 'Move to a different folder...')]"])
            ActionChains(self.browser()).click(move).perform()

        paths = [
            "//span[contains(text(), 'Move 1 conversation')]//..//..",
            ".//span[contains(text(), '" + dest_folder + "')]",
        ]
        delete = self.find_element_by_xpath_block(paths)
        ActionChains(self.browser()).click(delete).perform()

        paths = [
            "//span[text()='Move']",
            "..",
        ]
        btn_move = self.find_element_by_xpath_block(paths)
        btn_move.click()

        self.browser().refresh()

    def delete_message(self, user_email, folder, subject):
        print("delete message<" + user_email + "> from <" + folder + ">")

        item, content = self.__get_item_from_menu(user_email, folder, subject, 'Delete')
        ActionChains(self.browser()).click(item).perform()

        try:
            paths = [
                "//span[text()='OK']",
                "..",
            ]

            btn_ok = self.find_element_by_xpath_block(paths, 3)
            btn_ok.click()
            self.browser().refresh()
        except:
            print("delete_message, no need to confirm")

    def empty_folder(self, user_email, folder):
        print("empty_folder: " + folder)

        element = self.open_folder(user_email, "mail", folder)
        ActionChains(self.browser()).context_click(element).perform()

        paths = [
            "//div[@aria-label='Context menu']",
            ".//span[contains(text(),'Empty folder')]",
        ]
        menu_empty = self.find_element_by_xpath_block(paths)
        ActionChains(self.browser()).click(menu_empty).perform()

        paths = [
            "//span[text()='OK']",
            "..",
        ]

        btn_ok = self.find_element_by_xpath_block(paths)
        btn_ok.click()

        self.browser().refresh()


