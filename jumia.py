
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

n = []
pr = []
ra = []
re = []

start = int(input('From Page: '))
end = int(input('To page: '))
urls = []

start_time = time.time()

for x in range(start, end):
    url = f'https://www.jumia.co.ke/all-products/?page={x}#catalog-listing'
    urls.append(url)

print(urls)

async def parse(soup):
    card = soup.find_all('article',attrs = {'class':'prd _fb col c-prd'})
    for c in card:
        #name
        try:
            name = c.find('h3').text
            n.append(name)
        except:
            n.append(np.nan)
        #price
        try:
            price = c.find('div',attrs={'class':'prc'}).text.replace('KSH','')
            pr.append(price)
        except:
            pr.append(np.nan)
        #rating
        try:
            rating = c.find('div',attrs={'class':'rev'}).text
            rating = rating[0:3]
            ra.append(rating)
        except:
            ra.append(np.nan)
        #review
        try:
            review = c.find('div',attrs={'class':'rev'}).text
            review = review[12:17].replace('(','')
            review = review.replace(')','')
            re.append(review)
        except:
            re.append(np.nan)

async def get_data(session, url):
    async with session.get(url) as r:
        html = await r.text()
        soup = BeautifulSoup(html, 'html5lib')
        page = await parse(soup)
        return page

async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_data(session, url))
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    return result

async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(main(urls))
    print(result)

df = pd.DataFrame({
    'Name':n,
    'Price/KSH':pr,
    'Rating':ra,
    'Review':re
})
df.fillna(0)
df.to_csv("Jumia1.csv", index=False)
print(df)

print("--- %s seconds ---" % (time.time() - start_time))