"""PageRank of twitter pages of Amitabh Bachchan and Narendra Modi."""

import tweepy
import time
import numpy as np
from page_rank import PageRank
import pickle


def get_followers(api, screen_name, follower_limit=500):
    """Get the followers of a user using screen name."""
    user_followers = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
        user_followers.extend(page)
        print("Got {} followers".format(str(len(page))))
        if len(user_followers) > follower_limit:
            break
        time.sleep(4)
    user_followers = user_followers[0:follower_limit]
    return user_followers


def get_follower_matrix(api, screen_name, follower_limit=500):
    """Get the follower matrix of a user using screen name."""
    user_followers = get_followers(api, screen_name, follower_limit)
    user = api.get_user(screen_name)

    pages = dict()
    pages[user.id] = 0
    for i, user_id in enumerate(user_followers):
        pages[user_id] = i+1

    follwer_matrix = np.zeros((len(pages), len(pages)), dtype=int)
    follwer_matrix[0] = np.ones((1, len(pages)))

    for user_id in user_followers:
        user = api.get_user(user_id)
        time.sleep(4)
        second_followers = get_followers(api, user.screen_name, follower_limit)
        for follower in second_followers:
            try:
                follwer_matrix[pages[follower], user_id] = 1
            except:
                continue
    pickle.dump(follwer_matrix, open(screen_name+".pkl", "wb"))
    return follwer_matrix


def main(user, follower_limit=500):
    """Main."""
    print("Finding PageRank for user {}".format(user))
    ACCESS_TOKEN = '719518948547387392-yDU25e2hdHrmmQw5kFNfNCrjyIg1Hd7'
    ACCESS_SECRET = '1c4B6nZSblmXgEKSQ4KBsckWIFTRurNeJJ6IeA99rFSkD'
    CONSUMER_KEY = 'fTIqmDkfG06In6kzkPI1aWhp9'
    CONSUMER_SECRET = '7kgdIT2HZbITad2Nkghi6B4di9eRs7PjwEFbIWuvmtZfV24Xl0'

    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    oauth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(oauth)

    print("Getting Followers and second followers")
    try:
        follower_matrix = get_follower_matrix(api, user, follower_limit)
    except:
        try:
            follower_matrix = pickle.load(open(user+".pkl", "rb"))
        except FileNotFoundError:
            print("Could not retrieve data from Twitter and no offline data available.")

    print("Calculating PageRank")
    PR = PageRank(follower_matrix.shape[0], follower_matrix)
    PR.iterate(20)

    rank = PR.page_scores[0]
    print("Rank of user {} is {}".format(user, str(rank)))


if __name__ == "__main__":
    main("SrBachchan", 10)

    time.sleep(30)

    main("narendramodi", 10)
