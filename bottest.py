from botImports import *
from topSecretNoNoZone import *
from bot import *

"""
Small tests for various parts of the bot
NOT NEEDED FOR OPERATION
"""

if __name__ == '__main__':

#<meta property="og:description" content="1,641 Followers, 2,499 Following, 57 Posts - See Instagram photos and videos from Brandon Pardi (@brandonator24)" />
    ig_bot = InstagramBot(un, pw)
    ig_bot.nav_user('brandonator24')
    time.sleep(6)
    tags = ig_bot.driver.find_element_by_xpath('//meta[@property="og:description"]')
    print(tags.get_attribute("content"))
    meta_tag = tags.get_attribute("content")
    #meta_tag = ("1,644 Followers, 2,500 Following, 57 Posts - See Instagram photos and videos from Brandon Pardi (@brandonator24)")
    reg_num = re.findall(r'\d+\,?\.?\d+k?m?', str(meta_tag))
    wers_str = reg_num[0]
    wing_str = reg_num[1]
    posts_str = reg_num[2]
    if(re.findall(r'k', str(wers_str))):
        print("found k")
        wers = 100*int(wers_str.replace('.', '').strip('k'))
    elif(re.findall(r'm', str(wers_str))):
        print("found m")
        wers = 100000*int(wers_str.replace('.', '').strip('k'))
    else:
        wers = int(wers_str.replace(',', ''))

    if(re.findall(r'k', str(wing_str))):
        print("found k")
        wing = 100*int(wing_str.replace('.', '').strip('k'))
    elif(re.findall(r'm', str(wing_str))):
        print("found m")
        wing = 100000*int(wing_str.replace('.', '').strip('k'))
    else:
        wing = int(wing_str.replace(',', ''))

    print(f"followers: {wers}, following: {wing}, posts: {reg_num[2]}")

    """
    url = "https://www.instagram.com/brandonator24/"
    #headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    headers = {'User-Agent':'Mozilla/5.0'}
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    stuff = soup.find('meta', property="og:description")
    #thing = stuff['content'].split()
    print(stuff)
    reg_num = re.findall(r'\d+\,?\.?\d+k?m?', str(stuff))
    wers_str = reg_num[0]
    wing_str = reg_num[1]
    posts_str = reg_num[2]
    if(re.findall(r'k', str(wers_str))):
        print("found k")
        wers = 100*int(wers_str.replace('.', '').strip('k'))
    if(re.findall(r'k', str(wing_str))):
        print("found k")
        wing = 100*int(wing_str.replace('.', '').strip('k'))
    if(re.findall(r'm', str(wers_str))):
        print("found m")
        wers = 100000*int(wers_str.replace('.', '').strip('k'))
    if(re.findall(r'm', str(wing_str))):
        print("found m")
        wing = 100000*int(wing_str.replace('.', '').strip('k'))

    print(f"followers: {wers}, following:{wing}, posts: {reg_num[2]}")
    """
    """
    r = requests.get("https://ca.iherb.com/pr/Life-Extension-BioActive-Complete-B-Complex-60-Vegetarian-Capsules/67051")
    soup = BeautifulSoup(r.content, 'html.parser')
    list_items = soup.find('div', itemprop="description")
    found = str(re.findall(r'itemprop="description"><ul><li>(\D+)', str(list_items)))

    newfound = re.sub(r"</li>|[\[']", '', found)
    newfound2 = re.sub(r"<li>", ', ', newfound)
    stripped = newfound2.split('\\xa0', 1)[0]

    print(stripped)
    """
    """
    url = "https://www.instagram.com/brandonator24/?__a=1"
    r = requests.get(url).text
    print(int(re.search('"edge_follow":{"count":(\d+)}', r).groups(0)[0]))
    """
    
    """
    user = "brandonator24"
    headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    res = requests.get(f'https://www.instagram.com/{user}/?__a=1', headers=headers)

    print(res.json()['graphql']['user']['username'])
    print(res.json()['graphql']['user']['edge_followed_by']['count'])
    """
    """ THIS WORKS-
    r = requests.get('https://www.instagram.com/brandonator24/', headers = {'User-Agent':'Mozilla/5.0'}).text

    print(int(re.search('"edge_follow":{"count":(\d+)}', r).groups(0)[0]))
    """

    input("\n\npress enter to exit")
    quit()