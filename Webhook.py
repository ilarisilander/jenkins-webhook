from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

'''
    This program is a replacement for the built-in trigger
    for Jenkins when you push to your github repository.

    You need to fill in the following rows to get the program running correctly:
    32, 48, 64, 109
'''


class Webhook:
    def __init__(self, username, password):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        #self.bot = webdriver.Chrome()                 # Not headlesschrome
        self.bot = webdriver.Chrome(options=options)   # Headlesschrome
        #self.j_bot = webdriver.Chrome()               # Not headlesschrome
        self.j_bot = webdriver.Chrome(options=options) # Headlesschrome
        self.username = username
        self.password = password

    ''' Fill in your desired github repository in the get method that you want to use '''
    def goto_github(self):
        bot = self.bot
        bot.get('Your Github URL')

    def refresh_github(self):
        self.bot.refresh()

    def refresh_jenkins(self):
        self.j_bot.refresh()

    def get_commit(self):
        find_commit = self.bot.find_element_by_xpath('/html/body/div[4]/div/main/div[2]/div/div[2]/ul/li[1]/a/span')
        string_commit = find_commit.get_attribute('innerText')
        commit = int(string_commit)
        return commit

    ''' Fill in your desired jenkins server URL in the get method that you want to use '''
    def login_jenkins(self):
        self.j_bot.get('Your Jenkins URL')
        email = self.j_bot.find_element_by_id('j_username')
        password = self.j_bot.find_element_by_xpath('/html/body/div/div/form/div[3]/input')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

    def pipeline_jenkins(self):
        '''
            This is where you fill in your xpath to the pipeline in your landing page on Jenkins after login.
            To find your full xpath: In Google Chrome -> Jenkins website -> press F12 -> use select item (shift + ctrl + C) ->
            find your pipeline -> click on it -> on the right side, you have now html code with the element selected ->
            right click on it and choose "Copy" -> "Copy full xpath" -> paste it here as an argument
        '''
        ssrs_infotiv = self.j_bot.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[2]/table/tbody/tr[43]/td[3]/a')
        ssrs_infotiv.click()

    def build_jenkins(self):
        build = self.j_bot.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[4]/a[2]')
        build.click()

    def check_builds(self):
        try:
            self.j_bot.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div[2]/table/tbody/tr/td[2]')
        except NoSuchElementException:
            return False
        return True

    def close_jenkins(self):
        self.j_bot.close()

    def run_webhook(self):
        input_counter = input('Current commit amount: ')
        time.sleep(3)
        self.goto_github()
        time.sleep(2)
        self.login_jenkins()
        time.sleep(2)
        self.pipeline_jenkins()
        counter = int(input_counter)
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

webhook = Webhook('username', 'password')
webhook.run_webhook()
