from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import BeautifulSoup

# use pydub to play the audio - requires ffmpeg as well
from pydub import AudioSegment
from pydub.playback import play


import time
import re
import base64
import os
import json


def login_and_play():
    # create a new Firefox session
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.maximize_window()

    # navigate to the application home page
    driver.get("https://www.wakingup.com/")

    # get the username textbox
    username = driver.find_element_by_name("username")
    username.clear()

    # enter username
    username.send_keys("your_username")

    # submit the form to send the magic link
    username.send_keys(Keys.RETURN)

    # wait for the email to arrive
    time.sleep(60)

    # use the Gmail API to retrieve the magic link
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q="from:noreply@wakingup.com").execute()
    messages = results.get('messages', [])

    if not messages:
        print('No new messages.')
    else:
        message = messages[0]
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        email_data = msg['payload']['headers']
        for values in email_data:
            name = values['name']
            if name == 'From':
                from_name = values['value']
                for part in msg['payload']['parts']:
                    data = part['data']
                    data = data.replace("-","+").replace("_","/")
                    decoded_data = base64.b64decode(data)
                    soup = BeautifulSoup(decoded_data , "lxml")
                    body = soup.body()
                    # find the magic link in the email body
                    link = re.findall(r'(https?://\S+)', body)
                    driver.get(link[0])

    # find and click the play button
    play_button = driver.find_element_by_id("play_button")
    play_button.click()

    # wait for the network requests to load
    time.sleep(5)

    # get the network requests
    network_requests = driver.get_log('performance') 

    # find the .m4a file in the network requests
    sound_file_url = None
    for request in network_requests:
        if '.m4a' in request['message']:
            sound_file_url = json.loads(request['message'])['message']['params']['request']['url']
            break

    # play the sound file
    if sound_file_url:
        os.system("mpg123 " + sound_file_url)

    
    # load the sound file from the url
    sound = AudioSegment.from_file(sound_file_url, format="m4a")

    # play the sound file
    play(sound)

login_and_play()