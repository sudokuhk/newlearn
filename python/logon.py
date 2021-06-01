from selenium import webdriver
from time import sleep
from .base import OwaBase


class OwaLogon(OwaBase):
    def __init__(self, domain_name, ex, owa_version):
        super().__init__(domain_name, ex, owa_version)

    def login(self, username, password):
        print("login: " + self.domain + "/" + username + "<" + password + ">")

        self.find_element_by_id_block("username").send_keys(self.domain + "/" + username)
        self.browser().find_element_by_id("password").send_keys(password)
        self.browser().find_element_by_class_name("signinbutton").click()

        super().login(username)

    def logout(self):
        print("logout")
        if self.owa_version > 2013:
            self.signout_button().click()
        super().logout()

    def open_another_mailbox(self, user):
        # super().open_another_mailbox(user)
        user_email = user + "@" + self.domain_name()

        # Inbox Opened/Mailbox Opened
        self.open_folder(user_email, "mail", "Inbox")
        if user == "SharedMailbox":
            self.open_folder(user_email, "mail", user, 10)
        else:
            self.open_folder(user_email, "mail", user)
        self.open_folder(user_email, "mail", "Inbox")
        # self.open_folder(user_email, "mail", "Drafts")
        # self.open_folder(user_email, "mail", "Deleted Items")
        # self.open_folder(user_email, "mail", "Sent Items")

        self.currentuser = user


def create_owa_logon(domain_name):
    return OwaLogon(domain_name)


def main():
    print('this message is from main function')
    owaLogin = OwaLogon("ca.aws")
    mailbox = owaLogin.login("ex2019", "administrator", "Password123")
    print(mailbox)
    print(chrome.current_window_handle)

    owaLogin.open_another_mailbox("SharedMailbox")
    sleep(10)

    owaLogin.open_another_mailbox("SecondUser")
    sleep(10)

    owaLogin.logout()
    sleep(4)


if __name__ == '__main__':
    main()