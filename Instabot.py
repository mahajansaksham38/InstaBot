#IMPORT REQUIRED LIBRARIES
import requests,urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from termcolor import colored

# __________________________________________________________________________________________________________________________________________________

#STRORING ACCESS _TOKEN AND BASE_URL IN GLOBAL VARIABLE
APP_ACCESS_TOKEN='1415747117.b9cb54b.3d49d10dcde5416cbc03113f3ffd6ad7'
BASE_URL = 'https://api.instagram.com/v1/'

# __________________________________________________________________________________________________________________________________________________

#METHOD TO PRINT OWN INFO
def self_info():
    try:
        request_url=BASE_URL+'users/self/?access_token='+APP_ACCESS_TOKEN               #GET REQUEST URL
        print "GET request url: %s" %(request_url)                                      #PRINTS GET REQUEST URL
        user_info=requests.get(request_url).json()                                      #STORES JSON OBJECT RESPONSE IN A VARIABLE
    except:
        print colored("Request url is not working proper. Please Try again.",'red')
    if user_info['meta']['code'] == 200:                                            #CHECKS IF RECIEVED META CODE IS 200
        if len(user_info['data']):                                                  #IF DATA IN USER INFO IS NOT EMPTY THEN PRINTS DATA
                    print colored('Username: %s','green') % (user_info['data']['username'])
                    print colored('No. of followers: %s','green') % (user_info['data']['counts']['followed_by'])
                    print colored('No. of people you are following: %s','green') % (user_info['data']['counts']['follows'])
                    print colored('No. of posts: %s','green' )% (user_info['data']['counts']['media'])
                    print colored('Short Bio: %s','green') %(user_info['data']['bio'])
        else:
                    print colored('User does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')


#__________________________________________________________________________________________________________________________________________________

#Function declaration to get the ID of a user by username
def get_user_id(insta_username):
    try:
        request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_info = requests.get(request_url).json()        #STORES JSON OBJECT RESPONSE IN A VARIABLE
    except:
        print colored("Request url is not working proper.", 'red')
    try:
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                return user_info['data'][0]['id']   #RETURNS ID OF THE USER
            else:
                return None                         #RETRUNS NONE IF USERNAME IS NOT PRESENT
        else:
            print colored('Status code other than 200 received!','red')

    except:
        print colored("Unable to process your request. Please try again!!", 'red')

# __________________________________________________________________________________________________________________________________________________


#FUNCTION TO GET USER INFO BY USERNAME WHICH ACCEPTS USERNAME AS ARGUEMENT
def get_user_info(insta_username):
        user_id = get_user_id(insta_username)
        if user_id == None:                                 #CHECKS  IF USERNAME IS VALID OR NOT
            print colored('User does not exist!','red')
        else:
            request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
            print 'GET request url : %s' % (request_url)            #PRINTS GET REQUEST URL
            user_info = requests.get(request_url).json()            #STORES JSON OBJECT RESPONSE IN A VARIABLE

            if user_info['meta']['code'] == 200:                    #CHECKS IF RECIEVED META CODE IS 200
                try:
                    if len(user_info['data']):
                        print colored('Username: %s','green') % (user_info['data']['username'])
                        print colored('No. of followers: %s','green') % (user_info['data']['counts']['followed_by'])
                        print colored('No. of people %s are following: %s','green') % (user_info['data']['username'],user_info['data']['counts']['follows'])
                        print colored('No. of posts: %s','green') % (user_info['data']['counts']['media'])
                    else:
                        print colored('There is no data for this user!','red')
                except KeyError:
                    print colored("Unable to process your request. Please try again!!", 'red')
            else:
                print colored('Status code other than 200 received!','red')

# __________________________________________________________________________________________________________________________________________________


