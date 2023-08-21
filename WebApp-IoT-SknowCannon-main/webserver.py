import cherrypy
import requests
import random
import time
import jwt
import json

from io import BytesIO
from PIL import Image


class webServer():

	exposed = True

	def __init__(self, key):
		self.secret_key = key
		print(f"\n\n\n CHIAVE: {key}\n\n")
		self.utenti = {"utenti": [{"username": "darior28"}, {"username":"lorenzo"}, {"username":"davide"}, {"username": "giuse"}]}
		
	

	def getIP_Port_Uri_From_Service_Catalog(self,name="ResourceCatalog"):
		r = requests.get(f'http://127.0.0.1:8081/SC?id={name}')
		print(r)
		body = r.json()
		ip = body["address"]
		port = body["port"]
		uri = body["uri"]

		return ip, port, uri
	def GET (self, *uri, **params):

		if len(uri)==0:
			return open("index.html")
		else:
			if uri[0]=="areaPersonale":
				try:
					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					return open("EditLocality.html")
				except:
					return open("login.html")
				
			elif uri[0]=="logout":
				try:
					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					cookie = cherrypy.response.cookie #manda i cookie al browser
					cookie['sessionID'] = token
					cookie['sessionID']['path'] = '/'
					cookie['sessionID']['max-age'] = 0
					cookie['sessionID']['version'] = 1
					out= {"canceled": "true"}
					return json.dumps(out)
				except:
					out= {"canceled": "false"}
					return json.dumps(out)
			elif uri[0]=="EditLocality":
				try:
					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					return open("EditLocality.html")
				except:
					return open("login.html")
			elif uri[0]=="loggedUser":
				try:
					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					username = decode_token["user_data"]["username"]
					out = {"username": str(username)}
					return json.dumps(out)
				except:
					return open("login.html")
				
					
		if uri[0]=="data_v2":
			if uri[1] == "getMeasure":    # in automatico 
				# http://127.0.0.1:8080/data_v2/getTemperature?loc=Bardonecchia&slo=SlopeA&sec=SectorX&ns=10&measure=field1
				# SPECIAL parameter ns -> numero samples se uguale a 1 ritorna singolo valore (per card) se maggiore di 1 ritorna una time series con gli ultimi N valori richiesti
				# SPECIAL parameter measure -> you can express directly what measure you are searching for!
					# field1 -> snow depth
					# To be exlarged maybe in future
				# body: empty
				# return: "Temperature: 135" -> a string with the number of the temperature- > da cambiare in cosa serve
				try:
					
					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					print(f"\n\nTOKEN LATO BROWSER DECODIFICATO : {decode_token}\n\n")
					print(f"\n tok del token: {decode_token['user_data']['tok']}")
					thing_id= decode_token["user_data"]["id"]
					tok = decode_token["user_data"]["tok"]

					print(f"\n\nPROVA STAMPA: {thing_id}\n\n")
					

					print("sono entrato nel try")
					ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(name="ResourceCatalog")
					print(f"\n\nIP RC: {ip}, \n {uri}\n {port}\n\n")
					#ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(name="Login")																				
					thingspeak_info = requests.get(f'http://{ip}:{port}/{uri}/sector/thingspeak_info', params={'loc': params['loc'], 'slo': params['slo'], 'sec': params['sec'], 'id': thing_id})
					#thingspeak_info = requests.get(f'http://{ip}:{port}/{uri}/RC/sector/thingspeak_info', params={'tok': 'tokenof user','loc': params['loc'], 'slo': params['slo'], 'sec': params['sec']})
					
					thingspeak_info = thingspeak_info.json()
					print(f"THINGSPEAK INFO: {thingspeak_info}")
					

					ip_thing, port_thing, uri_thing = self.getIP_Port_Uri_From_Service_Catalog(
						name="ThingspeakConnector")
					
					print(f"\n\nIP THING: {ip_thing}, \n {uri_thing}\n {port_thing}\n\n")
					
					thingspeak_data = requests.get(f'http://{ip_thing}:{port_thing}/{uri_thing}/data', params={
					                               'api_key': thingspeak_info['api_key_read'], 'channel_id': thingspeak_info['channel_id'], 'results': params['ns']})
					
			
					thingspeak_data = thingspeak_data.json()
					print(f"\n\nDATI DA THINGSPEAK: {thingspeak_data}\n\n")

					if len(thingspeak_data['feeds']) > 0:
						snow_depth = [(e[params['measure']], e['created_at']) for e in thingspeak_data['feeds']]    # field1 sta per SNOW DEPTH
					else:
						snow_depth = "Error Retrieving data from thingspeak"
					print(f"Value inside thingspeak: {snow_depth}")
					output = {"data": snow_depth}
					return json.dumps(output)
				except:
					return "ERROR Code"
		elif uri[0]=="edit":
			
			if uri[1] == "getLocalities":
				# http://127.0.0.1:8080/edit/getLocalities
				# body: empty
				# return: ["Bardonecchia", "Sauze_d_Oulx", "MONCALIERI", "Markulla", "Pippo"]
				try:
					

					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					print(f"\n\nTOKEN LATO BROWSER DECODIFICATO : {decode_token}\n\n")
					print(f"\n tok del token: {decode_token['user_data']['tok']}")
					thing_id= decode_token["user_data"]["id"]
					tok = decode_token["user_data"]["tok"]

					ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(
						name="Login")

					r = requests.get(
						f'http://{ip}:{port}/{uri}/RC/network/localitiesID', params={'tok': str(tok)})

					print(r.text)

					output = { "data": json.loads(r.text)}
					return json.dumps(output)

				except:
					return open("login.html")
			elif uri[1]=="getSlopesByLocalityName":
				# http://127.0.0.1:8080/edit/getSlopesByLocalityName?loc=Bardonecchia
				# body: empty
				# return: ["SlopeA", "SlopeB"] 
				try:
				
					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					print(f"\n\nTOKEN LATO BROWSER DECODIFICATO : {decode_token}\n\n")
					print(f"\n tok del token: {decode_token['user_data']['tok']}")
					thing_id= decode_token["user_data"]["id"]
					tok = decode_token["user_data"]["tok"]
					ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(name="Login")

					r = requests.get(f'http://{ip}:{port}/{uri}/RC/locality/slopesID',params= {'tok': str(tok), 'loc': params['loc']})
					
					print(r.text)
					output = { "data": json.loads(r.text)}
					return json.dumps(output)
				
				except:
					return open("login.html")
			elif uri[1] == "getSectorsBySlopeNameByLocalityName":
				# http://127.0.0.1:8080/edit/getSectorsBySlopeNameByLocalityName?loc=Bardonecchia&slo=SlopeA
				# body: empty
				# return: ["SectorX", "SectorY"]
				try:
					#Nel caso di SKNOW CANNON DEVO RECUPERARE tok 

					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					print(f"\n\nTOKEN LATO BROWSER DECODIFICATO : {decode_token}\n\n")
					print(f"\n tok del token: {decode_token['user_data']['tok']}")
					thing_id= decode_token["user_data"]["id"]
					tok = decode_token["user_data"]["tok"]
					
					ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(
						name="Login")

					r = requests.get(
						f'http://{ip}:{port}/{uri}/RC/slope/sectorsID', params={'tok': str(tok), 'loc': params['loc'], 'slo': params['slo']})

					print(r.text)
			
					output = { "data": json.loads(r.text)}
					return json.dumps(output)
				

				except:
					return open("login.html")


	
	def POST(self, *uri, **params):
		if uri[0]=="login":
			body=cherrypy.request.body.read()
			dict_body=json.loads(body)
			print(str(dict_body))
			if not dict_body:
				raise cherrypy.HTTPError(400, "Bad Request")
			else:
				username = dict_body["username"]
				password = dict_body["password"]
				print(f"PSS arrived(tok): {password}")

				esito = self.check_user(username, password) 
				if esito:
					cookie = cherrypy.response.cookie 
					token = self.generate_token(username,password, 600)
					print(token)
					cookie['sessionID'] = token
					cookie['sessionID']['path'] = '/'
					cookie['sessionID']['max-age'] = 600
					cookie['sessionID']['version'] = 1
					print("\ntoken generato e inviato al browser\n")
					out= {"verified": "true", "username": str(username)}
					return json.dumps(out)
				else:
					print(f"esito {esito}: password o username errati")
					#password immessa è sbagliata
					out= {"verified": "false"}
					return json.dumps(out)
		elif uri[0]=="edit":
			body=cherrypy.request.body.read()
			dict_body=json.loads(body)
			print(str(dict_body))
			if not dict_body:
				raise cherrypy.HTTPError(400, "Bad Request")
			else:
				if uri[1]=="addLocality":
					# http://127.0.0.1:8080/edit/addLocality
					# body
					'''
					{ 
						"name": "Miami",
					}
					'''

					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					print(f"\n\nTOKEN LATO BROWSER DECODIFICATO : {decode_token}\n\n")
					print(f"\n tok del token: {decode_token['user_data']['tok']}")
					thing_id= decode_token["user_data"]["id"]
					tok = decode_token["user_data"]["tok"]

					ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(name="Login")

					body_response = {"tok": str(tok),
										"name": dict_body["name"],
												"slopes": []
									}

					r = requests.post(
										f'http://{ip}:{port}/{uri}/RC/locality',params={"tok": str(tok) }, json=json.dumps(body_response))

					print(r.text)
					print(dict_body["name"])
					return "perfetto"
				if uri[1] == "addSlopeToLocality":
					# http://127.0.0.1:8080/edit/addSlopeToLocality
					# body
					'''
					{ 
						"name": "Slo3",
						"locality":"Markulla",
					}
					'''
					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					print(f"\n\nTOKEN LATO BROWSER DECODIFICATO : {decode_token}\n\n")
					print(f"\n tok del token: {decode_token['user_data']['tok']}")
					thing_id= decode_token["user_data"]["id"]
					tok = decode_token["user_data"]["tok"]


					ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(name="Login")
					slo = {
						'tok': str(tok),
						'name': dict_body["name"],
						'sectors': []
					}

					print(f"\n\nSTO FACENDO LA POST PER AGGIUNGERE LA SLOPE: {dict_body['name']}")
					
					print(dict_body["name"])
					
					r= requests.post(f'http://{ip}:{port}/{uri}/RC/slope', params = {"tok": str(tok), 'loc': dict_body["locality"]}, json = json.dumps(slo))


					print(r.text)
					return "slope aggiunta"
				if uri[1] == "addSectorToSlopeToLocality":
					# http://127.0.0.1:8080/edit/addSectorToSlopeToLocality
					# body
					'''
					{ 
						"name": "Sec3",
						"locality":"Markulla",
						"slope":"Slo1"
					}
					'''

					incoming_cookie = cherrypy.request.cookie
					token = incoming_cookie["sessionID"].value
					decode_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
					print(f"\n\nTOKEN LATO BROWSER DECODIFICATO : {decode_token}\n\n")
					print(f"\n tok del token: {decode_token['user_data']['tok']}")
					thing_id= decode_token["user_data"]["id"]
					tok = decode_token["user_data"]["tok"]

					ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(name="Login")
					sec = {
						'tok': str(tok),
						'name': dict_body["name"],
						'cannons': [],
						'sensors':[]
					}

					print(f"\n\nSTO FACENDO LA POST PER AGGIUNGERE IL SETTORE: {dict_body['name']}")
					r= requests.post(f'http://{ip}:{port}/{uri}/RC/sector', params = {"tok": str(tok), 'loc': dict_body["locality"],'slo':dict_body["slope"]}, json = json.dumps(sec))


					print(r.text)
					return "sector aggiunto"

		return 
	
	def PUT(self, *uri, **params):
		return None
	
	def DELETE (self, *uri,**params):
		# DELETE Sector
		# http://127.0.0.1:8082/RC/sector?loc=Markulla&slo=Slo1&sec=Sec2
		# body: empty

		pass
	

	def check_user(self, username, password):
	
		'''for user in self.utenti["utenti"]:
			if (user["username"] == str(username) ) and (user["password"]==str(password)) :	
				return True'''
		
		ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(name="Login")

		r = requests.get(f'http://{ip}:{port}/{uri}/auth',params={"tok": str(password)})

		print(f"RISPOSTA ALLA REQUEST LOGIN: {r.text}")

		for user in self.utenti["utenti"]:
			if user["username"]==str(username) and r.status_code==200:
				return True		
		
		return	False
	
	def generate_token(self, username, password, expiration):

		ip, port, uri = self.getIP_Port_Uri_From_Service_Catalog(name="Login")

		r = requests.get(f'http://{ip}:{port}/{uri}/auth',params={"tok": str(password)})

		user_data = {"username": str(username), "tok": str(password), "id": r.text.replace('"', '')}

		print(f"\n\n\nuser data: {user_data}\n\n\n")

		payload = {
			"user_data": user_data,
			"exp": time.time() + expiration
		}
		token = jwt.encode(payload, self.secret_key, algorithm="HS256")
		return token
		

