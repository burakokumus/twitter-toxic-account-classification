import DataMan #to manipulate data
import got3 as got #to get tweets

#RacistJ0kes

############ get username ############
user = input('Enter your username: ')
num_of_tweets = int(input('Enter number of tweets: '))
tweetCriteria = got.manager.TweetCriteria().setUsername(user).setMaxTweets(100000)

############# get tweets #############

#tweets = TwitterMan.get_tweets(user)
tweet = got.manager.TweetManager.getTweets(tweetCriteria) # list with object type 'Tweet'

############ convert Tweet list to Text list ############
tweets = []
for twet in tweet:
    tweets.append(twet.text)
reduced_list = []
if num_of_tweets >= len(tweets):
    reduced_list = tweets
else:
    for i in range(0, num_of_tweets):
        reduced_list.append(tweets[i])

############ make prediction ############
try:
    predictions = DataMan.get_prediction(reduced_list)
except:
    print('username ', user, ' not found')
    quit()

toxic = predictions['toxic'].mean()
severe_toxic = predictions['severe_toxic'].mean()
obscene = predictions['obscene'].mean()
threat = predictions['threat'].mean()
insult = predictions['insult'].mean()
identity_hate = predictions['identity_hate'].mean()

############ print the result ############

for column in predictions.columns:
    print(column, ":  %", predictions[column].mean() * 100)

print('Number of tweets considered: ' , len(reduced_list))
#print prediction
#print(predictions * 100)

#print(len(tweet))