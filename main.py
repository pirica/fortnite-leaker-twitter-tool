import json
import os
import time

import requests

try:
    import tweepy
except ImportError:
    os.system('python -m pip install tweepy')
    try:
        import tweepy
    except ImportError:
        print("Please install the Python Package: tweepy")

import settings.SETTINGS as SETTINGS
import settings.MODULES as MODULES


def check_leaks():
    try:
        with open('Cache/leaks.json', 'r') as file:
            Cached = json.load(file)
        data = requests.get('https://peely.de/api/leaks/lastupdate')
        new = data.json()
        if data.status_code != 200:
            return
    except Exception as ex:
        print(ex, "leaks")
        return
    if new != Cached:
        MODULES.tweet_image(url=f"https://peely.de/leaks", message=f"New Cosmetics found!\n#Fortnite")
        with open('Cache/leaks.json', 'w') as file:
            json.dump(new, file, indent=3)
        print("Leaks posted")


def check_shop():
    try:
        with open('Cache/shop.json', 'r') as file:
            Cached = json.load(file)
        data = requests.get('https://peely.de/api/shop/lastupdate')
        new = data.json()
        if data.status_code != 200:
            return
    except:
        return
    if new != Cached:
        MODULES.tweet_image(url=new["discordurl"], message=f"New Shop detected!\n#Fortnite")
        with open('Cache/shop.json', 'w') as file:
            json.dump(new, file, indent=3)
        print("Item Shop posted")


def other():
    try:
        with open('Cache/content.json', 'r') as file:
            Cached = json.load(file)
        data = requests.get('https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game')
        new = data.json()
        if data.status_code != 200:
            return
    except:
        return
    if new["emergencynotice"]["news"]["messages"] != Cached["emergencynotice"]["news"]["messages"]:
        for i in new["emergencynotice"]["news"]["messages"]:
            if i not in Cached["emergencynotice"]["news"]["messages"]:
                title = i["title"]
                body = i["body"]
                MODULES.post_text(text=f"{title}\n{body}\n#Fortnite")
        print("emergencynotice postet")
    with open('Cache/content.json', 'w') as file:
        json.dump(new, file)


def blogpost():
    try:
        with open('Cache/blog.json', 'r', encoding="utf8") as file:
            Cached = json.load(file)
        data = requests.get(
            'https://www.epicgames.com/fortnite/api/blog/getPosts?category=&postsPerPage=6&offset=0&locale=en-US')
        new = data.json()
        if data.status_code != 200:
            return
    except:
        return
    if Cached["blogList"] != new["blogList"]:
        print("Blog Update")
        for i in new["blogList"]:
            old = False
            for i2 in Cached["blogList"]:
                if i["title"] == i2["title"]:
                    old = True
            if old is True:
                continue
            else:
                str = ""
                str += i["shareDescription"]
                str += "\n"
                str += f'https://www.epicgames.com/fortnite/{i["urlPattern"]}'
                MODULES.tweet_image(url=i["image"], message=str)
        with open('Cache/blog.json', 'w', encoding="utf8") as file:
            json.dump(new, file)


def staging():
    try:
        with open('Cache/staging.json', 'r', encoding="utf8") as file:
            Cached = json.load(file)
        data = requests.get(
            'https://fortnite-public-service-stage.ol.epicgames.com/fortnite/api/version')
        new = data.json()
        if data.status_code != 200:
            return
    except:
        return
    if Cached["version"] != new["version"]:
        print("Staging Server Updated")
        MODULES.post_text(text=f"Patch v{new['version']} was applied to the staging servers.\n\n"
                               f"You can expect we'll get v{new['version']} next week.")
        with open('Cache/staging.json', 'w', encoding="utf8") as file:
            json.dump(new, file)


def hotfixes():
    with open('Cache/hotfix.json', 'r', encoding="utf8") as file:
        old = json.load(file)
    try:
        req = requests.get("https://benbotfn.tk/api/v1/hotfixes")
        if req.status_code != 200:
            return
        new = req.json()
    except:
        return
    list = []
    try:
        for i in new[""]:
            list.append(new[""][i])
        if old != list:
            print("NEW HOTFIXES")
            for i in list:
                if i not in old:
                    MODULES.post_text(text=f"New Hotfix: \n\n{i}")
            with open('Cache/hotfix.json', 'w', encoding="utf8") as file:
                json.dump(list, file)
    except:
        return


def news():
    with open('Cache/news.json', 'r', encoding="utf8") as file:
        old = json.load(file)
    try:
        req = requests.get("https://fortnite-api.com/v2/news/br")
        if req.status_code != 200:
            return
        new = req.json()
    except:
        return
    list = []
    if old != new:
        for i in new:
            if not i in old:
                print("NEW news feed")
                for i in list:
                    if i not in old:
                        MODULES.tweet_image(url=i["image"], message=f"BR News-Feed Update\n{i['title']}\n{i['body']}")
                with open('Cache/news.json', 'w', encoding="utf8") as file:
                    json.dump(list, file)


if __name__ == "__main__":
    print("Twitter Bot Ready")
    while True:
        print("Checking...")
        if SETTINGS.new_cosmetics is True:
            check_leaks()
        if SETTINGS.ingamebugmessage is True:
            other()
        if SETTINGS.shop is True:
            check_shop()
        if SETTINGS.hotfixes is True:
            hotfixes()
        if SETTINGS.staging is True:
            staging()
        if SETTINGS.blogposts is True:
            blogpost()
        if SETTINGS.newsfeed is True:
            news()
        if SETTINGS.intervall < 20:
            time.sleep(20)
        else:
            time.sleep(SETTINGS.intervall)