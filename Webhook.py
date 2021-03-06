from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

'''
    This program is a replacement for the built-in trigger
    for Jenkins when you push to your github repository.

    You need to fill in the following rows to get the program running correctly:
    32, 48, 58, 102
'''


class Webhook:
    def __init__(self, username, password):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        #self.bot = webdriver.Chrome()
        self.bot = webdriver.Chrome(options=options) # Headlesschrome
        #self.j_bot = webdriver.Chrome()
        self.j_bot = webdriver.Chrome(options=options) # Headlesschrome
        self.username = username
        self.password = password

    ''' Fill in your desired github repository in the get method that you want to use '''
    def goto_github(self):
        bot = self.bot
        bot.get('Github URL') # Insert the URL to your Github repo

    def refresh_github(self):
        self.bot.refresh()

    def refresh_jenkins(self):
        self.j_bot.refresh()

    def get_commit(self):
        find_commit = self.bot.find_element_by_class_name('num.text-emphasized')
        string_commit = find_commit.get_attribute('innerText')
        commit = int(string_commit)
        return commit

    ''' Fill in your desired jenkins server URL in the get method that you want to use '''
    def login_jenkins(self):
        self.j_bot.get('Jenkins Login URL') # Insert the URL to your Jenkins
        email = self.j_bot.find_element_by_id('j_username')
        password = self.j_bot.find_element_by_xpath("//input[@placeholder='Password']")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

    def pipeline_jenkins(self):
        pipeline_name = "" # Insert the name of your pipeline between the quotation marks
        self.j_bot.find_element_by_css_selector("a[href*='job/" + pipeline_name + "']").click()

    def build_jenkins(self):
        build = self.j_bot.find_element_by_class_name('task-link')
        build.click()

    def check_builds(self):
        try:
            self.j_bot.find_element_by_class_name('progress-bar-left')
        except NoSuchElementException:
            return False
        return True

    def close_jenkins(self):
        self.j_bot.close()

    def run_webhook(self):
        time.sleep(3)
        self.goto_github()
        time.sleep(2)
        self.login_jenkins()
        time.sleep(2)
        self.pipeline_jenkins()
        counter = self.get_commit()
        while True:
            self.refresh_github()
            time.sleep(15) # How often github refreshes (600 = 10 minutes)
            commit = self.get_commit()
            check = self.check_builds()
            if commit > counter:
                if check == True:
                    print('There are new commits, but Jenkins is already building')
                else:
                    self.build_jenkins()
                    counter = commit
                    print('Building commit number ' + str(counter))
            else:
                print('Refreshed github: Nothing to build.')



''' Fill in your username and your password for your Jenkins login '''

webhook = Webhook('username', 'password') # Insert your username and password to Jenkins
webhook.run_webhook()
