import requests
import requests.auth
import sys
import simplejson as json
UID = secret
SECRET = secret

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[1;40;92m'
	WARNING = '\033[1;40;93m'
	FAIL = '\033[1;40;91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def get_token():
	args = [
		'grant_type=client_credentials',
		'client_id=secret',
		'client_secret=secret',
	]
	client = requests.post("https://api.intra.42.fr/oauth/token?%s" % ("&".join(args)))
	token_json = client.json()
	return token_json['access_token']

def read_names():
	filename = sys.argv[1]
	with open(filename) as n_file:
		names = n_file.read().splitlines()
	return names
def init_location(names):
	loc = names[:];
	for i in range(len(names)):
		loc[i] = 'Not Active'
	return loc
token = get_token()
names = read_names()
loc = init_location(names)
for i in range(len(names)):
	status = requests.post('http://api.intra.42.fr/v2/users/' + names[i] + '/locations?access_token=' + token + '&filter[active]=true')
	response = status.json()
	if status.status_code != 200:
		loc[i] = 'User Does Not Exist'
		print(bcolors.FAIL + 'User:  \'' + names[i] +
			'\'' + bcolors.ENDC + '\n' +
			bcolors.FAIL + 'Error:  Does Not Exist' + bcolors.ENDC)
	elif response and names[i] == response[0]['user']['login']:
		loc[i] = response[0]['host']
		z = loc[i].index('z')
		r = loc[i].index('r')
		p = loc[i].index('p')
		print (bcolors.OKGREEN + 'User:  \'' + names[i] + "\'" + bcolors.ENDC + '\n' +
			bcolors.OKGREEN + "Host:  " + loc[i] +
			'  Zone: ' + loc[i][z + 1:r] + '  Row: ' + loc[i][r + 1:p]
			+ '  Position: ' + loc[i][p + 1:] + bcolors.ENDC)
	else:
		print(bcolors.WARNING + 'User:  \'' + names[i] + '\'' + bcolors.ENDC +
			'\n' + bcolors.WARNING + 'Error:  Not Active' + bcolors.ENDC)
	print ''
