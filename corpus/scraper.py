import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

base_url = "https://films.lk/"

links = []
i = 0
person_id = 0
for page_id in tqdm(range(26)):
    URL = "{}artists.php?page={}".format(base_url, page_id)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    people = soup.find_all("div", class_="column2")
    for person in people:   
        link = person.find("a")["href"]
        links.append(link)   

# with open('artist_links.txt', 'w') as f:
#     for link in links:
#         f.write("%s\n" % link)



# with open('artist_links.txt', 'r') as f:
#     links = f.readlines()

#base_url = "https://translate.google.com/translate?hl=&sl=en&tl=si&u=https%3A%2F%2Ffilms.lk%2F"

for i in tqdm(range(len(links))):
    if i < 164 or i > 173:
        continue
    person = {}
    URL = "{}{}".format(base_url, links[i])
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    person["id"] = i

    try:
        person["name"] = soup.find("span", class_="title").parent.contents[2].strip()
    except:
        person["name"] = ""

    if (person["name"] == ""):
        try:
            person["name"] = soup.find("span", class_="title").text.strip()
        except:
            continue
  
    try:
        person["real_name"] = soup.find("b", string=lambda text: "real name" in text.lower()).parent.text.strip()[12:]
    except:
        person["real_name"] = ""

    try:
        person["birth"] = soup.find("b", string=lambda text: "birthday" in text.lower()).parent.text.strip()[11:].strip()
    except:
        person["birth"] = ""

    try:
        person["death"] = soup.find("b", string=lambda text: "died" in text.lower()).parent.text.strip()[7:].strip()
    except:
        person["death"] = ""

    try:
        bio_div = soup.find("span", class_="eventTitle", string=lambda text: "biography" in text.lower()).parent
        person["bio"] = bio_div.find("p").text.strip()
    except:
        person["bio"] = ""

    person["films"] = []
    try:
        filmography_div = soup.find("span", class_="eventTitle", string=lambda text: "as cast member" in text.lower()).parent
    except:
        pass
    else:
        cast_tbl = filmography_div.find("table")
        tr_list = cast_tbl.find_all("tr")
        for tr in tr_list:
            film = {}
            film_url = tr.find_all("td")[1].a["href"]
            film_page = requests.get(base_url + film_url)
            film_soup = BeautifulSoup(film_page.content, "html.parser")
            try:
                film["title"] = film_soup.find("span", class_="title").parent.contents[1][2:].strip()
            except:
                film["title"] = film_soup.find("span", class_="title").text.strip()

            film["role"] = tr.find_all("td")[1].span.text.strip()
            film["year"] = tr.find_all("td")[2].div.text.strip()
            person["films"].append(film)
        
    try:
        filmography_div = soup.find("span", class_="eventTitle", string=lambda text: "as crew member" in text.lower()).parent
    except:
        pass
    else:
        cast_tbl = filmography_div.find("table")
        tr_list = cast_tbl.find_all("tr")
        for tr in tr_list:
            film = {}
            film_url = tr.find_all("td")[1].a["href"]
            film_page = requests.get(base_url + film_url)
            film_soup = BeautifulSoup(film_page.content, "html.parser")
            try:
                film["title"] = film_soup.find("span", class_="title").parent.contents[1][2:].strip()
            except:
                film["title"] = film_soup.find("span", class_="title").text.strip()
            film["role"] = tr.find_all("td")[1].span.text.strip()
            film["year"] = tr.find_all("td")[2].div.text.strip()
            person["films"].append(film)

    person["awards"] = []
    try:
        awards_parent_div = soup.find("span", class_="eventTitle", string=lambda text: "national awards" in text.lower() and "inter" not in text.lower()).parent
    except:
        pass
    else:
        try:
            awards_list = awards_parent_div.findChildren("div", recursive=False)
            for award_div in awards_list:
                award = {}
                award["title"] = award_div.p.contents[1].strip()
                award["instituition"] = award_div.div.span.a.text.strip()
                person["awards"].append(award)

            awards_list = awards_parent_div.find_all("tr")
            for award_tr in awards_list:
                award = {}
                award["title"] = award_tr.find_all("td")[1].span.text.strip()
                award["instituition"] = award_tr.find_all("td")[1].a.text.strip()
                person["awards"].append(award)
        except AttributeError as e:
            try:
                awards_list = soup.find("span", class_="eventTitle", string=lambda text: "national awards" in text.lower() and "inter" not in text.lower()).find_next("table").find_all("tr")
                for award_tr in awards_list:
                    award = {}
                    award["title"] = award_tr.find_all("td")[1].span.text.strip()
                    award["instituition"] = award_tr.find_all("td")[1].a.text.strip()
                    person["awards"].append(award)
            except:
                pass


    person_jsn = json.dumps(person)
    with open('artists.json', 'a') as f:
        f.write("%s,\n" % person_jsn)