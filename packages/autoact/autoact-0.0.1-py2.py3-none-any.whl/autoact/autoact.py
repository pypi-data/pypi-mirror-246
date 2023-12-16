
import requests

g_url = 'http://127.0.0.1:9560'  

def sendEvent(url):
    return requests.get(url).text

def sendEvent_ping():
    url = g_url + '/ping'  
    return sendEvent(url)

def sendEvent_hide():
    url = g_url + '/hide'  
    return sendEvent(url)
