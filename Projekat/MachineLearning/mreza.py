from unicodedata import category
import numpy as np
import sklearn
import tensorflow as tf
import pandas as pd
from keras.models import load_model


def determine_variable_types(data, label):
    nunique = data.nunique()
    count=len(data)
    dtypes = data.dtypes
    categorical = []
    numerical = []
    dnu = dict(nunique)
    dnu.pop(label[0], None)
    for key in dnu:
        if nunique[key] <= 20 and count>50:
            categorical.append(key)
        elif (dtypes[key] != object):
            numerical.append(key)
    
    return (categorical, numerical)

#vraca dataframe za datu putanju
def load_data(path):
  df_comma = pd.read_csv(path, nrows=1,sep=",")
  df_semi = pd.read_csv(path, nrows=1, sep=";")
  if df_comma.shape[1]>df_semi.shape[1]:
      print("comma delimited")
      return pd.read_csv(path,sep=',')
  else:
      print("semicolon delimited")
      return pd.read_csv(path,sep=';')
  
def split_data(data,train_percentage=0.8,test_percentage=0.1,val_percentage=0.1):
  #podela 80/10/10
  train,val,test=np.split(data.sample(frac=1),[int(train_percentage*len(data)),int((val_percentage+train_percentage)*len(data))])
  print(len(data), 'training examples')
  print(data)
  print(len(train), 'training examples')
  print(len(val), 'validation examples')
  print(len(test), 'test examples')
  return train,val,test


def df_to_dataset(dataframe,target, shuffle=True, batch_size=256):
  df = dataframe.copy()
  labels = df.pop(target)
  df = {key: value[:,tf.newaxis] for key, value in df.items()}
  ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  ds = ds.prefetch(batch_size)
  print(ds)
  return ds

def get_normalization_layer(name, dataset):
  # Create a Normalization layer for the feature.
  normalizer = tf.keras.layers.Normalization(axis=None)

  # Prepare a Dataset that only yields the feature.
  feature_ds = dataset.map(lambda x, y: x[name])

  # Learn the statistics of the data.
  normalizer.adapt(feature_ds)

  return normalizer

def get_category_encoding_layer(name, dataset, dtype, max_tokens=None):
  # Create a layer that turns strings into integer indices.
  if dtype == 'string':
    index = tf.keras.layers.StringLookup(max_tokens=max_tokens)
  # Otherwise, create a layer that turns integer values into integer indices.
  else:
    index = tf.keras.layers.IntegerLookup(max_tokens=max_tokens)

  # Prepare a `tf.data.Dataset` that only yields the feature.
  feature_ds = dataset.map(lambda x, y: x[name])

  # Learn the set of possible values and assign them a fixed integer index.
  index.adapt(feature_ds)

  # Encode the integer indices.
  encoder = tf.keras.layers.CategoryEncoding(num_tokens=index.vocabulary_size())

  # Apply multi-hot encoding to the indices. The lambda function captures the
  # layer, so you can use them, or include them in the Keras Functional model later.
  return lambda feature: encoder(index(feature))

def prepare_preprocess_layers(data,target,train):
  categorical_column_names,numerical_column_names=determine_variable_types(data,target)
  print("kategojskie")
  print(categorical_column_names)
  print("numericke")
  print(numerical_column_names)

  if(target in categorical_column_names):
    categorical_column_names.remove(target)
  else:
    numerical_column_names.remove(target)

  print(len(train))
  train_ds=df_to_dataset(train,target,batch_size=256)
  [(train_features, label_batch)] = train_ds.take(1)
  # depth_col=train_features["depth"]
  # layer=get_normalization_layer('depth',train_ds)
  # print(layer(depth_col))

  all_inputs = []
  encoded_features = []
  all_num_inputs=[]

  # Numerical features.
  for header in numerical_column_names:
      print("zapoceta normalizacija "+header)
      numeric_col = tf.keras.Input(shape=(1,), name=header)
      all_inputs.append(numeric_col)
      all_num_inputs.append(numeric_col)
      print("normalizovana "+header)

  for header in categorical_column_names:
      print("zapoceto enkodiranje "+header)
      if(data.dtypes[header]!=object):
          tip="int64"
      else:
          tip="string"
      categorical_col = tf.keras.Input(shape=(1,), name=header, dtype=tip)
      encoding_layer = get_category_encoding_layer(name=header,
                                                  dataset=train_ds,
                                                  dtype=tip)
      encoded_categorical_col = encoding_layer(categorical_col)
      all_inputs.append(categorical_col)
      encoded_features.append(encoded_categorical_col)
      print("zavrseno enkodiranje "+header)

  encoded_features=encoded_features+all_num_inputs
  return all_inputs,encoded_features

def make_model(all_inputs,encoded_features,num_of_layers=3,num_of_nodes=[10,10,10],activation_functions=["relu","relu","relu"],loss="mae",metric="mape"):
  all_features = tf.keras.layers.concatenate(encoded_features)
  x=tf.keras.layers.Normalization(axis=-1)(all_features)
  for i in range(num_of_layers):
    x=tf.keras.layers.Dense(num_of_nodes[i],activation=activation_functions[i])(x)
  output = tf.keras.layers.Dense(1)(x)

  model = tf.keras.Model(all_inputs, output)

  model.compile(optimizer='Adam',
                loss=loss,
                metrics=metric)
  return model


def train_model(model,train_data,validation_data,target,epochs=20):
  model.fit(df_to_dataset(train_data,target,shuffle=False), epochs=20, validation_data=df_to_dataset(validation_data,target,shuffle=False))

def test_model(model,test_data,target):
  return model.evaluate(df_to_dataset(test_data,target,shuffle=False))

data=load_data("diamonds.csv")
target="price"

train,val,test=split_data(data,0.8,0.1,0.1)

all_inputs,encoded_features=prepare_preprocess_layers(data,target,train)
model=make_model(all_inputs,encoded_features)
train_model(model,train,val,target)
test_model(model,test,target)