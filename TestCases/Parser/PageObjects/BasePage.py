from selenium import webdriver

from TestManagement.local_settings import *


class BasePage(object):

    def __init__(self):
        self.driver = webdriver.Firefox()


class JenkinsAcceptancePage(BasePage):

    def __init__(self):
        super(JenkinsAcceptancePage, self).__init__()
        self.driver.get(JENKINS_URL + ACCEPTANCE_URL)
