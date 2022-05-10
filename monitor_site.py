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


##############
# PARAMETERS #
##############

URL_TO_MONITOR = 'https://www.canyon.com/en-us/road-bikes/race-bikes/ultimate/cf-sl/ultimate-cf-sl-8/2861.html?dwvar_2861_pv_rahmenfarbe=BU%2FBK'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
delay = 900 # seconds

log = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


#############
# FUNCTIONS #
#############

def check_availability(URL_TO_MONITOR):
    previous_availability = ['July 2022']

    response = requests.get(URL_TO_MONITOR, headers=headers) # Requesting the webpage
    soup = BeautifulSoup(response.text, 'html.parser') # Parsing the webpage
    # Finding the desired element on the webapge to monitor
    size_small = soup.find_all('div', {'class': 'productConfiguration__selectVariant'})[2] # Size small  {0: XXS, 1: XS, 2: S, 3: M, 4: L, 5: XL}
    availability_message = size_small.find('div', {'class': 'productConfiguration__availabilitySubMessage'}).text # Availability message
    availability_message = availability_message.replace('\n', '').strip() # Removing line breaks and leading and trailing spaces

    if previous_availability[0] != availability_message: # Comparing the previous availability with the current one
        message = f'Canyon website has been updated --Availability changed to {availability_message}!'
        send_message(message, os.getenv('MY_NUMBER')) # Sending an SMS only if the availability changes
        previous_availability = availability_message # Updating previous availability with the current one
    else:
        log.info('No changes...')


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
messaging_service_sid = os.getenv('MESSAGE_SERVICE_SID')

def send_message(message_body, number):
    client = Client(account_sid, auth_token)
    
    message_body = client.messages.create(  
                                messaging_service_sid=messaging_service_sid, 
                                body=message_body,      
                                to=number 
                            ) 
    
    print('Message Sent!')


#################
# MAIN FUNCTION #
#################

def main():
    log.info("Monitoring Canyon website...")

    while True:
        try:
            check_availability(URL_TO_MONITOR)
        except:
            log.info("Error checking website.")
        time.sleep(delay)

if __name__ == "__main__":
    main()