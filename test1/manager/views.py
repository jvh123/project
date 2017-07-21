from django.shortcuts import render
from manager.forms import SearchForm,PlanForm
import requests
from bs4 import BeautifulSoup
import re
from manager.models import Rank1,Price,Rank2,Yearprice,AuthUser
from subcribers.models import Subscrpber

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader.data as web
from sklearn import neighbors, svm
from sklearn.ensemble import RandomForestClassifier
#####################################
def CompanyGuide(request):
    form = SearchForm()
    return render(request, 'news/CompanyGuide.html')
#####################################
def usa(request):
    form = SearchForm()
    return render(request, 'news/usa.html')
#####################################
def newsview(request):
    jpgurl = []
    harder = []
    url = []
    values = []
    newsvalue = []
    value = []
    newsvalue = []
    newscompany = []
    date = []
    time = []
    datetime=[]
    form = SearchForm()
    pt = re.compile('[\t\n]')
    ptt = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣]')
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            keyword =form.cleaned_data['Search']
        ##################################인코딩 부분
        if ptt.match(keyword) :
            a = keyword.encode('MS949')
            a = a.decode('MS949').encode('MS949')
            a = str(a).replace("\\", "").replace("'", "").split("x")
            search = ""
            for i in a[1:]:
                a = i.upper()
                search = search + '%' + a
        else:
            search=keyword
        ######################################

        for i in range(1):
            i = i + 1
            url1 = 'http://finance.naver.com/news/news_search.nhn?q=%s' % search + '&page=%d' % i
            plain_text = requests.get(url1).text
            print(url1)
            #soup = BeautifulSoup(plain_text, 'lxml')
            soup = BeautifulSoup(plain_text, 'html.parser')
            ranks = soup.find('div', {'class': 'newsSchResult'})
            for keywordss in ranks.findAll(class_=re.compile('articleSubject')):
                p = 0
                harder.append(keywordss.a.text)
                url.append('http://finance.naver.com'+keywordss.a['href'])
                for keywords in ranks.findAll(class_=re.compile('thumb')):
                    if keywordss.a['href'] == keywords.a['href']:
                        jpgurl.append(keywords.a.img['src'])
                        p = 1
                if p == 0:
                    jpgurl.append('')
            for keywords in ranks.findAll(class_=re.compile('articleSummary')):
                values=(list(filter(lambda x: x != '', pt.split(keywords.text))))
                value.append(values[0])
                newscompany.append(values[1])
                date.append(values[4])
                time.append(values[5])
            for b in range(len(harder)):
                newsvalue.append(
                    {'harder':harder[b], 'url':url[b], 'jpgurl':jpgurl[b],
                     'value':value[b],'newscompany':newscompany[b],
                     'date':date[b],'time':time[b]})
            print(values[0])
        documents=newsvalue
        return render(
            request,
            'news/newsview.html',
            {'documents':documents, 'form': form}
        )

    for i in range(1):
        i = i + 1
        url1 = 'http://finance.naver.com/news/mainnews.nhn'
        plain_text = requests.get(url1).text
        print(url1)
        # soup = BeautifulSoup(plain_text, 'lxml')
        soup = BeautifulSoup(plain_text, 'html.parser')
        ranks = soup.find('div', {'class': 'mainNewsList'})
        for keywordss in ranks.findAll(class_=re.compile('articleSubject')):
            p = 0
            harder.append(keywordss.a.text)
            url.append('http://finance.naver.com' + keywordss.a['href'])
            for keywords in ranks.findAll(class_=re.compile('thumb')):
                if keywordss.a['href'] == keywords.a['href']:
                    jpgurl.append(keywords.a.img['src'])
                    p = 1
            if p == 0:
                jpgurl.append('')
        for keywords in ranks.findAll(class_=re.compile('articleSummary')):
            values = (list(filter(lambda x: x != '', pt.split(keywords.text))))
            value.append(values[0])
            newscompany.append(values[1])
            datetime.append(values[3])
        for b in range(len(harder)):
            newsvalue.append(
                {'harder': harder[b], 'url': url[b], 'jpgurl': jpgurl[b],
                 'value': value[b], 'newscompany': newscompany[b],
                 'datetime': datetime[b]})
        print(value[1])
    documents = newsvalue
    return render(
        request,
        'news/newsview.html',
        {'documents': documents, 'form': form}
    )
