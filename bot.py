#Libraries

from botImports import *
from topSecretNoNoZone import *


class InstagramBot:

    #create instance of the class
    #Args are the Account username and password
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com'
        self.tag_url = 'explore/tags'
        
        #pass exe to an instance of chrome from selenium's webdriver
        self.driver = webdriver.Chrome()

        self.login()

    """
    Called by creating instance of bot
    -navigate to instagram.com
    -enters login information
    -submits login
    -closes 2 following popup prompts
    """
    def login(self):
        #opens instagram.com then inputs and submits passed in username and password
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(random.normalvariate(1.1, 0.2))
        username_entry = self.driver.find_element_by_name('username')
        password_entry = self.driver.find_element_by_name('password')
        username_entry.send_keys(self.username)
        password_entry.send_keys(self.password)
        time.sleep(random.normalvariate(1.1, 0.2))
        password_entry.submit()
        #self.driver.find_element_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        
        time.sleep(3)
        login_save_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0]
        login_save_button.click() 
        time.sleep(random.normalvariate(1.5, 0.2))
        notifications_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0]
        notifications_button.click() 
        time.sleep(random.normalvariate(1.5, 0.2))
        
    #NEXT SEVERAL FUNCTIONS ARE SHORT HELPER FUNCTIONS TYPICALLY CALLED ELSEWHERE AND ARE SELF-EXPLANAOTRY

    def search_tag(self, tag):
        time.sleep(1)
        self.driver.get('{}/{}/{}/'.format(self.base_url,self.tag_url,tag))
        

    def nav_user(self, user):
        time.sleep(1)
        #string interpolation with 2 vars (pass in vars as strings)
        self.driver.get('{}/{}/'.format(self.base_url,user))

    def follow_user(self, user):
        self.nav_user(user)

        follow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")[0]
        follow_button.click()

    def unfollow_user(self, user):
        self.nav_user(user)

        unfollow_button_list = self.driver.find_elements_by_xpath("//button[contains(text(), 'Following')]")[0]
        unfollow_button = unfollow_button_list[0]

        unfollow_button.click()

    def extract_numbers(self, raw_string):
        return b''.join(re.split(br"[^0-9]*", raw_string))
 

    """
    Navigates to a users profile and likes their latest posts as determined by 'numposts'
    """
    def like_latest_posts(self, user, numposts, like=True):
        action = 'Like' if like else 'Unlike'

        self.nav_user(user)
        time.sleep(random.normalvariate(1.5, 0.8))
        self.driver.find_element_by_class_name('_9AhH0').click()
        time.sleep(random.normalvariate(1.5, 0.8))
       
        self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button").click()
        time.sleep(random.normalvariate(0.7, 0.1))
        self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a").click()

        for img in range(0, numposts-1):
            
            time.sleep(random.normalvariate(2, 1))
            self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button").click()
            time.sleep(random.normalvariate(0.4, 0.2))
            self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]").click()

    """
    WORK IN PROGRES
    Designed to go search a tag, skip the first 'top' posts, and then like/follow the new posts
    NEEDS if statement to look if unfollow prompt has appeared and hit cancel if yes
        check if post already like
    """
    def like_tag_posts(self, tag, numposts, like = True):
        action = 'Like' if like else 'Unlike'

        self.search_tag(tag)
        time.sleep(random.normalvariate(1.5, 0.8))
        self.driver.find_element_by_class_name('_9AhH0').click()
        time.sleep(random.normalvariate(1.5, 0.8))
       
        self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a").click()
        time.sleep(random.normalvariate(0.7, 0.1))

        for img in range(1, 9):
            time.sleep(random.normalvariate(1.4, 0.42))
            self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]").click()

        for img in range(0, numposts):
            
            time.sleep(1.5)
            #if self.driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/svg/path") 

            self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button").click()
            time.sleep(random.normalvariate(2, 1))
            #follow_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]")
            follow_button = self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button")
            follow_button.click()
            time.sleep(random.normalvariate(0.4, 0.2))
            self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]").click()

    """
    NOT ACTIVE
    Loads all media on page
    """
    def infinite_scroll(self):
        """
        Scrolls to the bottom of a users page to load all of their media
        Returns:
         bool: True if the bottom of the page has been reached, else false
        """

        SCROLL_PAUSE_TIME = 1

        self.last_height = self.driver.execute_script("return document.body.scrollHeight")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        self.new_height = self.driver.execute_script("return document.body.scrollHeight")


        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False

    """
    NOT ACTIVE
    Compare list of those i follow and those who do not follow me and unfollow them
    """
    def get_unfollowers(self):
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        time.sleep(3)
        #suggestions = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        #self.driver.execute_script('arguments[0].scrollIntoView()', suggestions)
        time.sleep(1)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
    
        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            time.sleep(1)
            height = self.driver.execute_script("""
                arguements[0].scrollTo(0,arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)

    """
    Navigates to user profile, opens that profile's followers, and scrolls through following their followers
    BUGS doesn't actually fucking follow
    """
    def follow_multiple(self, user):
        #navigate to user profile
        self.nav_user(user)
        time.sleep(3)
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

        #open followers window
        followers_button = self.driver.find_element_by_xpath("//a[contains(@href, '/{}/followers')]".format(user))
        followers_button.click()
        time.sleep(2)
        followers_popup = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        follower_popup_range = int(self.follower_amt(user))
        for i in range(int(follower_popup_range/11)):
            time.sleep(random.normalvariate(2, 0.3))
            f = 1
            while f<=12:
                
                try:
                    #try to click follow button
                    time.sleep(random.normalvariate(1.2, 0.2))   
                    lc = f + (i*11)
                    print('pressing' + str(lc) + '...')
                    self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[3]/button"
                        .format(lc)).click()
                    print('button ' + str(lc) + ' pressed')

                except:
                    print('button ' + str(lc) + 'failed')
                    time.sleep(random.normalvariate(0.2, 0.04))
                    #click cancel

                    try:
                        #attempt to click cancel on one xpath
                        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click()
                        print(str(lc) + ': Already following user')
                        f -= 1

                    except:
                        #other xpath for the same button
                        time.sleep(1)
                        self.driver.find_element_by_xpath("/html/body/div[7]/div/div/div/div[3]/button[2]").click()

                f += 1 
            #JS to scroll through list
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_popup)
            time.sleep(2)

    
    """
    function scrape the amount of followers and following from a passed in user argument
    returns int value rounded down to the nearest thousand
    NEEDS: add option for 'm' million followers
    """
    def follower_amt(self, user):
        time.sleep(2)
        
        html = requests.get('https://www.instagram.com/%s/'%(user))
        soup = BeautifulSoup(html.text, 'lxml')
        data = soup.find_all('meta', attrs={'property':'og:description'})
        text = data[0].get('content').split()
        user = '%s %s %s' % (text[-3], text[-2], text[-1])
        followers = text[0]
        
        #print(followers.encode('UTF-8'))
        if followers[-1] == 'k':
            followers_str = (followers[:-1].encode('UTF-8'))
            followers = int(self.extract_numbers(followers_str))
            followers = followers * 1000
        else:
            followers_str = (followers.encode('UTF-8'))
            followers = int(self.extract_numbers(followers_str))
        
        following = text[2]
        if following[-1] == 'k':
            following_str = (following[:-1].encode('UTF-8'))
            following = int(self.extract_numbers(following_str))
            following = following * 1000
        else:
            following_str = (following.encode('UTF-8'))
            following = int(self.extract_numbers(following_str))

        lst = []
        lst.append(followers)
        lst.append(following)
        
        return int(followers)
        """
        self.driver.get('{}/{}/'.format(self.base_url,user))
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for title in soup.select("._h9luf"):
            posts = title.select("._fd86t")[0].text
            follower = title.select("._fd86t")[1]['title']
            following = title.select("._fd86t")[2].text
            print("Posts: {}\nFollower: {}\nFollowing: {}".format(posts,follower,following))
        """

#code under here will execute if the name called is main
if __name__ == '__main__':

    ig_bot = InstagramBot('brandonator24', pw)
    #ig_bot.nav_user('halo')
    #ig_bot.follow_user('Halo')
    #ig_bot.search_tag('haloreach')
    ig_bot.like_latest_posts('connorclarkxt', 20, 'like')
    #ig_bot.like_tag_posts('halo4', 12, 'like')

    #ig_bot.get_unfollowers()
    #ig_bot.infinite_scroll()

    #print(ig_bot.follower_amt('true_halo_memes'))

    #ig_bot.follow_multiple('halo.reach')