#FUNTION TO GET OWN RECENT POST AND DOWNLOAD IT
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)      #GET REQUEST URL
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()                                                    #STORES JSON OBJECT RESPONSE IN A VARIABLE

    if own_media['meta']['code'] == 200:                                                    #CHECKS IF RECIEVED META CODE IS 200
        try:
            if len(own_media['data']):
                image_name = own_media['data'][0]['id'] + '.jpeg'                               #SETS IMAGE NAME AFTER DOWNLOADING
                image_url = own_media['data'][0]['images']['standard_resolution']['url']        #STORING IMAGE URL IN VARIABLE
                urllib.urlretrieve(image_url, image_name)                                       #urlretrieve takes two arguements one is image url other is name and downloads image
                print colored('Your image has been downloaded!','blue')
            else:
                print colored('Post does not exist!','red')
        except KeyError:
            print colored("Unable to process your request. Please try again!!",'red')
    else:
        print colored('Status code other than 200 received!','red')

# __________________________________________________________________________________________________________________________________________________


#FUNCTION TO GET USER POST WHICH ACCEPTS USERNAME AS ARGUEMENT
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!','red')
    else:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_media = requests.get(request_url).json()                                           #STORES JSON OBJECT RESPONSE IN A VARIABLE

        if user_media['meta']['code'] == 200:                                                   #CHECKS IF RECIEVED META CODE IS 200
            if len(user_media['data']):
                image_name = user_media['data'][0]['id'] + '.jpeg'
                image_url = user_media['data'][0]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print colored('Your image has been downloaded!', 'blue')
            else:
                print colored('Post does not exist!', 'red')
        else:
            print colored('Status code other than 200 received!', 'red')

# __________________________________________________________________________________________________________________________________________________

#FUNTION TO GET POST ID WHICH ACCEPTS USERNAME AS ARGUEMENT
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!','red')
    else:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_media = requests.get(request_url).json()                                   #STORES JSON OBJECT RESPONSE IN A VARIABLE
        if user_media['meta']['code'] == 200:                                           #CHECKS IF RECIEVED META CODE IS 200
            try:
                if len(user_media['data']):
                    return user_media['data'][0]['id']                                      #RETURN RECENT POST ID
                else:
                    print colored('There is no recent post of the user!','red')
                    exit()
            except KeyError:
                print colored("Unable to process your request. Please try again!!",'red')
        else:
            print colored('Status code other than 200 received!','red')
            exit()

# __________________________________________________________________________________________________________________________________________________

#FUNTION TO GET LIST OF USERNAMES WHO HAVE LIKE THE RECENT POST OF GIVEN USERNAME
def get_like_list(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!', 'red')
    else:
        post_id = get_post_id(insta_username)
        if post_id == None:                                                             #CHECKS FOR VALID POST ID
            print colored('User does not exist!','red')
        else:
            try:
                request_url=(BASE_URL+'media/%s/likes?access_token=%s') %(post_id,APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url)
                like_list = requests.get(request_url).json()                                #STORES JSON OBJECT RESPONSE IN A VARIABLE
                if len(like_list['data']):
                    print colored('These are the usernames that have liked your recent post:','green')
                    for i in range(len(like_list['data'])):                                 #FOR LOOP ITERATES THROUGH LENGTH OF DATA AND PRINTS USERNAMES WHO HAVE LIKED THE POST
                            print colored('username: %s','blue') %(like_list['data'][i]['username'])
                else:
                    print colored('User\'s recent post has no likes yet!','red')
            except KeyError:
                    print colored("Unable to process your request. Please try again!!",'red')

# __________________________________________________________________________________________________________________________________________________


#FUNTION TO MAKE A LIKE ON RECENT POST
def like_a_post(insta_username):
    user_id=get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!','red')
    else:
        media_id=get_post_id(insta_username)                                            #GETTING MEDIA ID OF POST IN VARIABLE
        request_url=(BASE_URL+"media/%s/likes") %(media_id)
        payload={"access_token":APP_ACCESS_TOKEN}                                       #PAYLOAD IS BODY OF POST REQUEST. HERE ITS ACCESS TOKEN
        print 'POST request url : %s' % (request_url)
        try:
            post_a_like = requests.post(request_url, payload).json()                        #STORES JSON OBJECT RESPONSE IN A VARIABLE
            if post_a_like['meta']['code'] == 200:                                          #CHECKS IF RECIEVED META CODE IS 200
                print colored('Like was successful!','blue')
            else:
                print colored('Your like was unsuccessful. Try again!','red')
        except KeyError:
                print colored("Unable to process your request. Please try again!!",'red')

# __________________________________________________________________________________________________________________________________________________

def unlike_a_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!', 'red')
    else:
        media_id = get_post_id(insta_username)
        request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_id,APP_ACCESS_TOKEN)
        print 'DELETE request url: %s'%(request_url)                                    #PRINTS DELETE REQUEST URL
        unlike_post=requests.delete(request_url).json()                                 #STORES JSON OBJECT RESPONSE IN A VARIABLE
        if unlike_post['meta']['code'] == 200:                                          #CHECKS IF RECIEVED META CODE IS 200
            print colored('Unike was successful!','blue')
        else:
            print colored('Your Unlike was unsuccessful. Try again!','red')

