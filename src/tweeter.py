import tweepy
import keys
from time import sleep
import datetime


class Tweeter(object):
    def __init__(self):
        self.consumer_key = keys.consumer_key
        self.consumer_secret = keys.consumer_secret
        self.key = keys.access_token
        self.secret = keys.access_secret
        self.next_tweet_at = None

    def send_tweet(self, formula):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)
        api = tweepy.API(auth)
        api.update_status(formula.convert_to_tweet())
        self.next_tweet_at = datetime.datetime.now() + datetime.timedelta(minutes=3*60)

    def tweet_tautology(self, formula):
        if not self.next_tweet_at:
            self.send_tweet(formula)
        else:
            difference = self.next_tweet_at - datetime.datetime.now()
            difference_in_minutes = difference.total_seconds() / 60
            if 0 <= difference_in_minutes < 3*60:
                sleep((3*60 - difference_in_minutes) * 60)
            self.send_tweet(formula)


if __name__ == "__main__":
    tweeter = Tweeter()
    tweeter.tweet_tautology()