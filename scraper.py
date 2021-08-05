import requests
from bs4 import *
import string
import os

page_number = int(input("> "))
article_type = str(input("> "))

saved_articles = []

i = 1

while i <= page_number:

    path = os.path.join(os.getcwd(), "Page_{}".format(i))

    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

    # type_folder = os.path.join(path, article_type)
    # if not os.path.exists(type_folder):
    #     os.mkdir(article_type)

    os.chdir(path)

    r = requests.get("https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={}".format(i))
    soup = BeautifulSoup(r.content, "html.parser")

    for item in soup.find_all("article", {"class": "u-full-height c-card c-card--flush"}):
        if item.find("span", {"class": "c-meta__type"}).text == article_type:

            link = "https://www.nature.com" + str(item.a.get("href"))
            r2 = requests.get(link)

            article_soup = BeautifulSoup(r2.content, "html.parser")

            if article_type == "Article":
                try:
                    header = article_soup.find("div", {"class": "c-article-header"}).h1.text.strip()
                    teaser = ""
                    body = article_soup.find("div", {"class": "c-article-section__content"}).text.strip()

                except AttributeError:
                    break

            elif article_type == "Research Highlight":
                try:
                    header = article_soup.find("header", {"class": "article-item__header"}).h1.text.strip()
                    teaser = article_soup.find("div", {"class": "article-item__teaser-text"}).text.strip()
                    body = article_soup.find("div", {"class": "article-item__body"}).text.strip()

                except AttributeError:
                    break
            else:
                try:
                    header = article_soup.find("div", {"class": "c-article-header"}).h1.text.strip()
                    teaser = article_soup.find("div", {"class": "c-article-teaser-text"}).text.strip()
                    body = article_soup.find("div", {"class": "c-article-body u-clearfix"}).text.strip()

                except AttributeError:
                    break

            content = header + "\n" + teaser + "\n" + body

            translation_table = str.maketrans("", "", string.punctuation)
            format_file_name = header.translate(translation_table)

            file_name = "{}.txt".format(format_file_name.replace(" ", "_"))
            saved_articles.append(file_name)

            file = open(file_name, "wb")
            file.write(bytes(content, encoding="UTF-8"))
            file.close()

    os.chdir(os.path.dirname(path))
    i += 1

print("Saved all articles: ", saved_articles)
