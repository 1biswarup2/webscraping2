import sqlite3

conn = sqlite3.connect("OlympicsData1.db")
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
    # query="drop table SummerOlympics"
    # cursor.execute(query)
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
    query="select Athletes from SummerOlympics"
    result=cursor.execute(query)
    sum=0
    for ath in result:
        #print(ath[0])
        cnt=ath[0]
        num=""
        if cnt is not None and cnt !='None':
            for c in cnt:
                if c=='[' or c=='(':
                    break
                num+=c
        else:
            num="0"
        
        num=num.strip()
        num=num.replace(',','')
        if num is not None:
            #print(num)
            num=int(str(num))
            sum=sum+num
    print(f"avg number of partipating athletes {sum/10}")
    # query="drop table SummerOlympics"
    # cursor.execute(query)
    conn.close()