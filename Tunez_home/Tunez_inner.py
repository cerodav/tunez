import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import sys
import logging
import argparse
import platform
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

class Tunez_inner(object):
    def __init__(self,query=None):
        self.query=query
        if self.query == None:
            sys.exit("Please enter search string")
        logging.debug("Query=="+self.query)
    
    def main_func(self):
        results=self.search(self.query)
        logging.info(len(results))
        #songID=input('\n Which song do you want to download ? ')
        #url=results[int(songID)]['url']
        #logging.debug("Url=="+url)
        #title=results[int(songID)]['title'];
        #logging.debug("Title=="+title)
        #logging.info("\n#Downloading_the_song")
        #self.download(url,title+".mp3")
        #logging.info("\n#Download completed\n")

    def search(self,query):
        query=query.replace(" ","%20")
        search_url='https://mp3skull.cr/search_db.php?q=%s&fckh=d4b5c698c0c30fa8f4229d59f9cc22bc' % (query)
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        logging.debug("Search url=="+search_url)
        try: 
            html_req=urllib2.Request(search_url,headers=hdr)
            html=urllib2.urlopen(html_req)
        except urllib2.HTTPError:
            try:
                html_req=urllib2.Request(search_url,headers=hdr)
                html=urllib2.urlopen(html_req)
            except urllib2.HTTPError:
                logging.warning("An error occured while getting the results. Please try again")
                
        #this part is useless (html response have to be sorted) 
        html_read=html.read()
        soup=BeautifulSoup(html_read)
        song_list_left=soup.find_all(class_="left")

        count=0
        song_info={}
        p = re.compile(r'<.*?>')
        for ele in song_list_left:
            song_info[count]=p.sub(' ',str(ele))
            count=count+1



        song_list_title=soup.find_all(class_="mp3_title")

        count=0
        song_title={}
        for ele in song_list_title:
            song_title[count]=ele.string
            count=count+1

        song_list_url=soup.find_all(class_="download_button")

        count=0
        song_url={}
        for ele in song_list_url:
            buff=ele.find_all('a',href=True)
            song_url[count]=buff[0]['href']
            count=count+1

        count=0
        song_results={}
        for ele in song_title:
            song_results[count]={}
            song_results[count]['info']=song_info[count]
            song_results[count]['title']=song_title[count]
            song_results[count]['url']=song_url[count]
            count=count+1

        return song_results

    def topsearches(self):
        search_url='https://mp3skull.cr'
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        logging.debug("Search url=="+search_url)
        try: 
            html_req=urllib2.Request(search_url,headers=hdr)
            html=urllib2.urlopen(html_req)
        except urllib2.HTTPError:
            try:
                html_req=urllib2.Request(search_url,headers=hdr)
                html=urllib2.urlopen(html_req)
            except urllib2.HTTPError:
                logging.warning("An error occured while getting the results. Please try again")
                
        #this part is useless (html response have to be sorted) 
        html_read=html.read()
        soup=BeautifulSoup(html_read)
        song_list_right=soup.find_all(id="topright")

        count=0
        song_info=[]
        p = re.compile(r'<.*?>')
        ptitle = re.compile('[0-9a-zA-Z ]* Mp3')
        pclean = re.compile(' Mp3')
        for ele in song_list_right:
            strng=ptitle.findall(str(ele))[0]
            song_info.append(pclean.sub("",str(strng)))

        return song_info

    def albumart(self,searchtag):
        searchtag=searchtag.replace(" ","+")
        search_url='http://www.covermytunes.com/search.php?search_query=%s&x=0&y=0' % (searchtag)
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

        try: 
            html_req=urllib2.Request(search_url,headers=hdr)
            html=urllib2.urlopen(html_req)
        except urllib2.HTTPError:
            try:
                html_req=urllib2.Request(search_url,headers=hdr)
                html=urllib2.urlopen(html_req)
            except urllib2.HTTPError:
                logging.warning("An error occured while getting the results for albumart search. Please try again")
                
        #this part is useless (html response have to be sorted)
        soup=BeautifulSoup(html.read())
        soupnodes=soup.find_all(width="170")

        try:
            if soupnodes[0]:
                src1=soupnodes[0].get('src');
            
        except:
            src1=""
        try:
            if soupnodes[1]:
                src2=soupnodes[1].get('src');
            
        except:
            src2=""

        albumart={src1,src2}
        
        return albumart

    def download(self,file_url,file_name):
        logging.info(file_url)
        url_res=urllib2.urlopen(file_url)

        file_res=open(file_name,'wb')
        meta=url_res.info()

        logging.info(meta)

        file_size = int(meta.get_all("Content-Length")[0])
        logging.info("Downloading %s (%s)" % (file_name, self.convertSize(file_size)))

        file_size_dl = 0
        block_size = 8192
        while True:
            buffer = url_res.read(block_size)
            if not buffer:
                break
                file_size_dl += len(buffer)
            file_res.write(buffer)
            status = r"%s [%3.2f%%]" % (self.convertSize(file_size_dl), file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1) #idk what this is ?
            logging.debug("Status == "+str(status)) 
            sys.stdout.write("\r        %s" % status)
        file_res.close()
        return 1;

    def joinartmusic(self,artfile,musicfile):
        audio = MP3(musicfile, ID3=ID3)

        # add ID3 tag if it doesn't exist
        try:
            audio.add_tags()
        except error:
            pass

        audio.tags.add(
            APIC(
                encoding=3, # 3 is for utf-8
                mime='image/png', # image/jpeg or image/png
                type=3, # 3 is for the cover image
                desc=u'Cover',
                data=open(artfile).read()
                )
        )
        audio.save()

    def convertSize(self, n, format='%(value).1f %(symbol)s', symbols='customary'):
    #dont know how this is working (please do check)    
        SYMBOLS = {
            'customary': ('B', 'K', 'Mb', 'G', 'T', 'P', 'E', 'Z', 'Y'),
            'customary_ext': ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                              'zetta', 'iotta'),
            'iec': ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
            'iec_ext': ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                        'zebi', 'yobi'),
        }
        n = int(n)
        if n < 0:
            raise ValueError("n < 0")
        symbols = SYMBOLS[symbols]
        prefix = {}
        for i, s in enumerate(symbols[1:]):
            prefix[s] = 1 << (i + 1) * 10
        for symbol in reversed(symbols[1:]):
            if n >= prefix[symbol]:
                value = float(n) / prefix[symbol]
                return format % locals()
        return format % dict(symbol=symbols[0], value=n)


def main():
    try:
        print("Hello")
        parser = argparse.ArgumentParser(description="Tunez_inner without interface developement")
        parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        parser.add_argument("query", help = "the name of the song or artist to search for")
        args = parser.parse_args()
        if args.verbose:
            logging.basicConfig(format = "%(message)s", level=logging.DEBUG)
        else:
            logging.basicConfig(format = "%(message)s", level=logging.INFO)
        logging.debug("Arguments == "+str(args))
        logging.debug("Platform == %s" %(platform.platform()))
        logging.debug("Python version == %s" %(platform.python_version()))
        logging.info("Tunez_inner check")
        Tunez_inner(args.query)
    except KeyboardInterrupt:
        sys.exit("\nProgram was closed by the user\n")

if __name__ == '__main__':
    main()




