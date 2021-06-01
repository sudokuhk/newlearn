from .logon import OwaLogon
from .message import OwaMessage


def create_owa_logon(domainname, ex_server, owa_version):
    print("create_owa_logon: " + domainname)
    return OwaLogon(domainname, ex_server, owa_version)


def login_account(owa_logon, username, password):
    owa_logon.login(username, password)


def open_another_mailbox(owa_logon, username):
    owa_logon.open_another_mailbox(username)


def logout(owa_logon):
    owa_logon.logout()


def close_browser(owa_logon):
    owa_logon.quit()


def create_owa_message(domainname, ex_server, owa_version):
    print("create_owa_message: " + domainname)
    return OwaMessage(domainname, ex_server, owa_version)


def send_message(owa_message, from_, to, subject):
    owa_message.send_message(from_, to, subject)


def read_message(owa_message, mailbox, folder, subject):
    owa_message.read_message(mailbox, folder, subject)


def marked_message_as_unread(owa_message, mailbox, folder, subject):
    owa_message.marked_message_as_unread(mailbox, folder, subject)


def flag_message(owa_message, mailbox, folder, subject):
    owa_message.flag_message(mailbox, folder, subject)


def move_message(owa_message, mailbox, src_folder, dest_folder, subject):
    owa_message.move_message(mailbox, src_folder, dest_folder, subject)


def delete_message(owa_message, mailbox, folder, subject):
    owa_message.delete_message(mailbox, folder, subject)


def empty_folder(owa_message, mailbox, folder):
    owa_message.empty_folder(mailbox, folder)