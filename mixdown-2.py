# very slow single threaded version
from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'ignoreerrors': 'yes',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]}

options = Options()
options.headless = True
profile = webdriver.FirefoxProfile()
profile.DEFAULT_PREFERENCES['frozen']["dom.webdriver.enabled"] = False # I'm not a bot honest!

print("Staring browser")

browser = webdriver.Firefox(firefox_profile=profile, options=options )
#browser.get("https://www.patientaccess.com/login")
print("Browser up, Getting links")

for genre in ["beats", "deep-house", "drum-bass", "dubstep", "edm", "electronica", "house", "tech-house", "techno", "trance", "science"] :
   url = "http://www.mixcloud.com/discover/"
   url += genre
   browser.get(url)
   elems = browser.find_elements_by_tag_name('a')
   uelems = set(elems)
   urllist = []
   for elem in uelems:
      href = elem.get_attribute('href')
      if href is not None:

         slashes = href.count("/") # ensure correct path depth
         select = href.count("select") # thise are just links to more lists
         discover = href.count("discover")

         if slashes == 5 and select == 0 and discover == 0 :
               # string cleaning
#            print("URL:"),
            print(href)
            urllist.append(href)
   print(len(urllist))
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download(urllist)
browser.close()
