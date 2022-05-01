#Importing Modules
from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json
from data import facts, get_news



#Getting Videos From Youtube
def get_video():
  channel = 'https://api.rss2json.com/v1/api.json?rss_url=https://www.youtube.com/feeds/videos.xml?channel_id=UC07-dOwgza1IguKA86jqxNA'
  r = requests.get(channel).json()
  links = []
  for item in (r['items']):
    links.append({"title":item['title'],
  "id":item['guid'].split("video:")[1],
  "date":item['pubDate'][10:16]+", "+item['pubDate'][:9],
  "author":item['author'],
  "link":item['link']})
  #Picking Videos that is related to Covid19
  links = [x for x in links if "virus" in x['title'].lower() or "vaccine" in x['title'].lower() or "covid" in x['title'].lower()]
  return links[:6]



#Setting Up Flask
app = Flask(__name__,  template_folder='site', static_folder='assets')

#HomePage
@app.route('/', methods=["POST", "GET"])
def base_page():
   return render_template('index.html', news=get_news(), videos=get_video(), facts=facts)

#Handling Errors
@app.errorhandler(Exception)
def http_error_handler(error):
  return render_template('index.html', news=get_news(), videos=get_video(), facts=facts)


#Running Flask
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    #app.run()


  
