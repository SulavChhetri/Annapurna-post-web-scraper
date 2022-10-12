import requests
from bs4 import BeautifulSoup
import json
import os

headers = {
    'authority': 'bg.annapurnapost.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.6',
    'origin': 'https://annapurnapost.com',
    'referer': 'https://annapurnapost.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}
params = {
    'title': 'चुनाव',
    'page': '1',
}

def writetojsonfile(data):
    with open('./data.json','w',encoding='utf-8') as file:
        json.dump(data, file)

def newsscraper(datalength,data):
    for page in range(datalength+1,5):
        pagelist = []
        r = requests.get('https://bg.annapurnapost.com/api/search', params=params, headers=headers)
        jsonresponse = json.loads(r.content)
        # print(len(jsonresponse['data']['items']))
        for i in range(len(jsonresponse['data']['items'])):
            title = jsonresponse['data']['items'][i]['title']
            content = jsonresponse['data']['items'][i]['content']
            soup = BeautifulSoup(content,'html.parser')
            newscontainer = list()
            contents = soup.find_all('p')
            for news in contents:
                newscontainer.append(news.text)
            finalnewscontent = ' '.join(newscontainer)
            pagelist.append({"title": title, "content":finalnewscontent})
        data.append({"Page No": page, "news":pagelist})
        params['page']= str(page)
        writetojsonfile(data)



def main():
    if os.path.getsize('./data.json')<2:
        writetojsonfile([])
    with open('./data.json','r') as file:
        data = json.load(file)
    newsscraper(len(data),data)


if __name__ == "__main__":
    main()