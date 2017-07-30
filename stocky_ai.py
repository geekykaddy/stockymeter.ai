import watson_developer_cloud
import wikipedia



discovery = watson_developer_cloud.DiscoveryV1(
    '2016-11-07',
    username='username',
    password='password')

environments = discovery.get_environments()
# print(json.dumps(environments, indent=2))


news_environments = [x for x in environments['environments'] if
                     x['name'] == 'Watson News Environment']
news_environment_id = news_environments[0]['environment_id']
# print(json.dumps(news_environment_id, indent=2))

collections = discovery.list_collections(news_environment_id)
news_collections = [x for x in collections['collections']]
# print(json.dumps(collections, indent=2))

configurations = discovery.list_configurations(
    environment_id=news_environment_id)
# print(json.dumps(configurations, indent=2))
default_config_id = discovery.get_default_configuration_id(
    environment_id=news_environment_id)
# print(json.dumps(default_config_id, indent=2))

default_config = discovery.get_configuration(
    environment_id=news_environment_id, configuration_id=default_config_id)
# print(json.dumps(default_config, indent=2))

query_results = ""


def query_brands(brand):
    query_options = {'query': brand}
    global query_results
    query_results = discovery.query(news_environment_id,
                                    news_collections[0]['collection_id'],
                                    query_options)
    #print(json.dumps(query_results, indent=2))

    return (type(query_results))

def influential():
    post = ''
    for i in range(0, 5):
        score = query_results['results'][i]['ac_suggest'][0]
        post += " '"+score+"' "
    return (post)


def topnews():
    topstring = "\n"
    for i in range(0, 4):
        topnews = query_results['results'][i]['title']
        url = query_results['results'][i]['url']
        date = query_results['results'][i]['yyyymmdd']
        topstring = topstring + "News Title: " + topnews + "\n" + "url:" + url + "\n" + "date of the article: " + date + "\n"
    return (topstring)


def senti():
    sentiment = "\n"
    x = '0'
    x = int(x)
    for i in range(0, 9):
        #print(query_results['results'][i])
        result = query_results['results'][i]
        if 'docSentiment' in result:
            pnn = result['docSentiment']['type']
            if pnn != 'neutral':
                    score = result['docSentiment']['score']
                    score = int(100 * float(score))
                    x = x + score
                    #print (x)
           #type = query_results['results'][i]['docSentiment']['type']
           #sentiment = sentiment + "score: " + str(score) + "\n" + "type:" + type + "\n"
    x = str(x/10)
    return (x)


def mostpostive():
    post = []
    for i in range(0, 9):
        result = query_results['results'][i]
        if 'docSentiment' in result:
            pnn = result['docSentiment']['type']
            if pnn != 'neutral':
                score = query_results['results'][i]['docSentiment']['score']
                score = int(100 * float(score))
                post.append(score)

    #print(post)
    confidentscore = max(post)
    #print(confidentscore)
    index = post.index(max(post))
    powerfullnews_title = query_results['results'][index]['title']
    powerfullnews_date = query_results['results'][index]['yyyymmdd']
    powerfullnews_senti = confidentscore
    powerfullnews_language = query_results['results'][index]['language']
    powerfullnews_host = query_results['results'][index]['host']
    powerfullnews_text = query_results['results'][index]['text']
    return (powerfullnews_date,powerfullnews_host,powerfullnews_senti,powerfullnews_title,powerfullnews_text)

def basic(company):
    query_brands(company)
    data = str(wikipedia.summary(company, sentences=2))
    return(data)

# functions

text0 = basic(input("Say the company name stocky should analyse: "))

#function returns
influence = influential()
a = senti()
date, host, senti, title, text = mostpostive()


total = str(query_results['matching_results'])
text1 = "\n     The overall sentiment is " + str(a) + "% which is analyzed from over " + str(total) + " pooled from 300,000 articles and blogs"

text2 = "\n     From this analytics, we have found the powerful message. This message was released on "+ str(date) +" and was hosted by "+ str(host) +". The sentiment of this powerfull message is "+ str(senti) +"%. The title in which this message was released is '"+ str(title) +"' under the text "+ str(text)

text3 = "\n     Based on crunching the colosal data, we have predicted this company stocks depends on the following trademarks: "+influence+". If you are interested to control the stock market share price of this company you should possibly manipulate one of the above fields mentioned above."

text = "\n      " + text0 + "\n" + text1 + "\n" + text2 + "\n" + text3
print(text)
text_file = open("output.txt", "w")
text_file.write(text)
text_file.close()