#####################################
def plans(request):
    yearprice = Yearprice.objects.values_list()
    if request.method=="POST":
        form = PlanForm(request.POST,request.FILES)
        if form.is_valid():
            plan = form.cleaned_data['Plan1']
        Rank=Rank1.objects.values(plan)
        ranks=[]
        for i in Rank:
            if i[plan]!=0:
                ranks.append(i[plan])
        Prices = Price.objects.values('name',plan).filter(name__in=ranks)
        documents=[]
        a=0
        ranknum=0
        for i in Prices:
            ranknum+=1
            documents.append({'name':i['name'],'price':i[plan],'ranknum':ranknum})
            a+=i[plan]
        if a!=0:
            a=a/len(Prices)
        return render(
            request,
            'Rank1/plan1.html',
            {'documents':documents,'a':a,'yearprice':yearprice[0][1:],'form':form}
        )
    else:
        form = PlanForm(request.POST)
        return render(
            request,
            'Rank1/plan1.html',
            {'form': form,'yearprice':yearprice[0][1:]}
        )
#####################################
def plans2(request):
    yearprice = Yearprice.objects.values_list()
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.cleaned_data['Plan1']
        Rank = Rank2.objects.values(plan)
        ranks = []
        for i in Rank:
            if i[plan] != 0:
                ranks.append(i[plan])

        Prices = Price.objects.values('name', plan).filter(name__in=ranks)
        documents = []
        a = 0
        ranknum = 0
        for i in Prices:
            ranknum += 1
            if i[plan] !=-1.0:
                documents.append({'name': i['name'], 'price': i[plan],'ranknum':ranknum})
                a += i[plan]
        if a != 0:
            a = a / len(Prices)
        return render(
            request,
            'Rank1/plan2.html',
            {'documents': documents, 'a': a,'yearprice':yearprice[1][1:], 'form': form}
        )
    else:
        form = PlanForm(request.POST)
        return render(
            request,
            'Rank1/plan2.html',
            {'form': form,'yearprice':yearprice[1][1:]}
        )
#####################################
def viewplan(request):
    # KNN Machine Learning Strategy


    def price(stock, start):
        price = web.DataReader(name=stock, data_source='yahoo', start=start)['Adj Close']
        return price.div(price.iat[0]).resample('M').last().to_frame('price')

    def fractal(a, p):
        df = pd.DataFrame()
        for count in range(1, p + 1):
            a['direction'] = np.where(a['price'].diff(count) > 0, 1, 0)
            a['abs'] = a['price'].diff(count).abs()
            a['volatility'] = a.price.diff().abs().rolling(count).sum()
            a['fractal'] = a['abs'] / a['volatility'] * a['direction']
            df = pd.concat([df, a['fractal']], axis=1)
        return df

    a = price('^KS11', '2000-01-01')
    a['cash'] = [(1.03 ** (1 / 12)) ** x for x in range(len(a.index))]
    a['meanfractal'] = pd.DataFrame(fractal(a, 12)).sum(1, skipna=False) / 12
    a['rollingstd'] = a.price.pct_change().shift(1).rolling(12).std()
    a['result'] = np.where(a.price > a.price.shift(1), 1, 0)
    a = a.dropna()

    clf = neighbors.KNeighborsClassifier(n_neighbors=3)
    clf1 = svm.SVC()
    clf3 = RandomForestClassifier(n_estimators=5)

    a['predicted'] = pd.Series()
    predictions = []
    for i in range(12, len(a.index)):
        x = a.iloc[i - 12:i, 6:8]
        y = a['result'][i - 12:i]
        clf.fit(x, y)
        a['predicted'][i] = clf.predict(x)[-1]
        #     print(clf.predict(x)[-1])
        predictions.append(clf.predict(x)[-1])

    x1 = a.iloc[len(a.index) - 12:len(a.index), 6:8]
    fit4 = clf.predict(x1)[-1]

    a = a.dropna()
    a.price = a.price.div(a.price.ix[0])

    accuracy = clf.score(a.iloc[:, 6:8], a['result'])

    a['Aggresive'] = np.where(a.predicted.shift(1) == 1, ((a.price / a.price.shift(1)) * 0.7 + (1.0026) * 0.3),
                              1.0026).cumprod()
    a[['Aggresive', 'price']].plot()
    plt.show()
    print("Predicted model accuracy: " + str(accuracy)[2:4] + "%")

    period = len(a.index) / 12

    md = a.price.rolling(min_periods=1, window=500).max()
    pmd = a.price / md - 1.0
    mdd = pmd.rolling(min_periods=1, window=500).min()

    pmd.plot(subplots=True, figsize=(8, 2), linestyle='dotted')
    mdd.plot(subplots=True, figsize=(8, 2), color='red')


    # print("\nMDD : " + str(mdd.min() * 100)[0:5] + "%")
    # print("CAGR : " + str(a.price[-1] ** (1 / period) * 100 - 100)[0:4] + "%")

    # print('\nFor next Month:')
    # print('Do Invest') if fit4 == 1 else print('wait for next chance')

    plot = figure()
    plot.circle([1, 2], [3, 4])

    script, div = components(plot, CDN)
    return render(
        requests,
        'Rank1/viewplan.html',
        {'response':script}

    )
