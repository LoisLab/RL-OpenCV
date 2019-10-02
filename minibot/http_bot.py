import http.client
import time

'''
Client side of bot controlled by webservice over http
'''

class HttpBot:
    def __init__(self,ip,delay=1.5):
        self.ip = ip
        self.webservice = http.client.HTTPConnection(ip)
        self.delay=delay

    def step(self,n):
        try:
            self.webservice.request('GET','/action='+str(n))
            status = self.webservice.getresponse().status
            time.sleep(self.delay)
            print(status)
        except Exception as e:
            print(e)
