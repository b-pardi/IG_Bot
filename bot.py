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
        self.scroll_box = "/html/body/div[6]/div/div/div/div[2]"
        self.following_scroll_box = "/html/body/div[6]/div/div/div/div[3]"
        self.like_button = "/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div[2]/div/a/div"
        self.likes_scroll_box = "/html/body/div[7]/div/div/div[2]/div"
        self.top_button_xpath = "/html/body/div[6]/div/div/div[2]/div/div/div[1]/div[3]/button"
        self.next_arrow = "/html/body/div[6]/div[2]/div/div/button"
        
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
        time.sleep(random.normalvariate(5, 0.2))
        username_entry = self.driver.find_element_by_name('username')
        password_entry = self.driver.find_element_by_name('password')
        username_entry.send_keys(self.username)
        password_entry.send_keys(self.password)
        time.sleep(random.normalvariate(1.1, 0.2))
        password_entry.submit()
        print("Logged in succesfully to account: " + self.username)
        
        self.make_driver_wait("//button[contains(text(), 'Not Now')]")
        login_save_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0]
        login_save_button.click() 
        print("Closed popup 1")
        time.sleep(random.normalvariate(4.5, 0.2))
        
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
        wait = WebDriverWait(self.driver, 15)
        if by == 'xpath':
            wait.until(EC.element_to_be_clickable((By.XPATH, element_to_locate)))
        elif by == 'class_name':
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, element_to_locate)))
        elif by == 'tag_name':
            wait.until(EC.element_to_be_clickable((By.TAG_NAME, element_to_locate)))
        else:
            print('choose to search by xpath, class name, or tag name')


    def get_names(self, lc):
        self.make_driver_wait(self.scroll_box)
        scroll_box = self.driver.find_element_by_xpath(self.scroll_box)
        names = []
        links = []
        iteration = []
        time_taken = []
        x = 0
        last_ht, ht = 0, 1
        while last_ht <= (lc/12):
            # last_ht = ht
            start_time = time.time()
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
            end_time = time.time()
            iteration.append(x)
            time_taken.append(end_time - start_time)

            last_ht += 1

        self.make_driver_wait("/html/body/div[5]/div/div/div[1]/div/div[2]/button")
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
        return names, iteration, time_taken

    def follower_amt(self, user):
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
        try:
            req = requests.get(f'https://www.instagram.com/{user}/')
        except HTTPError as httperr:
            print(f"HTTP Error occurred as {httperr}")
        except (Exception) as err:
            print(f"Other error occurred as {err}")

        soup = BeautifulSoup(req.content, 'html.parser')
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
    """
        lst = []
        lst.append(wers)
        lst.append(wing)
        
        return lst
    

    def auto_scroll(self, num_users):
        scrolls = int(num_users) / 12
        num_scrolls = int(scrolls)
        scroll_box = self.driver.find_element_by_xpath(self.scroll_box)
        for i in range(num_scrolls):
            time.sleep(2.5)
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_box)

        print(f"Scrolled {scrolls} times past {num_users}.\nAll caught up!")


    def remove_duplicates(self, file_name):
        name_list = []
        special_names_list = []
        names_dict = {}
        file_name = "whitelist.txt"
        excl_file_name = "permawhitelist.txt"
        with open(file_name, 'r') as names:
            for line in names:
                if (line in names_dict):
                    names_dict[line] = names_dict[line] + 1
                else:
                    names_dict[line] = 1

                if (line not in name_list):
                    name_list.append(line)
                    
        with open(excl_file_name, 'a+') as special_names:
            special_names.seek(0)
            for line in special_names:
                special_names_list.append(line)
            for item in list(names_dict.keys()):
                if ((names_dict[item] > 0) and (item not in special_names_list)):
                    name_list.append(item)

        with open (file_name, 'w') as new_names:
            for item in name_list:
                new_names.write(item)
            for special_item in special_names_list:
                new_names.write(special_item)


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
        Likes posts from user's feed
    Args:
        int numposts: number of posts to like
    Needs:
        do not click like if button already liked,
        do not like ads
    """
    def like_home_feed(self, numposts):
        time.sleep(3)
        pic_posts = []
        vid_posts = []
        posts = []
        for i in range(0, 4):
            print("Scrolling...")
            self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(random.normalvariate(2,0.4))

            print("Gathering posts...")
            pic_posts += self.driver.find_elements_by_class_name("_9AhH0")
            vid_posts += self.driver.find_elements_by_class_name("fXIG0")
            print("Gathered " + str(len(pic_posts)) + " picture posts")
            print("Gathered " + str(len(vid_posts)) + " picture posts")
            time.sleep(random.normalvariate(2,0.4))

        actionChains = ActionChains(self.driver)
        posts = pic_posts + vid_posts
        print("\n"+str(len(posts))+"\n\n")
        for post in posts:
            print(str(posts.index(post)+1) + str(post))

        for index, post in enumerate(pic_posts):
            if post in pic_posts:
                try:
                    print("Liking image post " + str(index) + " ...")
                    #actionChains.move_to_element(post).perform()
                    self.driver.execute_script("arguments[0].scrollIntoView();", post)
                    time.sleep(1)
                    actionChains.double_click(on_element=post).perform()
                    print("Image post liked")

                except StaleElementReferenceException:
                    print("scrolling to top...")
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                    if index > 0:
                        post = pic_posts[index - 1]
                        print(str(post))

                time.sleep(random.normalvariate(6,0.5))

            elif post in vid_posts:
                print("vid post\nskipping for now...")
                pass
        """
            try:
                like_count = 0 + lc_start
            except UnboundLocalError:
                like_count = 0
                pass

            for like_num in range(like_count, (len(pic_posts1) + len(vid_posts1))):
                try:
                    actionChains = ActionChains(self.driver)
                    if(len(pic_posts1) > like_num):
                        print("Liking image post " + like_num + " ...")
                        actionChains.double_click(pic_posts1[like_num]).perform()
                        print("Image post liked")
                        time.sleep(random.normalvariate(6,0.5))
                    
                    if(len(vid_posts1) > like_num):
                        print("Liking video post " + like_num + " ...")
                        actionChains.double_click(vid_posts1[like_num]).perform()
                        print("Video post liked")
                        time.sleep(random.normalvariate(6,0.5))
                
                except:
                    print("error")
                
                lc_start = (len(pic_posts1) + len(vid_posts1))
        """


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
        self.nav_user(user)
        lst = self.follower_amt(user)
        fers = lst[0]
        fing = lst[1]
        ### comment out from here to next '###' to reprocess list cross referencing
        
        time.sleep(random.normalvariate(3.4, 0.2))
        self.make_driver_wait("//a[contains(@href, '/following')]")
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        print("Navigated to user's following")
        time.sleep(random.normalvariate(3.4, 0.2))
        print("acquiring following accounts...")
        following_data = self.get_names(fing)
        following = following_data[0]
        print("Names retrieved")
        with open('following.txt', 'w') as f:
                for name in following:
                    f.write("%s\n" % name)
        print("Added to text file 'following.txt'")
        iteration = following_data[1]
        time_taken = following_data[2]
        with open ("time_data.txt", "w") as time_data:
            time_data.write("***FOLLOWING DATA***\n")
            for point in iteration:
                time_data.write(f"{iteration[point-1]}, {time_taken[point-1]}\n")
            time_data.write("------\n")
            for point in iteration:
                time_data.write(f"{iteration[point-1]}\n")
            time_data.write("------\n")
            for point in iteration:
                time_data.write(f"{time_taken[point-1]}\n")
        print("Added data to 'time_data.txt'")
        
        time.sleep(random.normalvariate(3.4, 0.2))
        self.make_driver_wait("//a[contains(@href, '/followers')]")
        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
        print("Navigated to user's followers")
        time.sleep(random.normalvariate(3.4, 0.2))
        print("acquiring followers accounts...")
        followers_data = self.get_names(fers)
        followers = followers_data[0]
        print("Names retrieved")
        with open('followers.txt', 'w') as f:
                for name in followers:
                    f.write("%s\n" % name)
        print("Added to text file 'followers.txt'")
        iteration = followers_data[1]
        time_taken = followers_data[2]
        with open ("time_data.txt", "a") as time_data:
            time_data.write("***FOLLOWERS DATA***\n")
            for point in iteration:
                time_data.write(f"{iteration[point-1]}, {time_taken[point-1]}\n")
            time_data.write("------\n")
            for point in iteration:
                time_data.write(f"{iteration[point-1]}\n")
            time_data.write("------\n")
            for point in iteration:
                time_data.write(f"{time_taken[point-1]}\n")
        print("Appended data to 'time_data.txt'")
        
        """
        following = []
        followers = []
        with open('following.txt', 'r') as fing:
            for name in fing:
                following.append(name.strip())    
        
        with open('followers.txt', 'r') as fers:
            for name in fers:
                followers.append(name.strip())
        """###
        print("Cross referencing lists...")        
        #not_following_back = [user for user in following if not in followers]
        not_following_back = []
        for user in following:
            if user not in followers:
                not_following_back.append(user)
            else:
                pass
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
    Args:
        self
    Needs:
        Error checking for when instagram stops loading profiles
        Error checking for if line is empty
    """
    def mass_unfollow(self):
        print("Gathering users from 'notfollowingback.txt'...")
        nfb = open("notfollowingback.txt", 'r+')
        profiles = []
        index = 0
        for line in nfb:
            profiles.append(line.strip())
            index += 1

        nfb.close()
        print("Users found")
        count, x, refresh_number = 0, 0, 0
        for name in profiles:
            time.sleep(random.normalvariate(5.5, 0.425))
            self.nav_user(name)
            time.sleep(random.normalvariate(22, 8.6))
            
            try:
                buttons = self.driver.find_elements_by_xpath("//button[*]")[0].click()
                time.sleep(random.normalvariate(0.8, 0.05))
                self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()

                for refresh_number in range (6):
                    try:
                        print("Refreshing to confirm unfollow...")
                        time.sleep(random.normalvariate(1.2, 0.08))
                        self.driver.refresh()
                        wait_time = 5 + refresh_number**2
                        time.sleep(random.normalvariate(wait_time, 0.18))
                        buttons = self.driver.find_elements_by_xpath("//button[*]")
                        check_buttons = self.driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/div/div/div[1]/div/button")
                        if(len(check_buttons) > 0):                         
                            print("repeating unfollow...")
                            time.sleep(random.normalvariate(1, 0.054))
                            check_buttons[0].click()
                        if(len(buttons) > 0):
                            print("repeating unfollow")
                            buttons[0].click()
                        time.sleep(random.normalvariate(1.8, 0.05))
                        self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
                    except NoSuchElementException:
                        print("Unfollow confirmed")
                        pass
                        break
            
            except NoSuchElementException:
                print("Already unfollowed User")
                pass

            except IndexError:
                error_header = self.driver.find_elements_by_class_name("error-container -cx-PRIVATE-ErrorPage__errorContainer -cx-PRIVATE-ErrorPage__errorContainer__")
                error_header_v2 = self.driver.find_elements_by_xpath("//h2[contains(text(), 'Error')]")
                if(len(error_header) > 0 or len(error_header_v2) > 0):
                    print("Unfollow Limit Reached, try again later\n\nclosing in 5 seconds...")
                    time.sleep(5)
                    self.driver.save_screenshot("unfollowlimit.png")
                    self.driver.quit()
                    quit()
                else:
                    print("User no longer exists")
                    pass
            
            count +=1
            print(str(count) + ". Unfollowed user: " + profiles[x])
            
            with open("notfollowingback.txt", "r") as nfbr:
                profiles_new = nfbr.readlines()
            with open("notfollowingback.txt", "w") as nfbr:
                for line in profiles_new:
                    if (line.strip("\n") != profiles[x]):
                        nfbr.write(line)
            print("User " + profiles[x] + " removed from list")

            x += 1
        
        party = AudioSegment.from_mp3('Party_Horn_Sound_Effect.mp3')
        play(party)
        print('Congratulations all users have been unfollowed!')




    """
    WOOOO THIS BITCH WORKS
    Task:
        Navigates to user profile and opens their follower box
        iterates through loops following users and scrolling to repopulate list every 12 accounts using follower amt as loop conditional
    Args:
        self
        str user: target user account with followers that are those who user wants follow backs from
        int wait_time: time to wait between each follow button
        bool recent_follow: true if user has followed the target account recently
        int num_users: number of users to scroll past if previous arg is true
    Needs:
        LIKE POSTS OF USERS AFTER FOLLOWING
        put in num followers of target account into for loop
        WebDriverWaits
        Error checking for when Instagram cuts user off from following further (quit upon seeing message)
        Possibly needs more potential xpaths for follow buttons (see button 1 and 2)
    """
    def follow_multiple(self, user, wait_time, num_users, recent_follow):
        #navigate to user profile
        self.nav_user(user)
        print("Navigated to profile: " + user)
        time.sleep(3)
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException)

        #open followers window
        followers_button = self.driver.find_element_by_xpath("//a[contains(@href, '/{}/followers')]".format(user))
        followers_button.click()
        time.sleep(5)
        followers_popup = self.driver.find_element_by_xpath(self.scroll_box)
        print("Follower box opened")
        if (recent_follow == 'y' or 'Y'):
            self.auto_scroll(num_users)
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
                    time.sleep(random.normalvariate(int(wait_time), 1.5))   
                    lc = num_users + f + (i*12)
                    print('pressing ' + str(lc) + '...')

                    button1 = self.driver.find_elements_by_xpath("/html/body/div[6]/div/div/div/div[2]/ul/div/li[{}]/div/div[3]/button"\
                        .format(lc))                            #/html/body/div[6]/div/div/div/div[2]/ul/div/li[70]/div/div[2]/button
                    button2 = self.driver.find_elements_by_xpath("/html/body/div[6]/div/div/div/div[2]/ul/div/li[{}]/div/div[2]/button"\
                        .format(lc))
                    button3 = self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[3]/button"\
                        .format(lc))
                    button4 = self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[2]/button"\
                        .format(lc))
                    button5 = self.driver.find_elements_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[3]/button"\
                        .format(lc))
                    button6 = self.driver.find_elements_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[2]/button"\
                        .format(lc))
                    cancel_unfollow_button2 = self.driver.find_elements_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]")

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
                    cancel_unfollow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Cancel')]")
                    cancel_unfollow_button2 = self.driver.find_elements_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]")
                    follow_limit_buttons = self.driver.find_elements_by_xpath("//button[contains(text(), 'OK')]")
                    if (len(cancel_unfollow_button) > 0):
                        cancel_unfollow_button[0].click()
                        print(str(lc) + ': Already following user')
                        f -= 1
                    elif (len(cancel_unfollow_button2) > 0):
                        cancel_unfollow_button2[0].click()
                        print(str(lc) + ': Already following user')
                        f -= 1
                    elif (len(follow_limit_buttons) > 0):
                        input("Potential follow Limit Reached! Try again later :)\n\nPress any key to exit")
                        self.driver.save_screenshot("followlimit.png")
                        time.sleep(5)
                        self.driver.quit()
                        quit()

                except StaleElementReferenceException:
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_popup)
                    continue

                except IndexError:
                    error_header = self.driver.find_elements_by_class_name("error-container -cx-PRIVATE-ErrorPage__errorContainer -cx-PRIVATE-ErrorPage__errorContainer__")
                    error_header_v2 = self.driver.find_elements_by_xpath("//h2[contains(text(), 'Error')]")
                    if(len(error_header) > 0 or len(error_header_v2) > 0):
                        print("Follow Limit Reached, try again later\n\nclosing in 5 seconds...")
                        self.driver.save_screenshot("follow_multiple()_Indexerror.png")
                        time.sleep(5)
                        self.driver.quit()
                        quit()

                except NoSuchElementException:
                    input("error occured, please see console\nPress any key to exit")
                    self.driver.save_screenshot("follow_multiple()_NSEEerror.png")
                    time.sleep(2)
                    self.driver.quit()
                    quit()
                
            #JS to scroll through list
            try:
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_popup)
                print("scrolling...")
                time.sleep(2)
            except StaleElementReferenceException:
                continue

        
        print("Safe limit of 330 people followed\nclosing program...")
        self.driver.save_screenshot("follow_multiple()_330limit.png")
        time.sleep(2)
        self.driver.quit()
        quit()

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
    
    
    """
    W.I.P.  
    Task:
        Navigates to user recent posts
        opens list of those who liked post
        loops through adding each name to 'whitelist.txt'
    Args:
        self
    Problems:
        duplicate names, and duplicate removal fails
    Solutions:
        reevaluate life choices
    Needs:
        Problems fixed
        find users who viewed recent story
    """
    def find_active_users(self):
        self.nav_user(un)
        
        for i in range(1,10):
            time.sleep(random.normalvariate(8,0.5))
            #xpath for a post in the profile
            posts = self.driver.find_elements_by_class_name("_9AhH0")
            try:
                posts[i-1].click()
            except ElementClickInterceptedException:
                print("Could not open post\npossible video feed post")
                pass
            time.sleep(3)

            try:
                self.make_driver_wait(self.like_button)
            except:
                next_arrow_button = self.driver.find_element_by_xpath(self.next_arrow)
                next_arrow_button.click()
                self.make_driver_wait(self.like_button)

            liked = self.driver.find_element_by_xpath(self.like_button)
            liked.click()
            self.make_driver_wait(self.likes_scroll_box)
            scroll_box = self.driver.find_element_by_xpath(self.likes_scroll_box)
            
            names = []
            links = []

            links = scroll_box.find_elements_by_tag_name('a')
            print(f"Gathered top of list {len(links)} links, and they are {links}")
            for name in links:
                if (name.text != '') and (name.text not in links):
                    names.append(name.text)
                    print("Appended first iteration links")

            box_len = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
            print("Scrolled first")
            end = False
            while (end == False):
                page_ht = box_len
                time.sleep(2)

                links = scroll_box.find_elements_by_tag_name('a')
                print(f"Gathered {len(links)} and they are {links}")
                for name in links:
                    if (name.text != '') and (name.text not in links):
                        names.append(name.text)
                        print("Appended those links")

                box_len = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
                print("loop scroll")
                if (page_ht == box_len):
                    end = True

            print(len(links))
            

            with open("whitelist.txt", "a") as wl:
                for name in names:
                    wl.write(f"{name}\n")

            print(f"Links gathered from from {i} recent post")
            self.nav_user(un)

        self.remove_duplicates("whitelist.txt")
        print("Active users found and added to whitelist.txt")

    """
    W.I.P.  
    Task:
        gathers small group of users from following
    Args:
        self
    Problems:
        not tested
    Solutions:
        test it maybe
    Needs:

        testing
    """
    def gather_unfollow_names(self):
        first_user_links = scroll_box.find_elements_by_tag_name('a')
        print(f"{len(first_user_links)} links grabbed")
        time.sleep(1)

        unf_targets = []
        for name in first_user_links:
            if(name.text != '') and (name.text not in wl_names):
                unf_targets.append(name.text)
                print(f"Appended {name.text}")
        
        print("User list created")
        time.sleep(1)

        return unf_targets
    """        
    W.I.P.  
    Task:
        Unfollows users not in whitelist.txt or permawhitelist.txt
        navs to user's following and gets small group of names at a time
    Args:
        self
    Problems:
        goes to same profiles repeatedly
    Solutions:
        use the refresh check method from mass_unfollow()
    Needs:
        expand the group of names for when users in whitelist crowd the top
    """
    def ultra_mass_unfollow(self, unf_num):
        log = open("unfollow_log.txt", "w")
        wl_names = []
        with open("permawhitelist.txt", "r") as pwl:
            for name in pwl:
                wl_names.append(name.strip('\n'))
        with open("whitelist.txt", "r") as wl:
            for name in wl:
                wl_names.append(name.strip('\n'))
        print("Files opened")

        scroll_num = int(unf_num/12)
        j = 0
        while j <= unf_num:
            self.nav_user(un)
            print("profile navigated to")
            self.make_driver_wait(f"//a[contains(@href, '/{un}/following')]")
            self.driver.find_element_by_xpath(f"//a[contains(@href, '/{un}/following')]").click()
            print("following button clicked")
            self.make_driver_wait(self.following_scroll_box)
            scroll_box = self.driver.find_element_by_xpath(self.following_scroll_box)
            scroll_box.click()
            time.sleep(2)

            first_user_links = scroll_box.find_elements_by_tag_name('a')
            print(f"{len(first_user_links)} links grabbed")
            time.sleep(1)

            unf_targets = []
            for name in first_user_links:
                print(name)
                print(name.text)
                if(name.text != '') and (name.text not in wl_names):
                    unf_targets.append(name.text)
                    print(f"Appended {name.text}")
            
            print("User list created")
            time.sleep(5)

            while(len(unf_targets) <= 8):
                print("list is too short, scrolling")
                box_len = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
                time.sleep(5)
                first_user_links = scroll_box.find_elements_by_tag_name('a')
                print(f"{len(first_user_links)} links grabbed again")
                time.sleep(5)
                for name in first_user_links:
                    if(name.text != '') and (name.text not in wl_names):
                        unf_targets.append(name.text)
                        print(f"Appended {name.text}")

            refresh_num = 0
            for i in range(0, len(unf_targets)):
                print(f"navigating to user {j}.{i+1}: {unf_targets[i]}")
                self.nav_user(unf_targets[i])
                time.sleep(random.normalvariate(6,0.2))
                try:
                    buttons = self.driver.find_elements_by_xpath("//button[*]")[1].click()
                except Exception as e:
                    print(e)
                    pass
                time.sleep(random.normalvariate(1.8, 0.05))
                try:
                    self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
                except NoSuchElementException as nse:
                    print(f"User already unfollowed\nHere's the error just in case: {nse}")
                    pass
                
                time.sleep(random.normalvariate(20, 2.2))
                for refresh_num in range (6):
                    try:
                        print("Refreshing to confirm unfollow...")
                        time.sleep(random.normalvariate(1.2, 0.08))
                        self.driver.refresh()
                        wait_time = 5 + refresh_num**2
                        time.sleep(random.normalvariate(wait_time, 0.18))
                        buttons = self.driver.find_elements_by_xpath("//button[*]")
                        if(len(buttons) > 0):
                            print("repeating unfollow")
                            print(buttons)
                            buttons[2].click()
                        time.sleep(random.normalvariate(2, 0.08))
                        self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
                    except NoSuchElementException:
                        print(f"unfollow {j} confirmed")
                        j += 1
                        break
                    except ElementClickInterceptedException as exc:
                        print(exc)
                        self.driver.refresh()
                        j -= 1

        log.close()



    """
    Task:
        Similar to mass_unfollow()
        Navigates to user's profile, and then their following list
        Unfollows every user in list that is NOT in 'whitelist.txt' upto limit specified
        Each user unfollowed written to "unfollow.txt"
    Args:
        int num: number of users to unfollow
    Needs:
        write names of unfollowed to list
        Error checking for when Instagram cuts user off from unfollowing further (quit upon seeing message)
        actually implement whitelist
    """  
    def purge_following(self, num):
        self.nav_user(un)
        self.make_driver_wait("//a[contains(@href, '/following')]")
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        self.make_driver_wait(self.scroll_box)
        scroll_box = self.driver.find_element_by_xpath(self.scroll_box)
        i = 1
        wl_names = []

        log = open("unfollow_log.txt", "w")

        while (i <= num):
            time.sleep(10)
            try:
                self.make_driver_wait(f"//button[contains(text(), 'Following')]")  
                unfollow_button = self.driver.find_element_by_xpath(f"//button[contains(text(), 'Following')]")
                unfollow_button.click()                             #/html/body/div[5]/div/div/div[2]/ul/div/li[1]/div/div[3]/button
                print("Unfollow Clicked")
                time.sleep(1)
                confirm_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")
                confirm_button.click()
                print(f"Confirmed\n\t{i} users unfollowed")
                self.make_driver_wait('a', "tag_name")
                i +=1
                time.sleep(1)
            except NoSuchElementException as confexc:
                print(confexc)
                time.sleep(3)
                unfollow_button = self.driver.find_element_by_xpath(f"//button[contains(text(), 'Following')]")
                unfollow_button.click()
                print("Unfollow RE-clicked")
                time.sleep(1)
                confirm_button2 = self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")
                confirm_button2.click()
                print(f"2nd attempt Confirmed\n\t{i} users unfollowed")
            except TimeoutException as timexc:
                print(timexc)
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_box)


        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text !='']
        for user in names:
            log.write(user)
        log.write(f"Unfollowed {num} users")
        log.close()
        print(f"Successfully unfollowed {num} users!")
                


if __name__ == '__main__':

    print("***Menu***")

    choice = input("""
