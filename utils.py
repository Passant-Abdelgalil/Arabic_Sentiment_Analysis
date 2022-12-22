import re
import emoji
from nltk.corpus import stopwords

from camel_tools.utils.dediac import dediac_ar
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.normalize import normalize_alef_maksura_ar, normalize_teh_marbuta_ar, normalize_alef_ar
from camel_tools.tokenizers.morphological import MorphologicalTokenizer

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
        if (match == 'أ.ف.ب.') or match == ('ا.ل.ل.ق.ا.ح.'):
            string = re.sub(match, lambda match_obj: ' ' + re.sub(
                '\.', "", match_obj.group(0))+' ', string)
        # remove others completely
        else:
            string = re.sub(match, "", string)

    return string

def clean_tweet(tweet):

    # remove <LF>
    tweet = re.sub("<LF>", " ", tweet)
    # remove duplicate letters (الوووو -> الو)
    tweet = re.sub(r'(.)\1{2,}', r'\1', tweet)
    # remove URLs
    tweet = re.sub(r'(https?://\S+)', " ", tweet)
    # remove mentions
    tweet = re.sub(r'@\w*', " ", tweet)
    # remove hash signs
    tweet = re.sub(r'#', " ", tweet)
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
    # dediacterize
    tweet = dediac_ar(tweet)
    # TODO: (It is inversed) normalize ه to ة
    # tweet = normalize_teh_marbuta_ar(tweet)

    return tweet

def tokenize_with_dialect(tweet, did, msa_mle, egy_mle):
  # Predict dialect
  dialectid = did.predict([tweet], 'region')[0].top

  dialect_map = {
    'Gulf': msa_mle,
    'Levant': egy_mle,
    'Modern Standard Arabic': msa_mle,
    'Maghreb': egy_mle,
    'Nile Basin': egy_mle,
    'Gulf of Aden': msa_mle
  }

  # Create morphological tokenizer instance
  bw_tokenizer = MorphologicalTokenizer(disambiguator=dialect_map[dialectid], split=True, scheme='bwtok')
  # Generate tokenizations
  tokens = bw_tokenizer.tokenize(simple_word_tokenize(tweet))
  # Filter out tokens with + in them (to remove prefixes and suffixes)
  filtered_tokens = list(filter(lambda token: '+' not in token, tokens))
  return ' '.join(filtered_tokens)

def normalize_chars(tweet):
  # normalize ى to ي
  tweet = re.sub(r'[ى]', "ي", tweet)
  tweet = normalize_alef_maksura_ar(tweet)
  tweet = normalize_alef_ar(tweet)
  return tweet

