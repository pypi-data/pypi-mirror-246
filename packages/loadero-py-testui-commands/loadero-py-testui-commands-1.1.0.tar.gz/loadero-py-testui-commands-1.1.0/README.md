# loadero-py-testui-commands [![PyPI - Version](https://img.shields.io/pypi/v/loadero-py-testui-commands)](https://pypi.org/project/loadero-py-testui-commands/)

## Installation

Installation is as simple as adding this line to your requirements.txt
(or equivalent) file.

```bash
loadero-py-testui-commands
```

After which you will be able to install all of the dependencies using pip.

```bash
pip install -r requirements.txt
```

The latest tag always will be the most up-to-date version when compared to the
commands used in the Loadero environment.

## Usage

These Py-TestUI custom commands were made to simplify local script development
for usage in the Loadero environment. By using these commands, you can write your
Loadero script locally and then upload it to Loadero. This also allows for more
rapid development because the script can be debugged and run locally.

To use the commands in your tests, you need to download this dependency to your
project (as shown in above) and then only import the functions in your
script file. Keep in mind, that when migrating the script to Loadero, you do not
need to import the functions there as-well, that will be done automatically.

This is how you can import the functions in your script file:

```py
from commands.receive_email import gen_email, receive_email
from commands.ignore_alert import ignore_alert
from commands.set_file import set_file
from commands.set_request_header import set_request_header
from commands.set_user_agent import set_user_agent
from commands.time_execution import time_execution
from commands.update_network import update_network
from commands.wait_for_download_finished import wait_for_download_finished
```

After which they can be used in your script file as any other function.
Script example:

```py
def test_on_loadero(driver: TestUIDriver):
    really_long_pause = 300
    driver.navigate_to("https://duckduckgo.com/")

    def locate_search_bar():
        e(
            driver, "css", "#searchbox_input"
        ).wait_until_visible().send_keys("QA Processes")
        e(driver, "css", "[aria-label='Search']").wait_until_visible().click()
        e(driver, "css", "#r1-0 > div > h2").wait_until_visible()
        time.sleep(really_long_pause)

    # Example of timing execution without specifying a timeout.
    time_execution("locate_search_bar", locate_search_bar)
```

Not all commands behave the same way as they do in the Loadero environment.
Some of them are modified to work in a local environment, such as
`update_network` and `set_request_header`.

## Commands

The following table shows all available commands and whether there are any
changes to how they function in a local environment.

Full descriptions for how each function behaves in Loadero and their usage can
be found in [Loadero wiki](https://wiki.loadero.com/docs/testui-python/custom-commands/)
page. To see the differences between local and Loadero environment, you can
compare the descriptions in the wiki to the differences mentioned in this README.

| Command                      | Differences                                                                                                                                   |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen_email`                  | Full email or only first part can be provided, if only the first part is provided then `@mailinator.com` is appended                          |
| `ignore_alert`               | No differences                                                                                                                                |
| `receive_email`              | By default an empty array will be returned, but `emails.json` file can be saved in the working directory which will contain all of the emails |
| `set_file`                   | Any local file can be used, Loadero constant can be used if the same file name is used                                                        |
| `set_request_header`         | No request header will be set                                                                                                                 |
| `set_user_agent`             | User agent won't be changed                                                                                                                   |
| `time_execution`             | Execution time will be logged, but not saved                                                                                                  |
| `update_network`             | Network settings will not be updated                                                                                                          |
| `wait_for_download_finished` | Function will finish instantly and not wait for download to be finished                                                                       |

The `emails.json` file should be located in the directory from which you will be
running the tests and should have the following structure:

```json
{
  "emails": [
    {
      "from": "email_from",
      "to": "email_to",
      "headers": {
        "header1": "header_value"
      },
      "subject": "email_subject",
      "text/html": "html body",
      "text/plain": "plain text body"
    }
  ]
}
```

To simulate a more realistic environment, you can modify the `emails.json` file 
mid-run to add additional emails to the array. The file will be read every time
the `receive_email` command is called.
