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
        print("Loaded Chromedriver")
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
        print("Navigated to: 'instagram.com'")
        time.sleep(random.normalvariate(1.1, 0.2))
        username_entry = self.driver.find_element_by_name('username')
        password_entry = self.driver.find_element_by_name('password')
        username_entry.send_keys(self.username)
        password_entry.send_keys(self.password)
        time.sleep(random.normalvariate(1.1, 0.2))
        password_entry.submit()
        print("Logged in succesfully to account: " + self.username)
        #self.driver.find_element_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        
        time.sleep(3)
        login_save_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0]
        login_save_button.click() 
        print("Closed popup 1")
        time.sleep(random.normalvariate(1.5, 0.2))
        #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(By.XPATH("//button[contains(text(), 'Not Now')]")))
        self.make_driver_wait("//button[contains(text(), 'Not Now')]")
        notifications_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0]
        notifications_button.click() 
        print("Closed popup 2")
        time.sleep(random.normalvariate(1.5, 0.2))
        
    

    """
    This group of funcitons are all smaller helper functions that are only called from other larger functions
    Functions in here are clearly named for what they do
    """
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

    def make_driver_wait(self, element_to_locate, by='xpath'):
        wait = WebDriverWait(self.driver, 5)
        if by == 'xpath':
            wait.until(EC.element_to_be_clickable((By.XPATH, element_to_locate)))
        elif by == 'class_name':
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, element_to_locate)))
        elif by == 'tag_name':
            wait.until(EC.element_to_be_clickable((By.TAG_NAME, element_to_locate)))
        else:
            print('choose to search by xpath, class name, or tag name')


    def get_names(self, lc):
        self.make_driver_wait("/html/body/div[4]/div/div/div[2]")
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        names = []
        links = []
        x = 0
        last_ht, ht = 0, 1
        while last_ht <= (lc/12):
            # last_ht = ht
            time.sleep(random.normalvariate(1.4,0.098))
            try:
                ht = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
                time.sleep(2)
            except StaleElementReferenceException:
                continue

            self.make_driver_wait('a', "tag_name")
            links = scroll_box.find_elements_by_tag_name('a')
            names = [name.text for name in links if name.text !='']
            
            x += 1
            print("executed loop scroll: " + str(x) + " times")
            last_ht += 1

        self.make_driver_wait("/html/body/div[4]/div/div/div[1]/div/div[2]/button")
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
            
        return names

    #NEEDS: add option for 'm' million followers
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

        elif followers[-1] == 'm':
            followers_str = (followers[:-1].encode('UTF-8'))
            followers = int(self.extract_numbers(followers_str))
            followers = followers * 1000000

        else:
            followers_str = (followers.encode('UTF-8'))
            followers = int(self.extract_numbers(followers_str))
            
        following = text[2]
        if following[-1] == 'k':
            following_str = (following[:-1].encode('UTF-8'))
            following = int(self.extract_numbers(following_str))
            following = following * 1000

        elif following[-1] == 'm':
            following_str = (following[:-1].encode('UTF-8'))
            following = int(self.extract_numbers(following_str))
            following = following * 1000000

        else:
            following_str = (following.encode('UTF-8'))
            following = int(self.extract_numbers(following_str))

        lst = []
        lst.append(followers)
        lst.append(following)
        
        return lst


    #
    #END HELPER FUNCTIONS
    #


    """
    Task:
        Navigates to a users profile and likes their latest posts as determined by
    Args:
        str user: target user for post liking
        int numposts: number of posts on user page to like
        bool like: True will like all posts, False will unlike them
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
    W.I.P.
    
    Task:
        Designed to go search a tag, skip the first 'top' posts, and then like/follow the new posts
    Args:
        str tag: tag for bot to navigate to
        int numposts: number of posts to like/follow
        bool like: True will like posts, False will unlike
    NEEDS:
        if statement to look if unfollow prompt has appeared and hit cancel if yes
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
    Task:
        Gets list of users the target account follows and outputs to 'following.txt'
        Gets list of users FOLLOWING the target account and outputs to 'followers.txt'
        Cross References the 2 lists and outputs accounts not reciprocating follow to 'notfollowingback.txt'
    Args:
        str user: target user to follow   
    """
    def get_unfollowers(self, user):
        lst = self.follower_amt(user)
        fers = lst[0]
        fing = lst[1]
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        time.sleep(random.normalvariate(3.4, 0.2))
        self.make_driver_wait("//a[contains(@href, '/following')]")
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        print("Navigated to user's following")
        time.sleep(random.normalvariate(3.4, 0.2))
        print("acquiring following accounts...")
        following = self.get_names(fing)
        print("Names retrieved")
        with open('following.txt', 'w') as f:
                for name in following:
                    f.write("%s\n" % name)
        print("Added to text file 'following.txt'")

        time.sleep(random.normalvariate(3.4, 0.2))
        self.make_driver_wait("//a[contains(@href, '/followers')]")
        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
        print("Navigated to user's followers")
        time.sleep(random.normalvariate(3.4, 0.2))
        print("acquiring followers accounts...")
        followers = self.get_names(fers)
        print("Names retrieved")
        with open('followers.txt', 'w') as f:
                for name in followers:
                    f.write("%s\n" % name)
        print("Added to text file 'followers.txt'")

        print("Cross referencing lists...")        
        not_following_back = [user for user in following if user not in followers]
        with open('notfollowingback.txt', 'w') as f:
                for name in not_following_back:
                    f.write("%s\n" % name)
        time.sleep(3)
        print('\n****Unfollowers****')
        prev = " "
        count = 0
        for x in not_following_back:
            if prev != x:
                count += 1
                print(count, x)
                prev = x
        print("Process complete!\n Check file 'notfollowingback.txt'")

       

    """
    Task:
        Reads data from 'notfollowingback.txt' and inserts all accounts into list called profiles
        strips list entries of newline char
        loops through list going to each users account and hitting unfollow while checking if account has been unfollowed
        refreshes page to confirm unfollow, will do this up to 5 times
        plays party horn when complete
    Args: (none)
    Needs:
        Error checking for when instagram stops loading profiles
        Error checking for if line is empty
    """
    def mass_unfollow(self):
        print("Gathering users from 'notfollowingback.txt'...")
        f = open("notfollowingback.txt", 'r+')
        profiles = []
        index = 0
        for line in f:
            #profiles.insert(index, index)
            profiles.append(line.strip())
            index += 1

        #profiles_enum = enumerate(profiles)
        f.close()
        print("Users found")
        count, x, check_runs, limit, refresh_number = 0, 0, 0, 5, 0
        for name in profiles:
            """if ((item[0]+1) % limit == 0):
                profiles[i,en] =(profiles[i,en]) + (limit * check_runs)
                profiles[i,en] = profiles[i,en+1-limit]
                check_runs += 1  #20, 4"""
            time.sleep(random.normalvariate(9.5, 1.125))
            self.nav_user(name)
            time.sleep(random.normalvariate(2.5, 0.025))
            try:
                buttons = self.driver.find_elements_by_xpath("//button[*]")[0].click()
                time.sleep(random.normalvariate(0.8, 0.05))
                self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
                print("Refreshing to confirm unfollow...")
                time.sleep(random.normalvariate(1.2, 0.08))
                self.driver.refresh()
                
                for refresh_number in range (4):
                    try:
                        time.sleep(random.normalvariate(3.2, 0.18))
                        self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
                    except NoSuchElementException:
                        print("Unfollow confirmed")
                        pass
                        break
            
            except NoSuchElementException:
                print("Already unfollowed User")
                pass

            except IndexError:
                print("User no longer exists")
                pass
            
            count +=1
            print(str(count) + ". Unfollowed user: " + profiles[x])
            x += 1            
            #checker +=1
        
        party = AudioSegment.from_mp3('Party_Horn_Sound_Effect.mp3')
        play(party)
        print('Congratulations all users have been unfollowed!')




    """
    WOOOO THIS BITCH WORKS
    Task:
        Navigates to user profile and opens their follower box
        iterates through loops following users and scrolling to repopulate list every 12 accounts using follower amt as loop conditional
    Args:
        str user: target user account with followers that are those who user wants follow backs from
    Needs:
        WebDriverWaits
        Error checking for when Instagram cuts user off from following further (quit upon seeing message)
        Possibly needs more potential xpaths for follow buttons (see button 1 and 2)
    """
    def follow_multiple(self, user):
        #navigate to user profile
        self.nav_user(user)
        print("Navigated to profile: " + user)
        time.sleep(3)
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException)

        #open followers window
        followers_button = self.driver.find_element_by_xpath("//a[contains(@href, '/{}/followers')]".format(user))
        followers_button.click()
        time.sleep(5)
        #WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(By.XPATH("//button[contains(text(), '')]"))
        followers_popup = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        #/html/body/div[7]/div/div/div[2]/ul
        print("Follower box opened")
        #follower_amt = self.follower_amt(user)
        #follower_popup_range = int(follower_amt[0])
        #for i in range(int(follower_popup_range/12)):
        for i in range(1000):
            time.sleep(random.normalvariate(2, 0.3))
            f = 0
            while f<=12:
                f+=1    

                try:
                    #try to click follow button
                    time.sleep(random.normalvariate(9.6, 1.3))   
                    lc = f + (i*12)
                    print('pressing ' + str(lc) + '...')

                    button1 = self.driver.find_elements_by_xpath("/html/body/div[6]/div/div/div[2]/ul/div/li[{}]/div/div[3]/button"\
                        .format(lc))
                    button2 = self.driver.find_elements_by_xpath("/html/body/div[6]/div/div/div[2]/ul/div/li[{}]/div/div[2]/button"\
                        .format(lc))
                    button3 = self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[3]/button"\
                        .format(lc))
                    button4 = self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[2]/button"\
                        .format(lc))
                    button5 = self.driver.find_elements_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[3]/button"\
                            .format(lc))
                    button6 = self.driver.find_elements_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[2]/button"\
                            .format(lc))
                    #for i in range(1,5):/html/body/div[5]/div/div/div[2]/ul/div/li[21]/div/div[2]/button
                    if (len(button1) > 0):
                        button1[0].click()
                        print('button1 ' + str(lc) + ' pressed')
                    elif (len(button2) > 0):
                        button2[0].click()
                        print('button2 ' + str(lc) + ' pressed')
                    elif (len(button3) > 0):
                        button3[0].click()
                        print('button3 ' + str(lc) + ' pressed')
                    elif (len(button4) > 0):
                        button4[0].click()
                        print('button4 ' + str(lc) + ' pressed')
                    elif (len(button5) > 0):
                        button5[0].click()
                        print('button5 ' + str(lc) + ' pressed')
                    elif (len(button6) > 0):
                        button6[0].click()
                        print('button6 ' + str(lc) + ' pressed')

                except ElementClickInterceptedException:
                    #attempt to click cancel on one xpath
                    self.driver.find_element_by_xpath("//button[contains(text(), 'Cancel')]").click()
                    print(str(lc) + ': Already following user')#/html/body/div[6]/div/div/div/div[3]/button[2]
                    f -= 1

                except StaleElementReferenceException:
                    continue

                except ElementClickInterceptedException:
                    input("Potential follow Limit Reached! Try again later :)\nPress any key to exit")
                    self.driver.quit()

                except NoSuchElementException:
                    input("error occured, please see console\nPress any key to exit")
                    self.driver.quit()
                
            #JS to scroll through list
            try:
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_popup)
                print("scrolling...")
                time.sleep(2)
            except StaleElementReferenceException:
                continue

    """
    W.I.P.  
    Task:
        Similar to follow_multiple()
        Navigates to passed in tag and selects a random top post
        opens list of those who liked post
        loops through following each account that liked target tag's post
    Args:
        str tag: target tag to navigate to and follow top liked posts of
    Problems:
        Loops through first 12-17 fine, then follows accounts sporadically in list not linearly
        This is caused by the xpath not being linearly listed as it is in follow_multiple()
    Solutions:
        Populate x amount of users in list and put names into list to be searched and followed with nav_user()
        Populate list and store buttons in array and then loop through and click buttons
    Needs:
        Problems fixed
        Error checking for when Instagram cuts user off from following further (quit upon seeing message)
        Possibly needs more potential xpaths for follow buttons (see button 1 and 2)
    """
    def follow_top_liked(self, tag):
        self.search_tag(tag)
        time.sleep(random.normalvariate(1.5, 0.8))
        top_posts = self.driver.find_elements_by_class_name('_9AhH0')
        top_post = top_posts[random.randint(0,8)]
        top_post.click()
        time.sleep(random.normalvariate(2.5, 0.8))
        
        #click likes
        self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div[2]/button").click()
        #self.driver.find_element_by_xpath("//button[contains(text(), '...')]").click()
        time.sleep(random.normalvariate(2.5, 0.8))
        self.make_driver_wait("/html/body/div[5]/div/div/div[2]")
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        last_ht, ht, olc  = 10, 0, 0
        while last_ht != ht:
            olc += 1
            ht += 1
            i = 0
            time.sleep(random.normalvariate(2.4,0.25))
            #pop_follow_list = self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")
            while (olc <= 12):
                time.sleep(random.normalvariate(2.0, 0.2))
                i += 1
                try:
                    self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div/div/div[{}]/div[3]/button".format(i + ((olc-1)*12))).click()
                    print("Account " + str(i + ((olc-1)*12)) + " Followed")
                except NoSuchElementException:
                    self.driver.find_element_by_xpath("//button[contains(text(), 'Cancel')]").click()
                    i -= 1
                    print("Account " + str(i + ((olc-1)*12)) + " Follow Cancelled")
                except:
                    pass
            try:
                ht = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
                time.sleep(2)
            except StaleElementReferenceException:
                continue
            

            print("executed loop scroll: " + str(olc) + " times")
    


#code under here will execute if the name called is main
if __name__ == '__main__':

    ig_bot = InstagramBot(un, pw)
    
    #ig_bot.like_latest_posts('connorclarkxt', 20, 'like')
    #ig_bot.like_tag_posts('halo4', 12, 'like')
    #print(ig_bot.follower_amt('true_halo_memes'))


    
    #ig_bot.get_unfollowers('brandonator24')
    ig_bot.mass_unfollow()

    #ig_bot.follow_multiple('halo')
    #ig_bot.follow_top_liked('minecraftmemes') 