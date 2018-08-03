from keras.models import model_from_yaml #to load model
from keras.preprocessing.text import Tokenizer #Prepare text data
from keras.preprocessing.sequence import pad_sequences #Prepare text data
import pandas as pd #to load data
import numpy as np


#Constant Variables
MODEL_YAML_ADDRESS   = 'model/model.yaml'
MODEL_WEIGHT_ADDRESS = 'model/model.h5'
MAX_FEATURES = 20000 # how many unique words to use (i.e num rows in embedding vector)
MAXLEN = 100 # max number of words in a comment to use
LOSS = 'binary_crossentropy'
OPTIMIZER = 'adam'
METRICS = 'accuracy'


#Load data for fit
train = pd.read_csv('train.csv')


#Load model from given .yaml and weight file addresses
#this function returns loaded model
def load_trained_model(yaml_add, weight_add, loss_, optimizer_, metrics_):
	yaml_file = open(yaml_add, 'r')
	loaded_model_yaml = yaml_file.read()
	yaml_file.close()
	loaded_model = model_from_yaml(loaded_model_yaml)
	loaded_model.load_weights(weight_add)
	loaded_model.compile(loss=loss_, optimizer=optimizer_, metrics=[metrics_])
	return loaded_model



#This function prepares data 
#for prediction
def data_for_pred(list_sentences):
	list_sentences_train = train['comment_text'].fillna("_na_").values
	#define tokenizer
	tokenizer = Tokenizer(num_words=MAX_FEATURES)
	#fit tokenizer
	tokenizer.fit_on_texts(list(list_sentences_train))
	#text to sequences
	list_tokenized = tokenizer.texts_to_sequences(list_sentences)
	list_pad = pad_sequences(list_tokenized, maxlen=MAXLEN)
	return list_pad


#This function returns prediction list
def get_prediction(data):
	#Load trained model from folder
	model = load_trained_model(MODEL_YAML_ADDRESS, 
							MODEL_WEIGHT_ADDRESS, 
							LOSS, OPTIMIZER, METRICS)
	#Prepare data for prediction
	prepared_data = data_for_pred(data)
	#Predict 
	predictions = model.predict([prepared_data],  batch_size=1024, verbose=1)
	#Return predictions
	prediction_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
	prediction_df = pd.DataFrame(np.array(predictions), columns=[prediction_cols])
	return prediction_df