# __________________________________________________________________________________________________________________________________________________

def get_comment_list(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!', 'red')
    else:
        post_id = get_post_id(insta_username)                                           #GETTING MEDIA ID OF POST IN VARIABLE
        if post_id == None:
            print colored('User does not exist!','red')
            exit()
        try:
            request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (post_id, APP_ACCESS_TOKEN)
            print 'GET request url : %s' % (request_url)
            comment_list=requests.get(request_url).json()                                                       #STORES JSON OBJECT RESPONSE IN A VARIABLE
            if len(comment_list['data']):
                print 'These are the usernames that have commented on your recent post:'
                for i in range(len(comment_list['data'])):                                                      #FOR LOOP  ITERATES THROUGH LENGTH OF DATA AND PRINTS USERNAMES AND THEIR COMMENTS
                        print colored('username: %s','blue') %(comment_list['data'][i]['from']['username'])
                        print colored('comment: %s \n','blue') %(comment_list['data'][i]['text'])
            else:
                print colored('User\'s recent post has no comments yet!','red')
        except KeyError:
                print colored("Unable to process your request. Please try again!!",'red')

# __________________________________________________________________________________________________________________________________________________


#FUNTION TO MAKE COMMENT ON RECENT POST OG UTL
def post_a_comment(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!', 'red')
    else:
        media_id = get_post_id(insta_username)                                                  #GETTING MEDIA ID OF POST IN VARIABLE
        comment_text = raw_input("Your comment: ")                                              #ASKING FOR USER INPUT FOR COMMENT
        try:
            payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}                     #HERE PAYLOAD IS ACCESS TOKEN AND COMMENT TEXT TO BE POSTED
            request_url = (BASE_URL + 'media/%s/comments') % (media_id)
            print 'POST request url : %s' % (request_url)                                           #PRINTS POST REQUEST URL
            make_comment = requests.post(request_url, payload).json()                               #STORES JSON OBJECT RESPONSE IN A VARIABLE
            if make_comment['meta']['code'] == 200:                                                 #CHECKS IF RECIEVED META CODE IS 200
                print colored("Successfully added a new comment!",'blue')
            else:
                print colored("Unable to add comment. Try again!",'red')
        except :
            print colored("Unable to process your request. Please try again!!",'red')

# __________________________________________________________________________________________________________________________________________________

#FUNCTIION GETS THE RECENT POST LIKED BY SELF
def recent_liked():
        request_url=(BASE_URL+'users/self/media/liked?access_token=%s') %(APP_ACCESS_TOKEN)
        print 'GET request url: %s' %(request_url)
        recent_liked_media=requests.get(request_url).json()
        try:
            if recent_liked_media['meta']['code']==200:
                if len(recent_liked_media['data']):
                    image_name = 'recent_liked' + '.jpeg'
                    image_url = recent_liked_media['data'][0]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)
                    print colored('Your image has been downloaded!', 'blue')
                else:
                    print colored('Post does not exist!', 'red')
            else:print colored('Status code other than 200 received!','red')
        except KeyError:
            print colored("Unable to process your request. Please try again!!",'red')


# __________________________________________________________________________________________________________________________________________________


