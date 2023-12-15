import re
import itertools
import pandas as pd

'''
    Tools to analyze text content from ANES election survey results.

    This module is used after data has been loaded in read_data.py

    It provides the following tools:
     - given a piece of text, calculate the frequency of each word (removing stopwords, if necessary)
     - given a text column, calculates the total word frequency across all values in the column
     - given two word frequency distributions, calculates the deltas in between them (finds the largest differences)
'''

DEFAULT_STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'don', 'must', 'dont']

def get_unique_words(text, stopwords=DEFAULT_STOPWORDS):
    """
    Given a piece of text, returns all unique words in the text. This also
    converts the text to lowercase, removes punctuation, joins negations 
    (by replacing "not word" with "not_word"), removes stopwords, and 
    removes words of 2 or fewer characters.
    
    Parameters
    ----------
    text : str 
      The text string from which to calculate all unique words

    stopwords : list (optional)
      A list of stopwords (or "filler words") to ignore from our final list of unique words.
      Defaults to ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'don', 'must', 'dont']
    
    Returns
    -------
    list(str)
      A list of strings, each of which is a unique word in our original input text

    Examples
    --------
    >>> get_unique_words("This is a sentence, it is a long sentence...", stopwords=[])
    ['long', 'sentence', 'this']
    >>> get_unique_words("This is a sentence, it is a long sentence...")
    ['long', 'sentence']
    """

    
    # Converts the text to lowercase
    text = text.lower()

    # Removes all punctuation
    replace_punctuation_re = re.compile('[^\w\s_]')
    text = re.sub(replace_punctuation_re, ' ', text)

    # Replaces not/isn't/never words
    negation_re = re.compile("(?:n't|not|never)\s(.+?)\Z")
    text = re.sub(negation_re, r"not_\g<1>", text)

    # Split by spaces
    words = text.split()
    words = [word for word in words if word]

    # Because we are calculating the % of comments that mention a word,
    # we do not want to double-count when a comment mentions a word twice.
    # Because of this, we will find the set of unique words instead
    words = list(set(words))

    # Remove any word that is found in stopwords
    words = [x for x in words if x not in stopwords]

    # Remove any word that is 2 or fewer characters
    words = [x for x in words if len(x) > 2]

    return words

from collections import Counter
def get_word_frequencies(series):
    """
    Given a Pandas Series, calculates the total word frequency across all items in the series.
    This calculates the unique words across each item in the series, and then finds
    the percentage of items in the series which contain each unique word.
    
    Parameters
    ----------
    series : Pandas.Series 
      The series from which we will calculate all word frequency (assumed to contain
      open-ended comments)
    
    Returns
    -------
    dict
      A dict of word: frequency pairs.

    Examples
    --------
    >>> import pandas as pd
    >>> sentences = pd.Series(["This is a sentence, it is a long sentence...", "This is another sentence", "A third sentence"])
    >>> analyze.get_word_frequencies(sentences)
    {'long': 0.3333333333333333,
     'sentence': 1.0,
     'another': 0.3333333333333333,
     'third': 0.3333333333333333}
    """
    
    # Replace NA with blanks
    series = series.fillna('')
    
    unique_words = series.astype(str).apply(get_unique_words).values

    # Our total count will be the number of non-blank values in unique words
    unique_count = len([x for x in unique_words if x])
    
    # Flattens from list of lists to a single list of all words
    unique_words = list(itertools.chain(*unique_words))
    
    word_counts = Counter(unique_words)
    # Converts from word counts to word frequencies
    word_frequencies = {}
    for word, count in word_counts.items():
        word_frequencies[word] = count / unique_count
    return word_frequencies

