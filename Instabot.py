import requests,urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from termcolor import colored

APP_ACCESS_TOKEN='1415747117.b9cb54b.3d49d10dcde5416cbc03113f3ffd6ad7'
BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
    request_url=BASE_URL+'users/self/?access_token='+APP_ACCESS_TOKEN
    print "GET request url: %s" %(request_url)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print colored('Username: %s','green') % (user_info['data']['username'])
            print colored('No. of followers: %s','green') % (user_info['data']['counts']['followed_by'])
            print colored('No. of people you are following: %s','green') % (user_info['data']['counts']['follows'])
            print colored('No. of posts: %s','green' )% (user_info['data']['counts']['media'])
        else:
            print colored('User does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')

    '''
    Function declaration to get the ID of a user by username
    '''

def get_user_id(insta_username):
        request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_info = requests.get(request_url).json()

        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                return user_info['data'][0]['id']
            else:
                return None
        else:
            print colored('Status code other than 200 received!','red')
            exit()


def get_user_info(insta_username):
        user_id = get_user_id(insta_username)
        if user_id == None:
            print colored('User does not exist!','red')
            exit()
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_info = requests.get(request_url).json()

        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                print colored('Username: %s','green') % (user_info['data']['username'])
                print colored('No. of followers: %s','green') % (user_info['data']['counts']['followed_by'])
                print colored('No. of people %s are following: %s','green') % (user_info['data']['username'],user_info['data']['counts']['follows'])
                print colored('No. of posts: %s','green') % (user_info['data']['counts']['media'])
            else:
                print colored('There is no data for this user!','red')
        else:
            print colored('Status code other than 200 received!','red')

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!','blue')
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!','red')
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!', 'blue')
        else:
            print colored('Post does not exist!', 'red')
    else:
        print colored('Status code other than 200 received!', 'red')

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print colored('There is no recent post of the user!','red')
            exit()
    else:
        print colored('Status code other than 200 received!','red')
        exit()

def get_like_list(insta_username):
    post_id = get_post_id(insta_username)
    if post_id == None:
        print colored('User does not exist!','red')
        exit()
    request_url=(BASE_URL+'media/%s/likes?access_token=%s') %(post_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    like_list = requests.get(request_url).json()
    if len(like_list['data']):
        print colored('These are the usernames that have liked your recent post:','green')
        for i in range(len(like_list['data'])):
                print colored('username: %s','blue') %(like_list['data'][i]['username'])
    else:
        print colored('User\'s recent post has no likes yet!','red')

def like_a_post(insta_username):
    media_id=get_post_id(insta_username)
    request_url=(BASE_URL+"media/%s/likes") %(media_id)
    payload={"access_token":APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print colored('Like was successful!','blue')
    else:
        print colored('Your like was unsuccessful. Try again!','red')

def unlike_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_id,APP_ACCESS_TOKEN)
    print 'DELETE request url: %s'%(request_url)
    unlike_post=requests.delete(request_url).json()
    if unlike_post['meta']['code'] == 200:
        print colored('Unike was successful!','blue')
    else:
        print colored('Your Unlike was unsuccessful. Try again!','red')



def get_comment_list(insta_username):
    post_id = get_post_id(insta_username)
    if post_id == None:
        print colored('User does not exist!','red')
        exit()
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (post_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_list=requests.get(request_url).json()
    if len(comment_list['data']):
        print 'These are the usernames that have commented on your recent post:'
        for i in range(len(comment_list['data'])):
                print colored('username: %s','blue') %(comment_list['data'][i]['from']['username'])
                print colored('comment: %s','blue') %(comment_list['data'][i]['text'])
    else:
        print colored('User\'s recent post has no comments yet!','red')


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print colored("Successfully added a new comment!",'blue')
    else:
        print colored("Unable to add comment. Try again!",'red')

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print colored('Negative comment : %s','red') % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print colored('Comment successfully deleted!\n','blue')
                    else:
                        print colored('Unable to delete comment!','red')
                else:
                    print colored('Positive comment : %s\n','blue') % (comment_text)
        else:
            print colored('There are no existing comments on the post!','red')
    else:
        print colored('Status code other than 200 received!','red')

def multi_comment(tag_list,comment_text):
    if tag_list['meta']['code'] == 200:
        for i in range(len(tag_list['data'])):
            post_id = tag_list['data'][i]['id']

            payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
            request_url = (BASE_URL + 'media/%s/comments') % (post_id)
            print 'POST request url : %s' % (request_url)
            make_comment = requests.post(request_url, payload).json()
            if make_comment['meta']['code'] == 200:
                print colored("Successfully added a new comment!",'blue')
            else:
                print colored("Unable to add comment. Try again!",'red')
    else:
        print colored("Status code other than 200 received!",'red')


def marketing_comment(tag_name):
    print "Select from following options for commenting on posts: "
    print "a. Fixed comment to promote acadview"
    print "b. Custom comment"
    choice=raw_input("Enter your choice: ")
    request_url=(BASE_URL+'tags/%s/media/recent?access_token=%s') %(tag_name,APP_ACCESS_TOKEN)
    print "GET request url: %s" %(request_url)
    tag_list=requests.get(request_url).json()
    if choice=='a':
        comment_text = "Join Acadview to become Full Stack Developer and get a job!"
        multi_comment(tag_list,comment_text)
    elif choice=='b':
        comment_text=raw_input("Enter the comment you want to post: ")
        multi_comment(tag_list,comment_text)
    else:
        print colored("Wrong choice!",'red')

def start_bot():
        while True:
            print '\n'
            print 'Hey! Welcome to instaBot!'
            print 'Here are your menu options:'
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
            print "k.To do targeted comments on posts for marketing"
            print "l.Exit"

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
                tag_name=raw_input('Enter tag name you want to market your product(without "#"): ')
                marketing_comment(tag_name)
            elif choice == "l":
                exit()
            else:
                print colored("wrong choice",'red')

start_bot()