#FUNTION TO DELETE NEGATIVE COMMENT ON RECENT POST OF GIVEN USERNAME
def delete_negative_comment(insta_username):

    media_id = get_post_id(insta_username)                                                  #GETTING MEDIA ID OF POST IN VARIABLE
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()                                         #STORES JSON OBJECT RESPONSE IN VARIABLE
    try:
        if comment_info['meta']['code'] == 200:                                                 #CHECKS IF RECIEVED META CODE IS 200
            if len(comment_info['data']):
                #for loop iterage through each comment in comment_info
                for x in range(0, len(comment_info['data'])):
                    comment_id = comment_info['data'][x]['id']                                  #storing comment id in comment_id variable
                    comment_text = comment_info['data'][x]['text']                              #storing comment text in comment_text
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())                #Textblob() takes comment text and analyzer as arguement
                    if (blob.sentiment.p_neg > blob.sentiment.p_pos):                           #checks if comment_text is more positive than negative
                        print colored('Negative comment : %s','red') % (comment_text)
                        delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                        print 'DELETE request url : %s' % (delete_url)
                        delete_info = requests.delete(delete_url).json()

                        if delete_info['meta']['code'] == 200:                                  #CHECKS IF RECIEVED META CODE IS 200
                            print colored('Comment successfully deleted!\n','blue')
                        else:
                            print colored('Unable to delete comment!','red')
                    else:
                        print colored('Positive comment : %s\n','blue') % (comment_text)
            else:
                print colored('There are no existing comments on the post!','red')
        else:
            print colored('Status code other than 200 received!','red')
    except KeyError:
            print colored("Unable to process your request. Please try again!!",'red')
# __________________________________________________________________________________________________________________________________________________

#FUNCTION TO POST COMMENTS ON EACH POST HAVING GIVEN TAG.
#TAKES TWO ARGUEMENTS-- POSTS LIST WITH HAVING GIVEN TAG AND COMMENT TEXT
def multi_comment(tag_list,comment_text):
    try:
        if tag_list['meta']['code'] == 200:
            if len(tag_list['data']):
                for i in range(len(tag_list['data'])):
                    post_id = tag_list['data'][i]['id']

                    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
                    request_url = (BASE_URL + 'media/%s/comments') % (post_id)
                    print 'POST request url : %s' % (request_url)
                    make_comment = requests.post(request_url, payload).json()                           #STORES JSON OBJECT RESPONSE IN A VARIABLE
                    if make_comment['meta']['code'] == 200:                                             #CHECKS IF RECIEVED META CODE IS 200
                        print colored("Successfully added a new comment!",'blue')
                    else:
                        print colored("Unable to add comment. Try again!",'red')
            else:
                print colored("Tag not found in any post",'red')
        else:
            print colored("Status code other than 200 received!",'red')
    except KeyError:
            print colored("Unable to process your request. Please try again!!",'red')
# __________________________________________________________________________________________________________________________________________________

