import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import os

# Function to fetch a Wikipedia page by URL
def fetch_wikipedia_page(wikiurl):
    header= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br'}

    response = requests.get(wikiurl,headers=header)
    #convert to text string and return 
    return response.text

# Function to update DONE_OR_NOT_DONE status in the database
def db_update(url):
    conn = sqlite3.connect("OlympicsData1.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE SummerOlympics SET Done_or_Not_Done = 1 WHERE WikipediaURL = ('%s')"%(url))
    conn.commit()
    conn.close()
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

def getcount(info_table_rows1):
    for row in info_table_rows1:
      #if(row.th.text=='Athletes'):
      try:
         if(row.th.text=='Athletes'):
              return row.td.text
      except:
          continue
def getsports(all_divs):
    plays=[]
    for d in all_divs:
        rows1=d.find_all('tr')
        header=rows1[0].th
        #print(heading)
        if header is not None:
            heading=header.text
            #print(heading)
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
def getcountry(ranks):
    countries=[]
    
    rows=ranks.find_all('tr')
    for row in rows:
        try:
            x=row.th.a
            countries.append(x.text)
        except:
            continue
    
    return countries
def page_scraping(url):
        link_data = fetch_wikipedia_page(url)
        soup = BeautifulSoup(link_data, 'lxml')
        name=soup.find('head').title.text
        year=re.sub('_Summer_Olympics$', '',url)[-4:]
        host=soup.find('td',class_="infobox-data location")
        if host is not None:
            host=host.a
            if host is not None:
               host=host.text
        tables=soup.find_all('table')
        nations=getNations(tables)
        nations_str=','.join(nations)
        info_table_rows=soup.find('table',class_="infobox")
        if info_table_rows is not None:
            info_table_rows=info_table_rows.find_all('tr')
            participants=getcount(info_table_rows)
            all_divs=soup.find_all('table',class_="wikitable")
            plays=getsports(all_divs)
            plays_str=','.join(plays)
            ranks=soup.find_all('table',class_="wikitable sortable plainrowheaders jquery-tablesorter")
            top_cntry=[]
            #print(type(ranks))
            # 
            
            rows=[]
            for rank in ranks:
                rows=rank.tbody.find_all('tr')
                #print(type(rows))
            for row in rows:
                try:
                    x=row.th.a
                    top_cntry.append(x.text)
                except:
                    continue
            con = sqlite3.connect("OlympicsData1.db")

            cursor = con.cursor()
            try:
                query = "UPDATE  SummerOlympics set Name='%s',Year='%s',HostCity='%s',ParticipatingNations='%s',Athletes='%s',Sports='%s',Rank_1_nation='%s',Rank_2_nation='%s',Rank_3_nation='%s',Done_or_Not_Done='%d' where WikipediaURL='%s'"%(name,year,host,nations_str,participants,plays_str,top_cntry[0],top_cntry[1],top_cntry[2],0,url)
                cursor.execute(query)
            # Implement your parsing logic here
            # Extract the required information from the page and update the corresponding database row

            # Example: Update DONE_OR_NOT_DONE status
            except:
               query = "UPDATE  SummerOlympics set Name='%s',Year='%s',HostCity='%s',ParticipatingNations='%s',Athletes='%s',Sports='%s',Done_or_Not_Done='%d' where WikipediaURL='%s'"%(name,year,host,nations_str,participants,plays_str,0,url)
               cursor.execute(query)
            con.commit()
            con.close()
        db_update(url)

if __name__ == "__main__":
    while True:
        conn = sqlite3.connect("OlympicsData1.db")
        cursor = conn.cursor()
        query="SELECT WikipediaURL FROM SummerOlympics WHERE Done_or_Not_Done = 0 LIMIT 1"
        cursor.execute(query)
        row =cursor.fetchone()
        conn.close()
        if row is None:
            break

        url = row[0]
        
        page_scraping(url)

    print("Scraper script completed.")

    os.system("python3 checker.py&")
    '''conn = sqlite3.connect("OlympicsData1.db")
    cursor = conn.cursor()
    # query="SELECT * FROM SummerOlympics"
    # cursor.execute(query)
    # result=cursor.fetchall()
    # print(len(result))
    # for row in result:
    #      print(row)
    #cursor.execute(query)
    query="SELECT COUNT(*) FROM SummerOlympics WHERE Done_or_Not_Done = 0"
    cursor.execute(query)
    count=cursor.fetchone()[0]
    if count!=0:
        print("all are not populated")
        query="drop table SummerOlympics"
        cursor.execute(query)
    else:
        query="select Year from SummerOlympics"
        result=cursor.execute(query)
        print("years are: ")
        for y in result:
            print(y)

        parti_cnt={}
        query="select Rank_1_nation,Rank_2_nation,Rank_3_nation from SummerOlympics"
        cursor.execute(query)
        rows=cursor.fetchall()
        for row in rows:
            for cntry in row:
                if cntry in parti_cnt:
                    parti_cnt[cntry]+=1
                else:
                    parti_cnt[cntry]=1
        sort_cntry=sorted(parti_cnt.items(), key=lambda x: x[1])
        top_3_nations=sort_cntry[-3:]
        print(top_3_nations)
        query="select ParticipatingNations from SummerOlympics"
        result=cursor.execute(query)
        sum=0
        for nations in result:
            #print(type(nations))
            sum=sum+len(str(nations).split(','))
        print(f"avg number of partipating countries {sum/10}")
        query="drop table SummerOlympics"
        cursor.execute(query)
        conn.close()
        '''