#####################################
def email(request):
    useremaillist=[]
    a=Subscrpber.objects.filter(email_check=1)
    for i in a:
        p=AuthUser.objects.get(id=i.user_rec_id)
        useremaillist.append([i.event1,i.event2,i.event3,p.email])

    pt = re.compile('[\t\n]')
    ptt = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣]')

    for event in useremaillist:
        newsvalue = []
        emailcount = 0
        for i in event:
            emailcount += 1
            print(i)
            if emailcount != 4:
                harder = []
                url = []
                values = []
                newscompany = []
                if ptt.match(i):
                    a = i.encode('MS949')
                    a = a.decode('MS949').encode('MS949')
                    a = str(a).replace("\\", "").replace("'", "").split("x")
                    search = ""
                    for j in a[1:]:
                        a = j.upper()
                        search = search + '%' + a
                else:
                    search = i
                print(search)
                i = 1
                url1 = 'http://finance.naver.com/news/news_search.nhn?q=%s' % search + '&page=%d' % i
                plain_text = requests.get(url1).text
                print(url1)
                soup = BeautifulSoup(plain_text, 'html.parser')
                ranks = soup.find('div', {'class': 'newsSchResult'})
                for keywordss in ranks.findAll(class_=re.compile('articleSubject')):
                    count3 = 0
                    harder.append(keywordss.a.text)
                    url.append('http://finance.naver.com' + keywordss.a['href'])
                for keywords in ranks.findAll(class_=re.compile('articleSummary')):
                    if count3 != 3:
                        values = (list(filter(lambda x: x != '', pt.split(keywords.text))))
                        newscompany.append(values[1])
                    else:
                        break
                    count3 += 1
                for b in range(len(newscompany)):
                    newsvalue.append(
                        {'harder': harder[b], 'url': url[b], 'newscompany': newscompany[b]}
                    )
            else:
                sender = "jvh3285@gmail.com"
                toAddrList = [i]

                msg = MIMEMultipart('alternative')
                # msg = MIMEText(text, _charset='utf8')
                msg['Subject'] = "충환 test email"
                msg['From'] = sender
                msg['To'] = ",".join(toAddrList)

                text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
                html = """
                <html>
                    <head></head>
                        <body>
                        <div style='background-color: #f5f5f5; padding: 0 16px 0 16px;'>
                            <div style='padding-top: 12px; padding-bottom: 12px; width: 100%; text-align: center;'>
                                    <p>트리플j</p>
                            </div>

                            <div style='max-width: 612px; margin: 16px auto;'></div>
                            <div style='max-width: 612px; border-radius: 2px; background-color: rgb(250, 250, 250); padding: 8px 24px 24px; margin: 0px auto;'>
                                <h3 style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 16px; font-weight: 400; color: #202020;'>
                                            """ + event[0] + """
                                </h3>
                                <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[0]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[0]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[0]['newscompany'] + """
                                    </b>
                                </p>
                                    <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[1]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[1]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[1]['newscompany'] + """
                                    </b>
                                </p>
                                    <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[2]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[2]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[2]['newscompany'] + """
                                    </b>
                                </p>
                            </div>
                            <div style='max-width: 612px; margin: 16px auto;'></div>

                            <div style='max-width: 612px; margin: 16px auto;'></div>
                            <div style='max-width: 612px; border-radius: 2px; background-color: rgb(250, 250, 250); padding: 8px 24px 24px; margin: 0px auto;'>
                                <h3 style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 16px; font-weight: 400; color: #202020;'>
                                            """ + event[1] + """
                                </h3>
                                <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[3]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[3]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[3]['newscompany'] + """
                                    </b>
                                </p>
                                    <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[4]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[4]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[4]['newscompany'] + """
                                    </b>
                                </p>
                                    <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[5]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[5]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[5]['newscompany'] + """
                                    </b>
                                </p>
                            </div>
                            <div style='max-width: 612px; margin: 16px auto;'></div>

                            <div style='max-width: 612px; margin: 16px auto;'></div>
                            <div style='max-width: 612px; border-radius: 2px; background-color: rgb(250, 250, 250); padding: 8px 24px 24px; margin: 0px auto;'>
                                <h3 style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 16px; font-weight: 400; color: #202020;'>
                                            """ + event[2] + """
                                </h3>
                                <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[6]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[6]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[6]['newscompany'] + """
                                    </b>
                                </p>
                                    <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[7]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[7]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[7]['newscompany'] + """
                                    </b>
                                </p>
                                    <p style='font-family: NanumBarunGothic, Helvetica, Arial, Sans-serif; font-size: 13px; line-height: 1.9; color: #727272;'>
                                    <a href='""" + newsvalue[8]['url'] + """',target='_blank',style='color: rgb(185, 140, 81); line-: 1.2; text-decoration: none; border-bottom: 1px solid rgb(185, 140, 81); display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[8]['harder'] + """
                                    </a>&nbsp;&nbsp;
                                    <b target='_blank',style='color: rgb(170, 170, 170); font-size: 11px; line-: 1.2; display: inline-block; margin-bottom: 8px;'>
                                        """ + newsvalue[8]['newscompany'] + """
                                    </b>
                                </p>
                            </div>
                            <div style='max-width: 612px; margin: 16px auto;'></div>

                            <div style='padding-top: 12px; padding-bottom: 12px; width: 100%; text-align: center;'></div>
                        </div>
                        </body>
                </html>"""

                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(html, 'html')

                msg.attach(part1)
                msg.attach(part2)

                ss = smtplib.SMTP('smtp.gmail.com', 587)
                ss.set_debuglevel(1)
                ss.ehlo()
                ss.starttls()
                ss.ehlo()
                ss.login(sender, 'wjd3285!')
                ss.sendmail(sender, toAddrList, msg.as_string())
                ss.close()
    return render(
        request,
        'mainhome.html'
    )
#####################################
def viewplan(request):

    # def price(stock, start):
    #     price = web.DataReader(name=stock, data_source='yahoo', start=start)['Adj Close']
    #     return price.div(price.iat[0]).resample('M').last().to_frame('price')
    #
    # def fractal(a, p):
    #     df = pd.DataFrame()
    #     for count in range(1, p + 1):
    #         a['direction'] = np.where(a['price'].diff(count) > 0, 1, 0)
    #         a['abs'] = a['price'].diff(count).abs()
    #         a['volatility'] = a.price.diff().abs().rolling(count).sum()
    #         a['fractal'] = a['abs'] / a['volatility'] * a['direction']
    #         df = pd.concat([df, a['fractal']], axis=1)
    #     return df
    #
    # a = price('^KS11', '2000-01-01')
    # a['meanfractal'] = pd.DataFrame(fractal(a, 12)).sum(1, skipna=False) / 12
    # a['rollingstd'] = a.price.pct_change().shift(1).rolling(12).std()
    # a['result'] = np.where(a.price > a.price.shift(1), 1, 0)
    # a = a.dropna()
    #
    # clf = neighbors.KNeighborsClassifier(n_neighbors=3)
    # clf1 = svm.SVC()
    # clf3 = RandomForestClassifier(n_estimators=5)
    #
    # a['predicted'] = pd.Series()
    # predictions = []
    # for i in range(12, len(a.index)):
    #     x = a.iloc[i - 12:i, 6:8]
    #     y = a['result'][i - 12:i]
    #     clf.fit(x, y)
    #     a['predicted'][i] = clf.predict(x)[-1]
    #     #     print(clf.predict(x)[-1])
    #     predictions.append(clf.predict(x)[-1])
    #
    # x1 = a.iloc[len(a.index) - 12:len(a.index), 6:8]
    # fit4 = clf.predict(x1)[-1]
    #
    # a = a.dropna()
    # a.price = a.price.div(a.price.ix[0])
    #
    # accuracy = clf.score(a.iloc[:, 6:8], a['result'])
    #
    # a['Aggresive'] = np.where(a.predicted.shift(1) == 1, ((a.price / a.price.shift(1)) * 0.7 + (1.0033) * 0.3),
    #                           1.0026).cumprod()
    # a[['Aggresive', 'price']].plot()
    # plt.savefig('templates/Rank1/png/knn1.png')
    # Predicted="Predicted model accuracy: " + str(accuracy)[0:4] + "%"
    #
    # period = len(a.index) / 12
    #
    # md = a.price.rolling(min_periods=1, window=500).max()
    # pmd = a.price / md - 1.0
    # mdd = pmd.rolling(min_periods=1, window=500).min()
    #
    # pmd.plot(subplots=True, figsize=(8, 2), linestyle='dotted')
    #
    # mdd.plot(subplots=True, figsize=(8, 2), color='red')
    # plt.savefig('templates/Rank1/png/knn2.png')
    #
    # MDD="\nMDD : " + str(mdd.min() * 100)[0:5] + "%"
    # CAGR="CAGR : " + str(a.price[-1] ** (1 / period) * 100 - 100)[0:4] + "%"
    #
    # print('\nFor next Month:')
    # print('Do Invest') if fit4 == 1 else print('wait for next chance')

    return render(
        request,
        'Rank1/viewplan.html'
    )
