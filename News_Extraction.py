import re
import time
from news_config import *
from bs4 import BeautifulSoup
from urllib import request


def articleHTML(url):
    """Returns html soup."""
    html = request.urlopen(url).read().decode("utf8")
    soup = BeautifulSoup(html, "html.parser")
    return(soup)


def articleURLs(soup, url_count):
    """Returns article urls of a certain news category."""
    st = "http://www.straitstimes.com"
    hrefs = str(soup.find_all(
        "span", class_="story-headline", limit=url_count))
    urls = re.findall('href=\"(.*?)\"', hrefs)
    urls = [st+url for url in urls if urls and "javascript" not in url]
    urls = [url for url in urls if "multimedia/" not in url]
    return(urls)


def urlCategory(url):
    """Returns an article's category from its url."""
    pattern = "straitstimes.com/(\w*)/"
    cat = re.search(pattern, url)
    if cat:
        cat = cat.group(1).title()
        return(cat)
    else:
        return(None)



def articleTitle(soup):
    """Returns news title.
    """
    title = soup.find("h1", class_="headline node-title")
    title = title.string
    return(title)


def articleJavaScript(soup):
    """Returns article's html (script tag).
    """
    script = str(soup.find_all("script"))
    return(script)



def articleDateTime(js):
    """Returns publication date and time (yyyy:mm:dd hh:mm) of news.
    """
    target = '"pubdate":"(.*)"'
    pubdate = re.search(target, js)
    if pubdate:
        return(pubdate.group(1).split(" "))



def articleDate(pub_datetime):
    """Returns article's published datetime.
    """
    pubdate = pub_datetime[0]
    date = pubdate.split("-")

    year, month, day = date[0], date[1], date[2]

    months = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Oct", "10": "Sep", "11": "Nov", "12": "Dec"}

    month_name = months.get(month)
    pub_date = "{} {} {}".format(day, month_name, year)
    return(pub_date)




def Main(todays_news):

    date_today = time.strftime("%d %b %Y")  # dd mmm yyyy

    print("  Collecting news for {}.\n".format(date_today))

    # statistics and counters
    reduction = []
    summarized = 0
    articles_fetched = 0

    # news categories
    print("  Categories fetched: {}".format(len(st_categories)))
    for (cat, cat_url, filename) in st_categories:
        print("\t[{}]".format(cat))

    # urls of articles for each category
    st_cats_urls = []
    for (cat, cat_url, filename) in st_categories:
        urls = articleURLs(articleHTML(cat_url), headline_count)
        st_cats_urls.append((urls, cat, filename))
        articles_fetched += len(urls)
    print("\n  Articles fetched: {}\n".format(articles_fetched))

    st_articles = [urls for urls in st_cats_urls]
    #print(st_articles)
    with open('OCBC_NEWS.txt', "w", encoding="utf8") as file:
        for (urls, cat, filename) in st_articles:
            for url in urls:

                    file.write('########################################################################\n')
                    file.write('\nSource : Strait Times\n')
                    file.write('Date : ' + str(articleDate(articleDateTime(articleJavaScript(articleHTML(url)))))+'\n')
                    file.write('Headline : ' + articleTitle(articleHTML(url)) + '\n')
                    file.write('Link : ' + url + '\n')
                    file.write('\n########################################################################\n')
                    print(articleTitle(articleHTML(url)))
                    print(articleDate(articleDateTime(articleJavaScript(articleHTML(url)))))

if __name__ == "__main__":
    Main(False)