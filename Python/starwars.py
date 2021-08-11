from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request as client
import sys
import json
import random as rand

# written by: Jake Peery
# email: jake_peery@yahoo.com
# service to aquire data from swapi.dev and return reformatted JSON data of a random film
# json data to consist of film_name as a string and opening_crawl as a list
# built and tested with version 3.9.0


#server variables
hostName = "localhost"
serverPort = 8080



#Get data
def GetSWAPI():
    random = rand.randint(1, 6)
    url = 'https://swapi.dev/api/films/{num}/'.format(num=random)
    data = client.urlopen(url).read()
    data = json.loads(data)

    toSend = {}
    
    toSend['film_name'] = data['title']

    openingCrawl = data['opening_crawl'].split('\r\n')
    toSend['opening_crawl'] = openingCrawl
    
    return toSend



#Server
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/random_crawl':
            data = GetSWAPI()
            tosend = json.dumps(data).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(tosend)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://{host}:{port}".format(host=hostName, port=serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
