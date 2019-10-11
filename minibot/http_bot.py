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
            if not status==200:
                print(status)
        except Exception as e:
            print(e)

    def set_speed(self,speed):
        try:
            self.webservice.request('GET','/speed='+str(speed))
            status = self.webservice.getresponse().status
            if not status==200:
                print(status)
        except Exception as e:
            print(e)