1: Follow users from profile
2: Follow users from tag [WIP]
3: Find Unfollowers
4: Unfollow users
5: Like home page posts [WIP]
6: Purge Following
7: Create whitelist
8: Unfollow using whitelist

test: TESTS
h: Help
q: Quit    
______________________________

""")

    if (choice == "1"):
        user = input('Enter user to follow followers of: ')
        wait_time = input('Enter wait time between follows: ')
        recent_follow = input('Have you followed this account recently?\n (enter y or n):  ')
        if (recent_follow == ('y' or 'Y')):
            snum_users = input("how many users to scroll past?\n(About how many users were followed recently?):  ")
            num_users = int(snum_users)
            print(f"Awesome! skipping {num_users} users and following from {user}")
            ig_bot = InstagramBot(un, pw)
            ig_bot.follow_multiple(user, wait_time, num_users, recent_follow)
        else:
            num_users = 0
            recent_follow = 'n'
            ig_bot = InstagramBot(un, pw)
            ig_bot.follow_multiple(user, wait_time, num_users, recent_follow)

    elif (choice == "2"):
        tag = input('Enter tag to follow profiles from: ')
        ig_bot = InstagramBot(un, pw)
        ig_bot.follow_top_liked(tag)

    elif (choice == "3"):
        print("Navigating to '" + un + "' to acquire users\nPlease do not interrupt process!\n\
        The time it takes increases exponentially with the more followers/following you have")
        ig_bot = InstagramBot(un, pw)
        ig_bot.get_unfollowers(un)

    elif (choice == "4"):
        print("Unfollowing users from 'notfollowingback.txt'")
        ig_bot = InstagramBot(un, pw)
        ig_bot.mass_unfollow()

    elif(choice == "5"):
        numposts = int(input("How many posts do you want to like? "))
        print("Will do!\nnavigating to home page to like posts...")
        ig_bot = InstagramBot(un, pw)
        ig_bot.like_home_feed(numposts)

    elif(choice == "6"):
        num = int(input("How many users to unfollow? "))
        print("Unfollowing users...")
        ig_bot = InstagramBot(un, pw)
        ig_bot.purge_following(num)

    elif(choice == "7"):
        print("Navigating to profile to find active users...")
        ig_bot = InstagramBot(un, pw)
        ig_bot.find_active_users()

    elif(choice == "8"):
        num = int(input("How many users to unfollow? "))
        print("Unfollowing users with exception of those in 'whitelist.txt'")
        ig_bot = InstagramBot(un, pw)
        ig_bot.ultra_mass_unfollow(num)

    elif(choice == "test"):
        print("executing current test function")
        time.sleep(0.5)
        ig_bot = InstagramBot("brandonator24", pw)
        ig_bot.remove_duplicates("whitelist.txt")
        
    elif (choice == "h" or choice == "H"):
        print("Help will be implemented in the future")
        time.sleep(1)
        sys.exit()

    elif (choice == "q" or choice == "Q"):
        print("Closing...")
        time.sleep(1)
        sys.exit()

    else:
        print("Please select valid option")

    #ig_bot.like_home_feed('3')

    #ig_bot.get_unfollowers('brandonator24')
    #ig_bot.mass_unfollow()

    #ig_bot.follow_multiple('halo')
    #ig_bot.follow_top_liked('minecraftmemes') 