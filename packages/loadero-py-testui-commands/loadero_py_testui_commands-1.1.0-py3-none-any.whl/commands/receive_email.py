import json

from testui.support.testui_driver import TestUIDriver
from testui.elements.testui_element import testui_error


def receive_email(driver: TestUIDriver, address: str) -> [] or None:
    if not address:
        testui_error(driver, "[ERROR] Loadero: No email address provided")
        return
    
    try:
        f = open("emails.json")
        data = json.load(f)

        return data["emails"]
    except OSError:
        return []


def gen_email(address: str) -> str:
    if "@" in address:
        return address

    return f"{address}@mailinator.com"
