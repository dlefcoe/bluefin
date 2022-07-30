import time
import datetime

# selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


time_str = time.strftime('%Y%m%d')
download_directory = 'Y:\\Benjamin\\Market_Making\\PCFs\\iShares_US\\' + time_str
# download_directory = 'Y:\\DL_trade\\code\\python\\get_usa_etf\\' + time_str


# chrome options
options = webdriver.ChromeOptions()
prefs = {
"download.default_directory": download_directory,
"download.prompt_for_download": False,
"download.directory_upgrade": True
}

options.add_experimental_option('prefs', prefs)


# connect webdriver
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

# driver.maximize_window()


# press the accpet button
driver.get('https://www.ishares.com/us/library')
x = '//*[@id="onetrust-accept-btn-handler"]'
button = driver.find_element_by_xpath(x)
driver.implicitly_wait(3)
ActionChains(driver).move_to_element(button).click(button).perform()


# Perform search
# search_keyword should be comma-separated with no space in between
search_keyword = "emb,lemb,cemb,emhy,lqd"
search = driver.find_element_by_name("keyword")
search.send_keys(search_keyword)
search.send_keys(Keys.RETURN)


# Click the checkbox "PCF"
try:
    pcf = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.ID, "materialTypePCF")))
        .click()
    )
except NoSuchElementException:
    print("An error has occurred!")
    driver.quit()



def download(filename):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, filename))
        ).click()
    except NoSuchElementException:
        print("An error has occurred for the file:", filename)
    return


folder_path = ''
file_list = ["pcf-" + name.upper() + "-en_US" for name in search_keyword.split(",")]


for file in file_list:
    download(file)
    time.sleep(1)

print('saved to folder: ', download_directory)



# log completed process
# log to file
data_file = r'Y:\DL_trade\code\python\get_usa_etf\log_file.txt'

with open(data_file, 'a') as f:
    f.write(f'process completed: {datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")}')
    f.write('\n')



