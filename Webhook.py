from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

'''
    This program is a replacement for the built-in trigger
    for Jenkins when you push to your github repository.

    You need to fill in the following rows to get the program running correctly:
    31, 44, 84
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
        bot.get('github URL')

    def refresh_github(self):
        self.bot.refresh()

    def get_commit(self):
        find_commit = self.bot.find_element_by_xpath('/html/body/div[4]/div/main/div[2]/div/div[2]/ul/li[1]/a/span')
        string_commit = find_commit.get_attribute('innerText')
        commit = int(string_commit)
        return commit

    ''' Fill in your desired jenkins server URL in the get method that you want to use '''
    def login_jenkins(self):
        self.j_bot.get('Jenkins login page')
        email = self.j_bot.find_element_by_id('j_username')
        password = self.j_bot.find_element_by_xpath('/html/body/div/div/form/div[3]/input')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

    def build_jenkins(self):
        ssrs_infotiv = self.j_bot.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[2]/table/tbody/tr[43]/td[3]/a')
        ssrs_infotiv.click()
        build = self.j_bot.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[4]/a[2]')
        build.click()

    def close_jenkins(self):
        self.j_bot.close()

    def run_webhook(self):
        self.goto_github()
        time.sleep(3)
        counter = 0
        while True:
            self.refresh_github()
            time.sleep(600) # How often github refreshes (600 = 10 minutes)
            commit = self.get_commit()

            if commit > counter:
                self.login_jenkins()
                self.build_jenkins()
                self.j_bot.close()
                counter = commit
                print(counter)
            else:
                print('Refreshed: No builds were made this time.')



''' Fill in your username and your password for your Jenkins login '''

webhook = Webhook('username', 'password')
webhook.run_webhook()
