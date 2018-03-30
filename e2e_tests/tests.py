from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class NewGameTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_new_game(self):
        # User story follows:
        # Alice goes to our app's homepage URI and a page loads
        self.browser.get(self.live_server_url)

        # Alice notices the page title and header mention 'bowling'
        self.assertIn('Bowling', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Bowling', header_text)

        # Alice sees a box to enter the results of her first roll
        inputbox = self.browser.find_element_by_id('id_new_roll')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            ' How many pins did you knock down?'
        )

        # Alice types '4' and hits ENTER. The page updates.
        inputbox.send_keys('4')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Alice notices there are now labels denoting total game score and frame score
        game_score_label = self.browser.find_element_by_id('id_game_score_label').text
        self.assertIn('Game running total score', game_score_label)
        frame_score_label = self.browser.find_element_by_class_name('frame_score_label').text
        self.assertIn('Frame 1 score', frame_score_label)

        # Alice types '5' and hits ENTER. The page updates and displays '9' next to 'frame score'.
        inputbox = self.browser.find_element_by_id('id_new_roll')
        inputbox.send_keys('5')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        game_score = self.browser.find_element_by_id('id_game_score').text
        self.assertEquals(game_score, '9')