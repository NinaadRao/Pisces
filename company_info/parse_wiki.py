import requests
from bs4 import BeautifulSoup


def get_wiki_summary(page_soup):
    summary = ""
    paragraphs = page_soup.findAll()
    for paragraph in paragraphs:
        if paragraph.name == "p":
            summary += paragraph.text + " "
            print("Adding summary")
        elif paragraph.name == "div" and paragraph.has_attr('class') and paragraph['class'][0] == 'toc':
            break

    print(summary)
    return summary


def get_wiki_company_categories(page_soup):
    categories = []
    table_html = str(page_soup.find("table", {"class": "infobox vcard"}))
    if table_html == "None":
        print("Returning none")
        return categories
    soup_table = BeautifulSoup(table_html, 'html.parser')
    td_list = soup_table.findAll("td", {"class": "category"})

    for item in td_list:
        if item.previous_sibling is not None and item.previous_sibling.text == "Industry":
            a_tag_list = BeautifulSoup(str(item), 'html.parser').findAll("a")
            for tag in a_tag_list:
                categories.append(tag.text)

    print(categories)
    return categories


def get_wiki_info(page_title):
    response = requests.get("https://en.wikipedia.org/wiki/" + page_title)

    if response.status_code != 200:
        return [None, None]
    page_html = response.content
    page_soup = BeautifulSoup(page_html, 'html.parser')

    summary = get_wiki_summary(page_soup)

    categories = get_wiki_company_categories(page_soup)

    return [summary, categories]
