import pymysql, random, xlrd
import jieba
import linklist
pymysql.install_as_MySQLdb()
# 打开数据库连接

def dbconn():
    db = pymysql.connect("39.102.33.86", "root", "Wzk+1998", "search", charset='utf8' )

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "select url from travels"
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
       #print(len(results))
    except:
       print ("Error: unable to fecth data")

    # 关闭数据库连接
    db.close()
    return results

def insert(word,id):
    db = pymysql.connect("39.102.33.86", "root", "Wzk+1998", "search", charset='utf8' )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = 'insert into allwordindex(word,webid) value('+word+','+id+')'
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

from newspaper import Article
def article(url):
    try:
        a=Article(url,language="zh")
        a.download()
        a.parse()
        return a.text
    except:
        pass

        return -1

from jieba import analyse
# 引入TF-IDF关键词抽取接口
# 引入TextRank关键词抽取接口
textrank = analyse.textrank
tfidf = analyse.extract_tags
def keyword(url):

    text =article(url)
    if text==-1:
        return -1
    else:
        # 基于TF-IDF算法进行关键词抽取
        keywords = tfidf(text)
        #print ("keywords by tfidf:")
        # 输出抽取出的关键词
        #for keyword in keywords:
            #print (keyword + "/")
        #keywords = textrank(text)
        return keywords

def cutworf(url):
    text=article(url)
    seg_list=jieba.cut_for_search(text)
    return  seg_list
ignorewords=set(['的','但是','然而','能','在','以及','可以','使','我','我们','大家','高兴','啊','哦'])
ll = linklist.LinkList()
kl = linklist.LinkList()

def index(url,count):
    #words=cutworf(url)
    keys=keyword(url)
    if keys==-1:
        return -1
    dick=list(keys)
    #dicn=list(words)
    # for i in range(len(dicn)):
    #     word = dicn[i]
    #     if word in ignorewords: continue
    #     if ll.getlength() == 0:
    #         wl = linklist.WebList()
    #         wl.initlist(count)
    #         ll.initlist(word, wl)
    #
    #     if ll.getlength() > 0:
    #         i = ll.index(word)
    #         if i == -1:
    #             wl = linklist.WebList()
    #             wl.initlist(count)
    #             ll.append(word, wl)
    #             # print(word)
    #         if i != -1:
    #             j = ll.getwh(i).index(count)
    #             if j == -1:
    #                 ll.getwh(i).append(count)

    for i in range(len(dick)):
        word = dick[i]
        if word in ignorewords: continue
        if kl.getlength() == 0:
            wl = linklist.WebList()
            wl.initlist(count)
            kl.initlist(word, wl)

        if kl.getlength() > 0:
            i = kl.index(word)
            if i == -1:
                wl = linklist.WebList()
                wl.initlist(count)
                kl.append(word, wl)
                # print(word)
            if i != -1:
                j = kl.getwh(i).index(count)
                if j == -1:
                    kl.getwh(i).append(count)
    return 1



if __name__ == '__main__':
    url=dbconn()

    for x in range(len(url)):
        falg=index(url[x][0],x+1)
        if falg==-1:
            continue
        else:
            print(x)
    db = pymysql.connect("39.102.33.86", "root", "Wzk+1998", "search", charset='utf8' )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    for i in range(kl.getlength()):
        word=kl.getdata(i)
        id =''
        for j in range(kl.getwh(i).getlength()):
            part=kl.getwh(i).getdata(j)
            if id =='':
                id=str(part)
            else:
                id=id+','+str(part)
        #print(word)
        #print(id)


        # SQL 插入语句
        sql = "insert into keyword(word,webid) value('" + word + "','" + id + "')"
        #print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
        # 关闭数据库连接
    db.close()