def compare_word_frequencies(group_1_series, group_2_series):
    """
    Given two Pandas Series objects, calculate the frequency of each word in each
    series, as well as the difference in frequency between the two series.
    
    Parameters
    ----------
    group_1_series : Pandas.Series 
      The first series from which we will calculate word frequency

    group_2_series : Pandas.Series 
      The second series from which we will calculate word frequency
    
    Returns
    -------
    list
      A list of dicts of frequency information, where each dict contains: 
      word, group_1 (frequency in group_1_series), group_2 (frequency in group_2_series),
      and delta (group1 - group2)

    Examples
    --------
    >>> group_1_series = pd.Series(["This is a sentence, it is a long sentence...", "This is another sentence", "A third sentence"])
    >>> group_2_series = pd.Series(["These are sentences", "This is also a sentence", "All of these are sentences happily"])
    >>> analyze.compare_word_frequencies(group_1_series, group_2_series)
    [{'word': 'sentences',
      'group_1': 0.0,
      'group_2': 0.6666666666666666,
      'delta': -0.6666666666666666},
     {'word': 'happily',
      'group_1': 0.0,
      'group_2': 0.3333333333333333,
      'delta': -0.3333333333333333},
     {'word': 'also',
      'group_1': 0.0,
      'group_2': 0.3333333333333333,
      'delta': -0.3333333333333333},
     {'word': 'third',
      'group_1': 0.3333333333333333,
      'group_2': 0.0,
      'delta': 0.3333333333333333},
     {'word': 'long',
      'group_1': 0.3333333333333333,
      'group_2': 0.0,
      'delta': 0.3333333333333333},
     {'word': 'another',
      'group_1': 0.3333333333333333,
      'group_2': 0.0,
      'delta': 0.3333333333333333},
     {'word': 'sentence',
      'group_1': 1.0,
      'group_2': 0.3333333333333333,
      'delta': 0.6666666666666667}]
    """
    
    group_1_frequencies = get_word_frequencies(group_1_series)
    group_2_frequencies = get_word_frequencies(group_2_series)
    
    # Returns a list of dicts for each word that has the frequency in each group
    # This can then be sorted by delta and multiple
    word_frequency_differences = []
    
    for word in set(list(group_1_frequencies.keys()) + list(group_2_frequencies.keys())):
        word_info = {}
        word_info["word"] = word
        word_info["group_1"] = group_1_frequencies.get(word, 0.0)
        word_info["group_2"] = group_2_frequencies.get(word, 0.0)
        word_info["delta"] = word_info["group_1"] - word_info["group_2"]        
        
        word_frequency_differences.append(word_info)

    word_frequency_differences = sorted(word_frequency_differences, key=lambda x: x["delta"])
    
    return word_frequency_differences

def summarize_word_frequency_differences(group_1_series, group_2_series, group_1_label="Group 1", group_2_label="Group 2", num_words=10):
    """
    Given two Pandas Series objects, summarize the difference in frequency between 
    the two series. This first calculates the frequency of each word in each series, 
    and then prints out a summary of the words that are more frequent in each of 
    group_1_series and group_2_series, respectively.
    
    Parameters
    ----------
    group_1_series : Pandas.Series 
      The first series from which we will calculate word frequency

    group_2_series : Pandas.Series 
      The second series from which we will calculate word frequency

    group_1_label : str (optional)
      A label to use when printing the output summary for group_1_series

    group_2_label : str (optional)
      A label to use when printing the output summary for group_2_series

    num_words : int (optional)
      The number of words to print out in each summary (default to 10)
    
    Returns
    -------
    list
      A list of dicts of frequency information, where each dict contains: 
      word, group_1 (frequency in group_1_series), group_2 (frequency in group_2_series),
      and delta (group1 - group2)

    Examples
    --------
    >>> group_1_series = pd.Series(["This is a sentence, it is a long sentence...", "This is another sentence", "A third sentence"])
    >>> group_2_series = pd.Series(["These are sentences", "This is also a sentence", "All of these are sentences happily"])
    >>> analyze.summarize_word_frequency_differences(group_1_series, group_2_series)
    These words occurred more often in Group 1:
           word  Group 1 freq  Group 2 freq
    0  sentence    100.000000     33.333333
    1     third     33.333333      0.000000
    2      long     33.333333      0.000000
    3   another     33.333333      0.000000
    These words occurred more often in Group 2:
            word  Group 1 freq  Group 2 freq
    0  sentences           0.0     66.666667
    1    happily           0.0     33.333333
    2       also           0.0     33.333333
    """
    
    word_frequency_differences = compare_word_frequencies(group_1_series, group_2_series)

    for reverse in [True, False]:
        top_words = sorted(word_frequency_differences, key=lambda x: x["delta"], reverse=reverse)

        # Filter to words where the delta is > or < 0 appropriately  
        if reverse:            
            top_words = [x for x in top_words if x["delta"] > 0]
        else:
            top_words = [x for x in top_words if x["delta"] < 0]
        
        print(f"\n\nThese words occurred more often in {[group_2_label, group_1_label][reverse]}:")        
        
        df = pd.DataFrame(top_words, columns=["word", "group_1", "group_2"])
        df['group_1'] = (df['group_1'] * 100)
        df['group_2'] = (df['group_2'] * 100)
        df = df.rename(columns={'group_1': group_1_label + " freq", 'group_2': group_2_label + " freq"})
        print(df.head(num_words))

    