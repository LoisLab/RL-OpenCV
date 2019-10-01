import http.client
import argparse
import time

def move(n):
    try:
        bot = http.client.HTTPConnection(args['ip'])
        bot.request('GET','/action='+str(n))
        return bot.getresponse()

    except Exception as e:
        print(e)
        print('Did you remember to specify ip address using -ip ?')

ap = argparse.ArgumentParser()
ap.add_argument('-ip')
args = vars(ap.parse_args())

for n in range(8):
    response = move(n)
    print(n, response.status)
    time.sleep(2)
