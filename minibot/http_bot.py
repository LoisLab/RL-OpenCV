import http.client
import time

'''
Client side of bot controlled by webservice over http
'''

class HttpBot:
    def __init__(self,ip,delay=1.5):
        self.ip = ip
        self.webservice = http.client.HTTPConnection(ip)

    def step(self,n):
        try:
            self.webservice.request('GET','/action='+str(n))
            time.sleep(delay)
        except Exception as e:
            print(e)