#FUNCTION ASKS USER IF HE WANTS TO SEE POST WITH MINIMUM LIKES OR SEE POSTS WITH PARTICULAR TEXT IN THEIR CAPTION
def choose_post():
    print colored("Choose post one of following options:",'magenta')
    print "a.Choose post with minimum likes of a username"
    print "b.Choose post with maximum likes of a username"
    print "c.Choose post which has particular text in caption"
    choice=raw_input("Enter your choice: ")
    try:
        if choice=='a':
            user_name=raw_input("Enter username: ")
            user_id=get_user_id(user_name)
            if user_id==None:
                print colored("Username not valid!",'red')
            else:
                request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url)
                user_media = requests.get(request_url).json()                                       #STORES JSON OBJECT RESPONSE IN A VARIABLE

                if user_media['meta']['code'] == 200:                                               #CHECKS IF RECIEVED META CODE IS 200
                    if len(user_media['data']):
                        like_count_list=[]                                                          #DECLARING EMPTY LIST TO STORE NUMBER OF LIKES
                        for i in range(len(user_media['data'])):
                            likes=user_media['data'][i]['likes']['count']                           #GETS LIKES COUNT OF POSTS
                            like_count_list.append(likes)                                           #APPENDS LIKES COUNT IN LIST
                        min_count=min(like_count_list)                                              #GETS MINIMUM NUMBER FROM LIKES COUNT LIST
                        for i in range(len(user_media['data'])):

                            #FINDS THE POST WITH MINIMUM LIKES AND GETS ITS ID AND DOWNLOAD IMAGE
                            if user_media['data'][i]['likes']['count']==min_count:
                                get_id=user_media['data'][i]['id']
                                image_name = get_id + '.jpeg'
                                image_url = user_media['data'][i]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        print colored('Your image has been downloaded!', 'blue')
        elif choice=='b':
            user_name = raw_input("Enter username: ")
            user_id = get_user_id(user_name)
            if user_id == None:
                print colored("Username not valid!", 'red')
            else:
                request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url)
                user_media = requests.get(request_url).json()  # STORES JSON OBJECT RESPONSE IN A VARIABLE

                if user_media['meta']['code'] == 200:  # CHECKS IF RECIEVED META CODE IS 200
                    if len(user_media['data']):
                        like_count_list = []  # DECLARING EMPTY LIST TO STORE NUMBER OF LIKES
                        for i in range(len(user_media['data'])):
                            likes = user_media['data'][i]['likes']['count']  # GETS LIKES COUNT OF POSTS
                            like_count_list.append(likes)  # APPENDS LIKES COUNT IN LIST
                        min_count = max(like_count_list)  # GETS MINIMUM NUMBER FROM LIKES COUNT LIST
                        for i in range(len(user_media['data'])):

                            # FINDS THE POST WITH MINIMUM LIKES AND GETS ITS ID AND DOWNLOAD IMAGE
                            if user_media['data'][i]['likes']['count'] == min_count:
                                get_id = user_media['data'][i]['id']
                                image_name = get_id + '.jpeg'
                                image_url = user_media['data'][i]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        print colored('Your image has been downloaded!', 'blue')


        elif choice=='c':
            user_name = raw_input("Enter username: ")
            user_id = get_user_id(user_name)
            if user_id == None:
                print colored("Username not valid!", 'red')
            else:
                request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url)
                user_media = requests.get(request_url).json()  # STORES JSON OBJECT RESPONSE IN A VARIABLE

                if user_media['meta']['code'] == 200:                                               #CHECKS IF RECIEVED META CODE IS 200
                    if len(user_media['data']):
                        word=raw_input("Enter word you want to search in caption of a post(It's case-sensitive!): ")    #ASKING FOR TEXT USER WANT TO SEARCH FOR IN CAPTION
                        if word.isspace()==True or len(word)==0:
                            print colored("Word cannot be empty. Try again!",'red')
                        else:
                            count=0
                            for i in range(len(user_media['data'])):                                #LOOP ITERATES THROUGH ITEMS IN JSON ARRAY- DATA
                                caption=user_media['data'][i]['caption']['text']
                                if word in caption:                                                 #GETS THE POST IF WORD IS FOUND IN CAPTION OF POST
                                    print "Post id is: %s" %(user_media['data'][i]['id'])
                                    print "Caption: %s\n" %(caption)
                                    get_id = user_media['data'][i]['id']
                                    image_name = get_id + '.jpeg'
                                    image_url = user_media['data'][i]['images']['standard_resolution']['url']
                                    urllib.urlretrieve(image_url, image_name)
                                    print colored('Your image has been downloaded!', 'blue')
                                    count+=1                                                        #INCREMENTS COUNT BY 1

                                    #WE CAN FETCH ANY POST DETAIL BUT HERE I AM DOWNLOADING THE POST AND PRINTTING ITS CAPTION AND ID

                            if count==0:                                                            #SO IF COUNT WAS NEVER INCREMENTED MEANS WORD IS NOT IN ANY CAPTION
                                print colored("Entered word is not in caption of any post!",'red')
                    else:
                        print colored("This user has no media. Try again!",'red')
                else:
                    print colored("Status code other than 200 recieved",'red')

        else:
            print colored("Wrong choice!! Try again.",'red')
    except:
        print colored("Unable to process your request. Please try again!!",'red')

