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
        # died_at is the highest count of the tweet that has been sent before the internet connection died
        self.died_at = 58
        self.tweet_counter = 0

    def send_tweet(self, formula):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)
        api = tweepy.API(auth)
        while True:
            try:
                api.update_status(formula.convert_to_tweet())
                #print(formula.convert_to_tweet())
                break
            except tweepy.error.TweepError as e:
                print(str(e))
            sleep(300)
        self.next_tweet_at = datetime.datetime.now() + datetime.timedelta(hours=3)

    def tweet_tautology(self, formula):
        self.tweet_counter += 1
        if self.tweet_counter > self.died_at:
            if not self.next_tweet_at:
                self.send_tweet(formula)
            else:
                difference = self.next_tweet_at - datetime.datetime.now()
                difference_in_minutes = difference.total_seconds() / 60
                print(self.tweet_counter, ' at:', datetime.datetime.now(), difference, int(difference_in_minutes))
                if 0 < int(difference_in_minutes) <= 180:
                    sleep(difference_in_minutes * 60)
                self.send_tweet(formula)


if __name__ == "__main__":
    tweeter = Tweeter()
    tweeter.tweet_tautology()