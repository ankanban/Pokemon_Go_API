import requests
import base64
import time
import pokemon_pb2
import pokemon
try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

api_url='https://pgorelease.nianticlabs.com/plfe/rpc'

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

def get_api():
	try:
		r=s.post(api_url,data=base64.b64decode(pokemon.generate_login('Milaly432')),verify=False)
		pok = pokemon_pb2.Login()
		pok.ParseFromString(r.content)
		return 'https://'+pok.api_point+'/rpc'
	except:
		print '[-] server offline'
		time.sleep(3)
		get_api()
		
def use_api(target_api):
	if debug:
		print '[!] using api:',target_api
	r=s.post(target_api,data=base64.b64decode(pokemon.generate_login('Milaly432')),verify=False)
	return r.content
		
def main():
	new_api= get_api()
	if 'Milaly432' in use_api(new_api):
		print '[+] logged in'
	else:
		print '[-] protobuf sux..'
	
if __name__ == '__main__':
	main()