# __________________________________________________________________________________________________________________________________________________

#FUNCTION TO SELECT IF USER WANT TO POST FIXED COMMENT OR CUSTOM COMMENT ON POSTS HAVING SPECIFIED TAG NAME
def marketing_comment(tag_name):
    if tag_name.isspace()==True or len(tag_name)==0:
        print colored("Tag is empty. Try again!",'red')
    else:
        print "Select from following options for commenting on posts: "
        print "a. Fixed comment to promote acadview"
        print "b. Custom comment"
        choice=raw_input("Enter your choice: ")
        request_url=(BASE_URL+'tags/%s/media/recent?access_token=%s') %(tag_name,APP_ACCESS_TOKEN)
        print "GET request url: %s" %(request_url)
        try:
            tag_list=requests.get(request_url).json()                                       #STORES JSON OBJECT RESPONSE IN A VARIABLE
            if choice=='a':
                comment_text = "Join Acadview to become Full Stack Developer and get a job!"
                multi_comment(tag_list,comment_text)
            elif choice=='b':
                comment_text=raw_input("Enter the comment you want to post: ")
                multi_comment(tag_list,comment_text)
            else:
                print colored("Wrong choice!",'red')
        except:
            print colored("Unable to process your request. Please try again!!",'red')

# __________________________________________________________________________________________________________________________________________________

#function to ask users user for task they want to perform and calls the function accordingly
def start_bot():
    while True:
            print '\n'
            print colored("___________________________ | _/\_  INSTABOT  _/\_ | ___________________________",'magenta')
            print colored('Hey! Welcome to instaBot!','blue')
            print colored('Here are your menu options:','blue')
            print "a.Get your own details\n"
            print "b.Get details of a user by username\n"
            print "c.Get your own recent post\n"
            print "d.Get the recent post of a user by username\n"
            print "e.Get a list of people who have liked the recent post of a user\n"
            print "f.Like the recent post of a user\n"
            print "g.Unlike the recent post of a user\n"
            print "h.Get a list of comments on the recent post of a user\n"
            print "i.Make a comment on the recent post of a user\n"
            print "j.Delete negative comments from the recent post of a user\n"
            print "k.To do targeted comments on posts for marketing\n"
            print "l.To choose post with minimum or maximum likes or post which has particular text in caption\n"
            print "m.Get recent post liked by you\n"
            print "n.Exit"

            choice = raw_input("Enter you choice: ")
            if choice == "a":
                self_info()
            elif choice == "b":
                insta_username = raw_input("Enter the username of the user: ")
                get_user_info(insta_username)
            elif choice=="c":
                get_own_post()
            elif choice=="d":
                insta_username = raw_input("Enter the username of the user: ")
                get_user_post(insta_username)
            elif choice=="e":
                insta_username = raw_input("Enter the username of the user: ")
                get_like_list(insta_username)
            elif choice=="f":
                insta_username = raw_input("Enter the username of the user: ")
                like_a_post(insta_username)
            elif choice=="g":
                insta_username = raw_input("Enter the username of the user: ")
                unlike_a_post(insta_username)
            elif choice=="h":
                insta_username = raw_input("Enter the username of the user: ")
                get_comment_list(insta_username)
            elif choice=="i":
                insta_username = raw_input("Enter the username of the user: ")
                post_a_comment(insta_username)
            elif choice=="j":
                insta_username = raw_input("Enter the username of the user: ")
                delete_negative_comment(insta_username)
            elif choice=='k':
                tag_name=raw_input('Enter tag name you want to market your product(without leading "#"): ')
                marketing_comment(tag_name)
            elif choice=='l':
                choose_post()
            elif choice=='m':
                recent_liked()
            elif choice == "n":
                exit()
            else:
                print colored("wrong choice",'red')


# __________________________________________________________________________________________________________________________________________________

#CALL TO start_bot() function
start_bot()

