import re
import emoji
from nltk.corpus import stopwords


def remove_emojis(string):
    emojis = emoji.distinct_emoji_list(string)

    for emoji_char in emojis:
        string = re.sub(emoji_char, "", string)

    return string


def remove_abbreviation(string):
    matches = re.findall(r'(?:[^\.\s]\.){2,}', string)

    if not matches:
        return string

    for match in matches:
        # only remove the . for these words
        if (match == 'أ.د.') or match == ('ا.ل.ل.ق.ا.'):
            string = re.sub(match, lambda match_obj: ' ' + re.sub(
                '\.', "", match_obj.group(0))+' ', string)
        # remove others completely
        else:
            string = re.sub(match, "", string)

    return string


def clean_tweet(tweet):

    # remove <LF>
    tweet = re.sub("<LF>", "", tweet)
    # remove URLs
    tweet = re.sub(r'(https?://\S+)', "", tweet)
    # remove mentions
    tweet = re.sub(r'@\w*', "", tweet)
    # remove hash signs
    tweet = re.sub(r'#', "", tweet)
    # remove abbreviations  except أ.ف.ب … ل.ق.ا.ح
    tweet = remove_abbreviation(tweet)
    # remove english letters
    tweet = re.sub(r'[a-zA-Z]', "", tweet)
    # remove emojis
    tweet = remove_emojis(tweet)
    # replace _ and - with spaces
    tweet = re.sub(r'[_-]', " ", tweet)
    # remove brackets and quotes
    tweet = re.sub(r'[\(\)"]', "", tweet)

    return tweet
