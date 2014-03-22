import requests

class Requester(object):
	def __init__(self, url):
		self.url = url

	def get_response(self, params = None):
		if params != None:
			if _check_input_type(params):
				response = requests.get(self.url, params=params)
		else:
			response = requests.get(self.url)

		return response

	def _check_input_type(self, inp):
		if type(inp) == dict:
			return True
		else:
			raise TypeError

	def post_response(self, params = None, headers = None, data = None):
		# not currect now, need do some changes

		if params == None and headers == None:
			response = requests.post(self.url)

		elif params == None and headers != None:
			if _check_input_type(data):
				response = requests.post(self.url, data=data, headers=headers)

		elif params != None and headers == None:
			if _check_input_type(params):
				response = requests.post(self.url, params=params)

		elif params != None and headers != None:
			if _check_input_type(params) and _check_input_type(data):
				response = requests.post(self.url, params=params, data=data, headers=headers)

		return response

	def put_response(self):
		response = requests.put(self.url)
		return response

	def delete_response(self):
		response = requests.delete(self.url)
		return response

	def head_response(self):
		response = requests.head(self.url)
		return response

	def options_response(self):
		response = requests.options(self.url)
		return response
	