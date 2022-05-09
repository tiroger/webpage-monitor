#############
# Libraries #
#############

import requests
from bs4 import BeautifulSoup
import os
import logging
import time
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

from twilio_send_sms import send_message


##############
# PARAMETERS #
##############

URL = 'https://www.canyon.com/en-us/road-bikes/race-bikes/ultimate/cf-sl/ultimate-cf-sl-8/2861.html?dwvar_2861_pv_rahmenfarbe=BU%2FBK'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
delay = 900 # seconds

log = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def check_availability(URL):
    previous_availability = ['July 2022']

    response = requests.get(URL, headers=headers) # Requesting the webpage
    soup = BeautifulSoup(response.text, 'html.parser') # Parsing the webpage
    # Removing the script and meta tags
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('meta')]

    availability = soup.find_all('div', class_='productConfiguration__availabilitySubMessage')[0].text
    availability = availability.replace('\n', '') # Removing line breaks and spaces
    # previous_availability.append(availability)

    if previous_availability[0] != availability: # Comparing the previous availability with the current one
        message = f'Canyon website has been updated --Availability changed to {availability}!'
        send_message(message, +16469426983) # Sending the message only if the availability has changed
    else:
        log.info('NO CHANGES...')


def main():
    log.info("Monitoring Canyon website...")

    while True:
        try:
            check_availability(URL)
        except:
            log.info("Error checking website.")
        time.sleep(delay)

if __name__ == "__main__":
    main()