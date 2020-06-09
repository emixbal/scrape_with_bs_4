from __future__ import print_function
import argparse
import mechanicalsoup
from getpass import getpass

parser = argparse.ArgumentParser(description="Login to DumbWays.")
# parser.add_argument("email")
args = parser.parse_args()
args.email = getpass("Please enter your DumbWays email: ")
args.password = getpass("Please enter your DumbWays password: ")

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='MyBot/0.1: mysite.example.com/bot_info',
)
# Uncomment for a more verbose output:
# browser.set_verbose(2)

browser.open("yourtargeturl.com/")
browser.follow_link("sign_in")
browser.select_form("#new_user")
browser["user[email]"] = args.email
browser["user[password]"] = args.password
resp = browser.submit_selected()

# Uncomment to launch a web browser on the current page:
browser.launch_browser()

# verify we are now logged in
page = browser.get_current_page()
messages = page.find("div", class_="flash-messages")
if messages:
    print(messages.text)
assert page.select(".logout-form")

print(page.title.text)

# verify we remain logged in (thanks to cookies) as we browse the rest of
# the site
page3 = browser.open("https://github.com/MechanicalSoup/MechanicalSoup")
assert page3.soup.select(".logout-form")
