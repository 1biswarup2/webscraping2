import requests
import sqlite3
import json
from bs4 import BeautifulSoup
from random import sample 
import re
import time
import os
import multiprocessing
from multiprocessing import process
#start_time = time.time()
'''some times due to netwok error it is showing some error ; if it happens then just re-run'''
def getcount(info_table_rows1):
    for row in info_table_rows1:
      #if(row.th.text=='Athletes'):
      try:
         if(row.th.text=='Athletes'):
              return row.td.text
      except:
          continue
def getNations(tables1):
        nations1=[]
        for table in tables1:
            try:
                header1=table.tbody.tr.th.a.text
                #print(header1)
                if(header1=="National Olympic Committees"):
                    rows=table.tbody.find_all('tr')
                    for row in rows:
                        try:
                            lists=row.td.ul.find_all('li')
                            for li in lists:
                                nations1.append(li.a.text)
                        except:
                            continue
                    #print(name)
            except:
                continue
        return nations1
def getData(url,header):
    response = requests.get(url,headers=header)
    #convert to text string and return 
    return response.text
def getsports(all_divs):
    plays=[]
    for d in all_divs:
        rows1=d.find_all('tr')
        header=rows1[0].th
        #print(heading)
        if header is not None:
            heading=header.text
            print(heading)
            if 'Sports' in heading:
                c=rows1[1].td.div.table.tbody.tr
                cols=c.find_all('td')
                for col in cols:
                    sports=col.ul.find_all('li')
                    for sport in sports:
                        allaq=sport.text.split()
                        for aq in allaq:
                            plays.append(aq)
                        
                        # temp=sport.find('li').text
                        # print(temp)
        else:
         continue
    return  plays

def convertJson(data):
    return json.loads(data)

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur,con
def getcountry(ranks):
    rows=ranks[0].tbody.find_all('tr')
    countries=[]
    for row in rows:
        try:
            x=row.th.a
            countries.append(x.text)
        except:
            continue
    return countries
def run_scraper():
        os.system("python3 scaper.py&")
if __name__=="__main__":
    print("choose 1 for single processing and 2 for multiprocess: ")
    choice=int(input())
    if(choice==2):
        start_time = time.time()
        headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'}

        url ='https://en.wikipedia.org/wiki/Summer_Olympic_Games'
        returnedData = getData(url,headers)
        #print(returnedData)

        dbName = "OlympicsData1.db"
        cursor,con = createDatabaseConnect(dbName)

        query = "CREATE TABLE IF NOT EXISTS SummerOlympics(Name,WikipediaURL,Year,HostCity,ParticipatingNations,Athletes,Sports,Rank_1_nation,Rank_2_nation,Rank_3_nation,Done_or_Not_Done int)"
        cursor.execute(query)

        soup=BeautifulSoup(returnedData,'lxml')
        para=soup.find_all('p')
        links=[]
        for p in para:
            for a in p.find_all('a'):
                links.append(a['href'])
        #print(links)
        olympic_link=[]
        flag=0
        for link in links:
            if 'Summer_Olympics' in link:
                olympic_link.append(link)

        #print(olympic_link)
        cnt=0
        links_derived=[]
        #for i in range(len(olympic_link)):
        while(cnt<10):
            random_link=sample(olympic_link,1)
            year=re.sub('_Summer_Olympics$', '', random_link[0])[-4:]
            #print(year)
            #y=int(year)
            if year>='1968' and year<='2020':
                links_derived.append('https://en.wikipedia.org'+random_link[0])
                cnt+=1

        print(cnt)
        print(links_derived)
        for link in links_derived:
            query="INSERT INTO SummerOlympics (WikipediaURL,Done_or_Not_Done) values('%s','%d')"%(link,0)
            cursor.execute(query)
        # query="SELECT WikipediaURL,Done_or_Not_Done FROM SummerOlympics"
        # cursor.execute(query)
        # result=cursor.fetchall()
        #print(len(result))
        # for row in result:
        #      print(row)
        con.commit()
        con.close()

        # def run_scraper():
        #   os.system("python scaper.py&")

        #start_time = time.time()
        processes=[]
        for _ in range(3):
        #version=""
            process = multiprocessing.Process(target=run_scraper)
            processes.append(process)
            process.start()

        for process in processes:
            process.join()
        # print("which command runs in your machine: python or python3: ")
        # command=input()
        # os.system(f"{command} scaper.py&")
        dbName = "OlympicsData1.db"
        cursor,con = createDatabaseConnect(dbName)
        query="drop table SummerOlympics"
        cursor.execute(query)
        con.commit()
        con.close()
        print("--- %s seconds ---" % (time.time() - start_time))
    if(choice==1):
        start_time = time.time()
        headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'}

        url ='https://en.wikipedia.org/wiki/Summer_Olympic_Games'
        returnedData = getData(url,headers)
        #print(returnedData)

        dbName = "OlympicsData1.db"
        cursor,con = createDatabaseConnect(dbName)

        query = "CREATE TABLE IF NOT EXISTS SummerOlympics(Name,WikipediaURL,Year,HostCity,ParticipatingNations,Athletes,Sports,Rank_1_nation,Rank_2_nation,Rank_3_nation,Done_or_Not_Done int)"
        cursor.execute(query)

        soup=BeautifulSoup(returnedData,'lxml')
        para=soup.find_all('p')
        links=[]
        for p in para:
            for a in p.find_all('a'):
                links.append(a['href'])
        #print(links)
        olympic_link=[]
        flag=0
        for link in links:
            if 'Summer_Olympics' in link:
                olympic_link.append(link)

        #print(olympic_link)
        cnt=0
        links_derived=[]
        #for i in range(len(olympic_link)):
        while(cnt<10):
            random_link=sample(olympic_link,1)
            year=re.sub('_Summer_Olympics$', '', random_link[0])[-4:]
            #print(year)
            #y=int(year)
            if year>='1968' and year<='2020':
                links_derived.append('https://en.wikipedia.org'+random_link[0])
                cnt+=1

        print(cnt)
        print(links_derived)
        for link in links_derived:
            query="INSERT INTO SummerOlympics (WikipediaURL,Done_or_Not_Done) values('%s','%d')"%(link,0)
            cursor.execute(query)
        # query="SELECT WikipediaURL,Done_or_Not_Done FROM SummerOlympics"
        # cursor.execute(query)
        # result=cursor.fetchall()
        #print(len(result))
        # for row in result:
        #      print(row)
        con.commit()
        con.close()
        os.system("python3 scaper.py&")
        dbName = "OlympicsData1.db"
        cursor,con = createDatabaseConnect(dbName)
        query="drop table SummerOlympics"
        cursor.execute(query)
        con.commit()
        con.close()
        print("--- %s seconds ---" % (time.time() - start_time))
