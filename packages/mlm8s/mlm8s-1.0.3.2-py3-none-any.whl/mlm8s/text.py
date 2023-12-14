import re
import nltk
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import string
import os


def build_re_pattern(liste):
  """
  creates regular-expression pattern-string
  for a list of words.
  """
  pattern = ''.join([' '+w+r'\b|' for w in liste])[:-1]
  return pattern

def _load_data(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'data', file_name)
    return np.load(file_path)

_names_pattern = build_re_pattern(_load_data('english_names.npy'))
_opinionated_pattern = build_re_pattern(_load_data('opinionated.npy'))
_stopword_pattern = build_re_pattern(_load_data('stopwords.npy'))

def custom_standardization(input_data):
  """
  standadizes text strings
  eg: for text-vectorization via keras
  """
  stripped = tf.strings.regex_replace(input_data, _names_pattern, ' ')
  stripped = tf.strings.lower(stripped)
  stripped = tf.strings.regex_replace(stripped, _stopword_pattern, ' ')
  stripped = tf.strings.regex_replace(stripped, '<br />', ' ')
  stripped = tf.strings.regex_replace(stripped,
                                      '[%s]' % re.escape(string.punctuation),
  
                                      '')
  # clean newline and words that are split by newline
  # also kills digits
  stripped = tf.strings.regex_replace(stripped, r'\n|'+r'-\n|'+r'\t', '')
  # clean single letters
  stripped = tf.strings.regex_replace(stripped, '(^| ).(( ).)*( |$)', ' ')
  # replace numbers that are not part of a word
  # Note: needs to run 2x
  stripped = tf.strings.regex_replace(stripped, r'(\A|[. ,])\d+([. ,]|$)', '  ')
  stripped = tf.strings.regex_replace(stripped, r'(\A|[. ,])\d+([. ,]|$)', '  ')
  return stripped

def build_vocab(dataset_train, standardization, batchsize=128, max_tokens=130_000):
  """
  builds vocabulary from dataset with custom_standardization
  """
  vectorize = tf.keras.layers.TextVectorization(
    max_tokens=max_tokens,
    standardize=standardization,
    split='whitespace',
    output_mode='int')
  # create vocabulary from train_ds
  text_only_ds = dataset_train.map(lambda x, y: x).batch(batchsize)
  vectorize.adapt(text_only_ds)
  vocab = vectorize.get_vocabulary()
  return vocab

def stemm(vocab):
  """
  stemm via nltk.snowball
  """
  stemmed = [nltk.stem.SnowballStemmer("english").stem(word) for word in vocab]
  return stemmed

def plot_stemming_efficiency(stemmed, min_vocab_size = 3000):
  """
  helps with choosing the right min_vocab_size
  by plotting relative stemming efficiency.

  args:
        stemmed - list of stemmed vocabulary that is far to long 
        min_vocab_size - integer of current estimation that gets
                         marked in the plot
  """
  min_vocab_k = tf.cast(min_vocab_size/1000, dtype=tf.int32)
  stemming_efficiency = lambda i: ((i-len(set(stemmed[:i]))) / len(set(stemmed[:i])))
  stemming_efficiency = [stemming_efficiency(i) for i in range(1, len(stemmed), 1000)]
  plt.figure(figsize=(10, 3))
  plt.title('relative stemming efficiency:')
  plt.xlabel('size of vocabulary in 1000s')
  plt.ylabel('efficiency')
  plt.plot(stemming_efficiency)
  plt.plot(stemming_efficiency[:min_vocab_k])
  return min_vocab_size

def build_lookup(keys, values, min_keys=3000, verbose=False):
  """
  build lookup-dict from unique but non-bijective key-value pairs
  note: <keys> and <values>   should correspond to eachother and
                                     be ordered according to frequency

  args:
        keys           - list of keys that is far to long 
        values         - list of values that is far to long
        min_keys       - integer that describes the number of 
                         unique lookup values. Defaults to 3000,
                         wich is the average number of words an
                         educated not-native english-speaker knows

  returns: lookup-dict with at least <min_keys> key-value pairs
  
  """
  table = [list(z) for z in zip(keys, values) if z[1] in stemmed[:min_keys]]
  table = dict(table)
  if verbose:
    print(str(len(table.keys())) + ' different words will be mapped to ' + 
          str(len(set(table.values()))) + ' unique tokens')
  return table

def custom_split(text):
  """
  spitter that can be used within tf.keras.layers.TextVectorization

  """
  split = tf.strings.regex_replace(text, ' +', ' ')
  split = tf.strings.split(split, sep=' ')
  return split

