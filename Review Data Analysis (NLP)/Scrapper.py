import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time


def AssignWebPage(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36', 
    }
    web_url = f"https://www.productreview.com.au/listings/harris-farm-markets?page={page}#reviews"
    #web_url = f"https://www.productreview.com.au/listings/iga?page={page}#reviews"
    web = requests.get(web_url, headers=headers)
    return web

def main():
    publishdate = []
    headline=[]
    comment=[]
    rating=[]

    page = 1
    web = AssignWebPage(page)

    while (web.status_code in range (200,300)):
        soup = BeautifulSoup(web.content, "html.parser")
        script = json.loads(soup.find("script", type = "application/ld+json").string)

        element_count = len(script["review"])

        for i in range (element_count):
            publishdate.append(script["review"][i]["datePublished"])
            headline.append(script["review"][i]["headline"])
            comment.append(script["review"][i]["reviewBody"])
            rating.append(script["review"][i]["reviewRating"]["ratingValue"])
        
        page += 1
        web = AssignWebPage(page)
        time.sleep(5)

    data = pd.DataFrame({    
        "Date": publishdate,
        "Headline": headline,
        "Comment": comment,
        "Rating": rating
    })
    return data

def replace_text(text, new_text, col_name, df):
    df[col_name] = df[col_name].str.replace(text,new_text,case=False)

if __name__ == "__main__":
    data = main()

    #remove company name
    replace_text("harris farm", "company name", "Comment", data)
    replace_text("harris farm", "company name", "Headline", data)
    replace_text("harris", "company name", "Comment", data)
    replace_text("harris", "company name", "Headline", data)

    data.to_csv(".\data.csv")
    print (data)

