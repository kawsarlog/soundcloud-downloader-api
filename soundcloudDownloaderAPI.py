import time
import json
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities


def define_driver():
    driver_path = 'C:\\Users\\Rana\\.wdm\\drivers\\chromedriver\\win64\\119.0.6045.124\\chromedriver-win32/chromedriver.exe'
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")

    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, desired_capabilities=capabilities, options=options)
    return driver


def get_downloadUrl(driver, track_url):
    for _ in range(5):

        downloadUrl = None

        try:
            driver.get(track_url)
        except:
            driver.get(track_url)

        # wait for the XHR requests to complete
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@class="userBadge__title" or contains(text(),"This track was not found")]')))
        time.sleep(1)

        not_found = len(driver.find_elements(By.XPATH, '//*[contains(text(),"This track was not found")]')) != 0
        if not_found:
            return False

        for i in range(100):
            logs_raw = driver.get_log("performance")
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
            xhr_logs = [log for log in logs if "Network.responseReceived" in log["method"]]
            if xhr_logs:
                break
            time.sleep(0.1)

        for log in xhr_logs:
            try:
                request_id = log["params"]["requestId"]
                resp_url = log["params"]["response"]["url"]
                if "https://cf-hls-media.sndcdn.com/media/" in resp_url:
                    downloadUrl = resp_url
                    return downloadUrl
            except:
                pass

    return downloadUrl


def get_response(track_url):
    driver = define_driver()
    downloadUrl = get_downloadUrl(driver, track_url)

    # If tracks Not found
    if not downloadUrl:
        output_json = {
            'status': False,
            'reason': 'This track was not found. Maybe it has been removed',
            'trackLink': track_url,
        }
        driver.quit()
        return output_json


    try:
        userName = driver.find_element(By.CSS_SELECTOR, '[class="userBadge__title"]').text.split('\n')[0]
    except:
        time.sleep(1)
        try:
            userName = driver.find_element(By.CSS_SELECTOR, '[class="userBadge__title"]').text.split('\n')[0]
        except:
            # print(traceback.format_exc())
            userName = None

    try:
        userFollowerCount = \
        driver.find_element(By.CSS_SELECTOR, '[title*="follower"]').get_attribute('title').split(' ')[0].replace(',',
                                                                                                                 '')
        userFollowerCount = int(userFollowerCount)
    except:
        # print(traceback.format_exc())
        userFollowerCount = None

    try:
        userTracksCount = driver.find_element(By.CSS_SELECTOR, '[title*="tracks"]').get_attribute('title').split(' ')[
            0].replace(',', '')
        userTracksCount = int(userTracksCount)
    except:
        # print(traceback.format_exc())
        userTracksCount = None

    try:
        userVerified = len(driver.find_elements(By.CSS_SELECTOR, '[title="Verified"]')) == 1
    except:
        # print(traceback.format_exc())
        userVerified = None

    try:
        title = driver.find_element(By.CSS_SELECTOR, 'h1[class*="soundTitle__title"]').text
    except:
        # print(traceback.format_exc())
        title = None

    try:
        likesCount = driver.find_element(By.CSS_SELECTOR, '[title*="like"]').get_attribute("title").replace(" likes",
                                                                                                            '').replace(
            " like", '').replace(",", '')
        likesCount = int(likesCount)
    except:
        # print(traceback.format_exc())
        likesCount = None

    try:
        playsCount = driver.find_element(By.CSS_SELECTOR, '[title*="play"]').get_attribute("title").replace(" plays",
                                                                                                            '').replace(
            " play", '').replace(",", '')
        playsCount = int(playsCount)
    except:
        # print(traceback.format_exc())
        playsCount = None

    try:
        repostsCount = driver.find_element(By.CSS_SELECTOR, '[title*="repost"]').get_attribute("title").replace(
            " reposts", '').replace(" repost", '').replace(",", '')
        repostsCount = int(repostsCount)
    except:
        # print(traceback.format_exc())
        repostsCount = None

    try:
        commentsCount = driver.find_element(By.CSS_SELECTOR, 'span[class="commentsList__actualTitle"]').text.replace(
            " comments", '').replace(" comment", '').replace(",", '')
        commentsCount = int(commentsCount)
    except:
        # print(traceback.format_exc())
        commentsCount = None

    # print('userName:', userName)
    # print('userFollowerCount:', userFollowerCount)
    # print('userTracksCount:', userTracksCount)
    # print('userVerified:', userVerified)
    # print('title:', title)
    # print('likesCount:', likesCount)
    # print('playsCount:', playsCount)
    # print('repostsCount:', repostsCount)
    # print('commentsCount:', commentsCount)
    # print('downloadUrl:', downloadUrl)

    driver.quit()

    output_json = {
        'status': True,
        'userName': userName,
        'userFollowerCount': userFollowerCount,
        'userTracksCount': userTracksCount,
        'userVerified': userVerified,
        'title': title,
        'likesCount': likesCount,
        'playsCount': playsCount,
        'repostsCount': repostsCount,
        'commentsCount': commentsCount,
        'downloadUrl': downloadUrl,
        'trackLink': track_url,
    }

    return output_json


if __name__ == '__main__':
    track_url = "https://soundcloud.com/whethan/lock-it-up"
    output_json = get_response(track_url)
    print(output_json)
