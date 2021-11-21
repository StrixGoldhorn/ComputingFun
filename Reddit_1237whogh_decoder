import praw
import time

def init_vars():
    # replace asterisks with relevant field
    reddit = praw.Reddit(client_id='********',
                        client_secret='********',
                        password='********',
                        user_agent='********',
                        username='********')
    subreddit = reddit.subreddit('1237whogh')
    
    #caesar shift amount
    shift = 7
    return reddit, subreddit, shift

def caesarshift(ct, shift):
    pt = ''
    for i in ct:
        if(i.isupper()):
            pt += chr((ord(i) + shift-65) % 26 + 65)
        elif(i.islower()):
            pt += chr((ord(i) + shift - 97) % 26 + 97)
        else:
            pt += i
    return pt

def main():
    reddit, subreddit, shift = init_vars()
    
    # gather title of replied posts
    replied = []
    with open('redditbot_replied', 'r') as f:
        replied = f.read().splitlines()
    print(replied)

    for submission in subreddit.new(limit = 20):
        id = submission.id
        submission = reddit.submission(id = id)

        # decode the submission
        ct = submission.title+'\n'+submission.selftext
        pt = caesarshift(ct, shift)
        
        # check if replied, and see if user confirm want to reply
        if(submission.title not in replied):
            print('----------||----------')
            print('NEW POST')
            print('----------------------')
            print(pt)
            print('----------------------')
            usercheck = input('Reply to post? (Y/n) ')
            if usercheck == 'Y':
                # submission.reply(pt)
                print('REPLIED')
            with open('redditbot_replied', 'a') as f:
                f.write(submission.title+'\n')

        else:
            print('----------||----------')
            print(submission.title, 'PREVIOUSLY REPLIED')
            print('----------------------')

        # time delay to prevent too many requests
        time.sleep(3)
    
    print("FINISHED")

if __name__ == '__main__': main()        
