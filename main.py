from requester import Requester
import requests
from lxml import html

def test():
	url = 'http://www.shandongair.com.cn/en/'
	requester = Requester(url)
	response = requester.get_response()
	print(response.text)
	# r = requests.post('http://www.shandongair.com.cn/en/')
	# print(r.text)

if __name__ == "__main__":
	test()