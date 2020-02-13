from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import os, sys

# download_path = 'C:\\Users\\gaurav.khatri\\Downloads\\Songs'
# ------------------------
if len(sys.argv) > 1:
    default_folder_name = sys.argv[1]
else:
    default_folder_name = 'Songs'
final_path = 'C:\\Users\\gaurav.khatri\\Downloads'
download_path = os.path.join(final_path, default_folder_name)

if not os.path.exists(download_path):
    os.mkdir(download_path)

# -----------------------
# Global arguments for avoiding Show notification popups
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,
    "download.default_directory": download_path
})


def check_download_completion(wait=False):
    # download_path = "C:/Users/gaurav.khatri/Downloads"
    input_flag = False
    for filename in os.listdir(download_path):
        if ".crdownload" in filename:
            print('Temp file found')
            wait = True
            time.sleep(15)
    input_flag = wait
    # print('*** Download complete *** ')
    return input_flag


class download_bot():
    def __init__(self, song, valid_link=None):
        self.driver = webdriver.Chrome(options=option)
        self.song = song
        self.valid_link = valid_link

    def get_link(self):
        self.driver.get('https://www.youtube.com/')
        search_button = self.driver.find_element_by_xpath('//*[@id="search"]')
        search_button.send_keys(song)

        click_button = self.driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
        click_button.click()

        # Getting the links of videos
        time.sleep(7.7)
        link = self.driver.find_elements_by_id("video-title")
        empty_list = []
        for x in link:
            j = str(x.get_attribute("href"))
            empty_list.append(j)

        self.valid_link = [link for link in empty_list if 'www.youtube.com/watch?' in link][0]

    def mp3site(self):
        self.driver.get("https://ytmp3.cc/en12/")
        searcher = self.driver.find_element_by_xpath('//*[@id="input"]')
        searcher.send_keys(self.valid_link)
        print('data enterred')

        clicker = self.driver.find_element_by_id("submit")
        clicker.click()
        time.sleep(15.5)

        download_button = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/a[1]')
        download_button.click()
        time.sleep(4)

    def close_session(self):
        print('Current download Completed ')
        self.driver.close()


def song_file_reader():
    song_list = []
    file = open('songfile.txt', 'r')

    for line in file:
        song_list.append(line.strip())
    file.close()
    return song_list


#
# bot  = download_bot(song)
# bot.get_link()
# bot.mp3site()
song_list = song_file_reader()

for song in song_list:
    bot = download_bot(song)
    bot.get_link()
    bot.mp3site()
    flag = check_download_completion()
    if flag is True:
        check_download_completion()

    bot.close_session()
