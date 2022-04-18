from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
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
print("Browser up, Getting links")

for genre in ["bass", "beats", "deep-house", "drum-bass", "dubstep", "edm", "electronica", "house", "tech-house", "techno", "trance" ] :
   url = "http://www.mixcloud.com/discover/"
   url += genre
   print("Loading mixcloud site for : " + genre )
   browser.get(url)
   notatend = True
   print("Loaded mixcloud site for : " + genre )
   lastplen = 0
   plen = 0 
#   print("\rLooking for 100th in the chart > ", )
   while notatend :
      print("\rLooking for change in length of page > Sending END key and wait for site to load - * Yawn * " + str(plen), end ="" )
      browser.find_element_by_xpath('//body').send_keys(Keys.END)
      time.sleep(5)
      paragraphs = browser.find_elements_by_tag_name('p')
      plen = len(paragraphs)
      if plen == lastplen :
#for p in paragraphs :
        # sys.stdout.write("\033[K")
        # print("\rLooking for 100th in the chart > " + p.text, end = "" )
        # if p.text == "100" :
          notatend = False
          print("\nGot it !")
          break
      lastplen = plen

#   time.sleep(10)
#   browser.send_keys(Keys.END)
   print("\rExtracting urls. Hunnnnnnnn..........", end = "")
   elems = browser.find_elements_by_tag_name('a')
   uelems = set(elems)
   urllist = []
   for elem in uelems:
      href = elem.get_attribute('href')
      if href is not None:
         cloud = href.count("www.mixcloud.com")
         slashes = href.count("/") # ensure correct path depth
         select = href.count("select") # thise are just links to more lists
         discover = href.count("discover")

         if slashes == 5 and select == 0 and discover == 0 and cloud > 0 :
               # string cleaning
#            print("URL:"),
#            print(href)
            urllist.append(href)
   #sys.stdout.write("\033[K")
   print("Agh..")
   print(str(len(urllist)) + " urls")
   uurllist = list( dict.fromkeys(urllist) )
   print(str(len(uurllist)) + " Unique urls")
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download(urllist)

browser.close()
