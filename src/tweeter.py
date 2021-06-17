import tweepy
import keys


class Tweeter(object):
    def __init__(self):
        self.consumer_key = keys.consumer_key
        self.consumer_secret = keys.consumer_secret
        self.key = keys.access_token
        self.secret = keys.access_secret

    def tweet_tautology(self, formula):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)

        api = tweepy.API(auth)

        #api.update_status("Hello World!")

        api.update_status("\u00AC \u2227 \u2228 \u21FF \u21FE \u22A5 \u25A1 \u25C7")

        #try:
        #    api.verify_credentials()
        #    print('verification ok')
        #except:
        #    print('Issue during verification')

if __name__ == "__main__":
    tweeter = Tweeter()
    tweeter.tweet_tautology()