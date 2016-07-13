import requests
import base64
import time
import re
import json
try:
	import pokemon_pb2
	import pokemon
	from protobuf_codec import Codec
except:
	print '[!] ask mila for files..'
	exit()
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

api_url='https://pgorelease.nianticlabs.com/plfe/rpc'
login_url='https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize'
login_oauth='https://sso.pokemon.com/sso/oauth2.0/accessToken'

proxies = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}
use_proxy=True
debug=True

s=requests.session()
if use_proxy:
	s.proxies.update(proxies)
s.headers.update({'User-Agent':'Niantic App'})
s.verify=False

def get_api(access_token):
	try:
		r=s.post(api_url,data=base64.b64decode(pokemon.generate_login(access_token)),verify=False)
		pok = pokemon_pb2.Login()
		pok.ParseFromString(r.content)
		return 'https://'+pok.api_point+'/rpc'
	except:
		print '[-] server offline'
		time.sleep(3)
		get_api()
		
def use_api(target_api,access_token):
	if debug:
		print '[!] using api:',target_api
	r=s.post(target_api,data=base64.b64decode(pokemon.generate_login(access_token)),verify=False)
	return r.content
	
def login_pokemon(user,passw):
	print '[!] doing login for:',user
	head={'User-Agent':'niantic'}
	r=s.get(login_url,headers=head)
	jdata=json.loads(r.content)
	data={'lt':jdata['lt'],
		'execution':jdata['execution'],
		'_eventId':'submit',
		'username':user,
		'password':passw}
	r1=s.post(login_url,data=data,headers=head)
	ticket=re.sub('.*ticket=','',r1.history[0].headers['Location'])
	data1={'client_id':'mobile-app_pokemon-go',
			'redirect_uri':'https://www.nianticlabs.com/pokemongo/error',
			'client_secret':'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR',
			'grant_type':'refresh_token',
			'code':ticket}
	r2=s.post(login_oauth,data=data1)
	access_token=re.sub('&expires.*','',r2.content)
	access_token=re.sub('.*access_token=','',access_token)
	return access_token
	
def main():
	access_token= login_pokemon('username','verystrongpassword')
	if access_token is not None:
		print '[+] Token:',access_token[:40]+'...'
		new_api= get_api(access_token)
		if 'Milaly432' in use_api(new_api,access_token):
			print '[+] logged in'
		else:
			print '[-] protobuf sux..'
	
if __name__ == '__main__':
	main()