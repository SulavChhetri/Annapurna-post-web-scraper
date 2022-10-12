import requests
import json
import os


#The headers, params are created after converting the cURL(bash) api into python from where the url for api can be used
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

#function for writing the data into data.json
def writetojsonfile(data):
    with open('./data.json','w',encoding='utf-8') as file:
        json.dump(data, file)

# datalength is used to measure the no of page that have been scraped, data is the existing scraped json file in which page that are already scraped are left behind and the page that aren't scraped are scraped and updated to the data
def newsscraper(datalength,data):
    pageno = int(datalength/10)
    #if we have pageno = 1, we have already scraped 1st page, so we can start scraping from 2nd page using the below for loop
    #and we only scrape through 3 pages, i.e. 30 articles and the news article beyond the 3rd page aren't that useful compared to first pages
    for page in range(pageno+1,4):
        #the parameter params contains key called 'page' which is changed to get news article from different page
        r = requests.get('https://bg.annapurnapost.com/api/search', params=params, headers=headers)
        #loading the data from the above url into json form
        jsonresponse = json.loads(r.content)
        print(jsonresponse['status'])
        #if the api request is successful, we scrape the data, else, we just increase the page number and scrape the data from next page
        if jsonresponse['status']=='success':
            for i in range(len(jsonresponse['data']['items'])):
                title = jsonresponse['data']['items'][i]['title']
                content = jsonresponse['data']['items'][i]['content']
                data.append({"news":{"title": title, "content":content}})
            params['page']= str(page)
        else:
            params['page']= str(page)
    #finally the data scraped that is stored in the list data is dumped to the data.json file
    writetojsonfile(data)



def main():
    #if the data.json is null, an empty list is updated to the data.json file
    if os.path.getsize('./data.json')<2:
        writetojsonfile([])
    with open('./data.json','r') as file:
        data = json.load(file)
    print(len(data))
    #In one page in annapurnapost.com, there are exactly 10 articles, so, we can use the length of the data to measure if the no of pages
    #that have been scraped. For e.g: if the len(data)=2, two pages have been scraped, so we only need to scrape page 3 only
    newsscraper(len(data),data)


if __name__ == "__main__":
    main()