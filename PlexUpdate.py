import requests
from bs4 import BeautifulSoup
import re

info = []


def read_info(filename):
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            info.append(line)
            reader.close()


def check_latest_version():
    # Stores Plex API Downloads URL
    url = 'https://plex.tv/pms/downloads/5.json'
    # Parses Response and creates JSON Object
    response = requests.get(url)
    response_data = response.json()
    # Parses JSON dict to locate version and stores the variable
    latest_ver = response_data['computer']['Linux']['version']
    # Return string of latest version
    return latest_ver


def get_update_url():
    # Stores Plex API Downloads URL
    url = 'https://plex.tv/pms/downloads/5.json'
    # Parses Response and creates JSON Object
    response = requests.get(url)
    response_data = response.json()
    # Parses JSON dict to locate URL of Debian x64 release
    update_url = response_data['computer']['Linux']['releases'][1]['url']
    print(update_url)
    filename_obj = re.search('plexmedia.*deb', update_url)
    filename = filename_obj.group()
    print(filename)
    return update_url


def my_current_version():
    # Stores Plex Login API URL
    login_url = 'https://plex.tv/users/sign_in.json'
    # Dictionary to store required HTTP Headers for the POST Request
    headers = {'X-Plex-Client-Identifier': 'Plex-Upgrade-Script',
               'X-Plex-Product': 'mmurphy-upgrade-script', 'X-Plex-Version': 'Version 1.0'}
    # Dictionary to store credentials - pulled from credentials.txt
    data = {'user[login]': USERNAME, 'user[password]': PASSWORD}
    # Parses Response and creates JSON object
    response = requests.post(login_url, headers=headers, data=data)
    login_data = response.json()
    # Parses JSON object and stores authToken
    token = login_data['user']['authToken']
    # Stores constructed PMS API URL - SERVER_IP from credentials.txt and token from previous POST
    pms_url = f'http://{SERVER_IP}:32400/servers/?X-Plex-Token={token}'
    # Stores GET Response
    pms_response = requests.get(pms_url)
    # Stores GET Content as BeautifulSoup Object parsed by HTML Parser
    bs_data = BeautifulSoup(pms_response.content, 'html.parser')
    # Parse and return version
    return bs_data.mediacontainer.server['version']


def is_update_required():
    if check_latest_version() == my_current_version():
        return False
    else:
        return True


# def plex_update(update_source):
    # url = update_source


# Actual Program
# Passes Credential File to ReadInfo Function
read_info('credentials.txt')


# Stores Credentials, Splices \n from Username/Password - Not needed for IP
USERNAME = info[0][:-1]
PASSWORD = info[1][:-1]
SERVER_IP = info[2]

# Debugging
print(f'Latest version from Plex.tv is {check_latest_version()}')
print(f'My Server is running version {my_current_version()}')
print(f'Does my server require an update? {is_update_required()}')
# get_update_url()
