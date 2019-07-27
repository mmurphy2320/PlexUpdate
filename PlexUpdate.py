import requests
from bs4 import BeautifulSoup
import re
import subprocess

class PlexServer:


	def __init__(self, credentials):
		self.credentials = credentials
		self.update_url = 'https://plex.tv/pms/downloads/5.json'
		self.login_url = 'https://plex.tv/users/sign_in.json'
		self.username = self.read_username()
		self.password = self.read_password()
		self.server_ip = self.read_ip()
		self.latest_version = self.check_latest_version()
		self.x_plex_token = self.get_x_plex_token()
		self.my_vers = self.get_my_vers()
		self.need_update = self.is_update_required()


	def read_username(self):
		with open(self.credentials, 'r') as f:
			entries = f.readlines()
			corrupt_user = entries[0]
			real_user = corrupt_user[:-1]
			return real_user

	def read_password(self):
		with open(self.credentials, 'r') as f:
			entries = f.readlines()
			corrupt_pass = entries[1]
			real_pass = corrupt_pass[:-1]
			return real_pass

	def read_ip(self):
		with open(self.credentials, 'r') as f:
			entries = f.readlines()
			real_ip = entries[2]
			return real_ip

	def check_latest_version(self):
		# Parses Response and creates JSON Object
		response = requests.get(self.update_url)
		response_data = response.json()
		# Parses JSON dict to locate version and stores the variable
		latest_ver = response_data['computer']['Linux']['version']
		# Return string of latest version
		return latest_ver

	def get_x_plex_token(self):
		headers = {'X-Plex-Client-Identifier': 'Plex-Upgrade-Script',
				   'X-Plex-Product': 'mmurphy-upgrade-script', 'X-Plex-Version': 'Version 1.1'}
		data = {'user[login]': self.username, 'user[password]': self.password}
		response = requests.post(self.login_url, headers=headers, data=data)
		login_data = response.json()
		# Parses JSON object and stores authToken
		token = login_data['user']['authToken']
		return token

	def get_my_vers(self):
		pms_server_API_url = f'http://{self.server_ip}:32400/servers/?X-Plex-Token={self.x_plex_token}'
		# Stores GET Response
		pms_response = requests.get(pms_server_API_url)
		# Stores GET Content as BeautifulSoup Object parsed by HTML Parser
		bs_data = BeautifulSoup(pms_response.content, 'html.parser')
		# Parse and return version
		return bs_data.mediacontainer.server['version']

	def is_update_required(self):
		if self.latest_version == self.my_vers:
			return False
		else:
			return True


myPlexServer = PlexServer('credentials.txt')
print(f'Latest version of Plex Media Server is {myPlexServer.latest_version}')
print(f'My version of Plex Media Server is {myPlexServer.my_vers}')
print(f'Does my PMS require an update: {myPlexServer.need_update}')