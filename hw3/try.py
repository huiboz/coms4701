import sys
import string

def extract_words(text):
    text = text.lower() # convert to lower case


    for p in string.punctuation: # strip
        text = text.replace(p,"")

    list_text = text.split()

    return text.split() # should return a list of words in the data sample.

if __name__ == "__main__":
    extract_words("hAha, ni ge dDd 123!!   df.df.")
