import sys
import json, requests
import flask
import os
import webbrowser
from keys import client_id, client_secret

authenticate_code = ""
access_token = ""
client_id = "be657616cb9e4c07b8a53f42fc9670f2"
client_secret = "39a8f0a14c4248368bcc03b6c36812f1"

def get_code():
    app = flask.Flask(__name__)

    def shutdown_flask():
        func = flask.request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return "Done"

    @app.route("/")
    def requst():
        global authenticate_code

        try:
            authenticate_code = flask.request.args["code"]
        except (ValueError, KeyError):
            flask.abort(400, "code not found!")

        shutdown_flask()

        return "Ok"

    app.run(port=8080)

def authenticate():
	global access_token
	params = "grant_type=authorization_code&code=" + authenticate_code + "&client_id=" + client_id + "&client_secret="+ client_secret
	headers = {
		"Content-type": "application/x-www-form-urlencoded"
	}
	r = requests.post("https://oauth.yandex.ru/token", data=params,headers=headers).json()
	access_token = r['access_token']
	return

def authenticate_user():
	global authenticate_code
	print('Opening login windows. Press any key when you are logged in')
	webbrowser.open_new("https://oauth.yandex.ru/authorize?response_type=code&client_id="+client_id)
	get_code()
	return authenticate()
	
def get_counter():
	print("retriving info of first counter")
	url = "https://api-metrika.yandex.ru/management/v1/counters?oauth_token=" + access_token
	r = requests.get(url).json()
	print("Counters count: " + str(r['rows']))
	print("id:   " + str(r['counters'][0]['id']))
	print("name: " + r['counters'][0]['name'])
	print("site: " + r['counters'][0]['site'])
	counter_id = r['counters'][0]['id']
	print("retriving info of first counter visit reports")
	url = "https://api-metrika.yandex.ru/stat/v1/data/bytime?ids=" + str(counter_id) + "&metrics=ym:s:visits,ym:s:pageviews,ym:s:users&date1=2daysAgo&date2=today&group=day&oauth_token=" + access_token
	r = requests.get(url).json()
	print(r)
	print(r['data'])
	print("Today")
	print("Visits:     " + str(r['data'][0]['metrics'][0][2]))
	print("PageViews:  " + str(r['data'][0]['metrics'][1][2]))
	print("Uniq users: " + str(r['data'][0]['metrics'][2][2]))
	print("Yesterday")
	print("Visits:     " + str(r['data'][0]['metrics'][0][1]))
	print("PageViews:  " + str(r['data'][0]['metrics'][1][1]))
	print("Uniq users: " + str(r['data'][0]['metrics'][2][1]))
	print("2 days ago")
	print("Visits:     " + str(r['data'][0]['metrics'][0][0]))
	print("PageViews:  " + str(r['data'][0]['metrics'][1][0]))
	print("Uniq users: " + str(r['data'][0]['metrics'][2][0]))
	return
	
authenticate_user()
get_counter()