def reduce_freq(look_up_table, min_keys=3000, verbose=False):

  """
  builds lookup-dictionaries from unique but non-bijective key-value pairs
                             that have reduced size

  note: <keys> and <values>  should correspond to eachother and
                                    be ordered according to frequency

        keys that have values that are not within
        the most frequent <min_keys> will return 0

  args:
        look_up_table[0]    - list of keys that shall be reduced
        look_up_table[1]    - list of values that shall be reduced
        min_keys            - integer that describes the number of
                              unique lookup values. Defaults to 3000,
                              wich is the average number of words an
                              educated not-native english-speaker knows

  returns: lookup-dictionaries with at least <min_keys> key-value pairs

           keys2values:
                              keys -> values for values wich have keys
                              that are most frequent (top <min_keys>)
           top_values2range:
                              values from keys2values -> integer
                              wich inreases approximatly
                              with decreasing key-frequency
           keys2int:
                              keys from keys2values -> int
                              according to top_values2range
           range2int:
                              like keys2values, but with integer-keys
                              and -values that correspond to frequency:
                              higher int -> lower frequency

  """

  keys, values = look_up_table

  zero = tf.constant(0, dtype=tf.int64)
  lookup_table = [list(z) for z in zip(keys, values) if z[1] in values[:min_keys]]
  keys2values = dict(lookup_table)
  unique_values = list(dict.fromkeys(keys2values.values()))
  top_values2range = dict(zip(unique_values,
                              1+tf.range(len(unique_values), dtype=tf.int64)))
  keys2int = {key: top_values2range.get(values[i])
                   for i, key in enumerate(keys)}
  keys2int = {key: value
                   for key, value in keys2int.items()
                   if value!=None}
  range2int = {i+1: keys2int.get(key) for i, key in enumerate(keys)
                                    if keys2int.get(key) != None}

  if verbose:
    print(str(len(lookup_table)) + ' different words will be mapped to ' +
          str(len(unique_values)) + ' unique tokens')

  return keys2values, top_values2range, keys2int, range2int


class LookUp(tf.keras.layers.Layer):
  
  """
  Class is depreciated and will be remvoved in future updates
  """
  
  def __init__(self, standardize, split, lookup):
    super(LookUp, self).__init__()
    self.standardize = standardize
    self.split = split
    keys = list(lookup.keys())
    values = list(lookup.values())
    values = tf.strings.to_hash_bucket_strong(values, len(values), [2, 42])
    lookup =  tf.lookup.KeyValueTensorInitializer(keys, values)
    self.lookup = tf.lookup.StaticVocabularyTable(lookup, num_oov_buckets = 1)
    self._name = 'lookup'
    
  def call(self, inputs):
    text = self.standardize(inputs)
    words = self.split(text)
    words = tf.ragged.map_flat_values(self.lookup.lookup, words)
    return words


class Tokenizer(tf.keras.layers.Layer):
  
  def __init__(self, standardize, split, lookup, output_sequence_length=None):
    super(Tokenizer, self).__init__()
    self._standardize = standardize
    self._split = split
    keys = list(lookup.keys())
    values = list(lookup.values())
    lookup =  tf.lookup.KeyValueTensorInitializer(keys, values)
    self._lookup = tf.lookup.StaticHashTable(lookup, default_value=0)
    self._output_sequence_length = output_sequence_length
    self._name = 'tokenizer'
    
  def pad_and_trunc(self, x):
    """
    input: ragged tensor with shape: [batchsize, None]
    output: tensor with shape: [batchsize, output_sequence_length]
    """
    x = x.to_tensor()
    shape = tf.shape(x)
    x = x[..., :self._output_sequence_length]
    shape = tf.shape(x)
    padded_shape = tf.concat((shape[:-1], [self._output_sequence_length]), 0)
    padding, _ = tf.required_space_to_batch_paddings(shape, padded_shape)
    x = tf.pad(x, padding)
    return x

  def call(self, inputs):
    text = self._standardize(inputs)
    words = self._split(text)
    words = tf.ragged.map_flat_values(self._lookup.lookup, words)
    if self._output_sequence_length != None:
      words = self.pad_and_trunc(words)
    return words


def build_text_input(standardize,
                     split,
                     lookup_dict,
                     embedding_dims,
                     output_sequence_length,):
                       
  vocab_size = len(lookup_dict.values()) + 1
  input_layer = tf.keras.Input(shape=(1,), dtype=tf.string)
  lookup_layer = Tokenizer(standardize, split, lookup_dict, output_sequence_length)
  embedding_layer = tf.keras.layers.Embedding(vocab_size,
                                              embedding_dims,
                                              name='embedding')
  reshape = tf.keras.layers.Lambda(lambda x: tf.squeeze(x, axis=1))
  model = tf.keras.models.Sequential([input_layer,
                                      lookup_layer,
                                      embedding_layer,
                                      reshape,
                                      ])
  return model
