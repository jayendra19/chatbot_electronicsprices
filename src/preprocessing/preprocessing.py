import json 
import os
import nltk
import logging
import numpy as np 
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from keras.layers import LSTM


file_path = 'json/json_file.json'
with open(file_path) as file:
    data = json.load(file)
logging.info("imported json data to preprocess")


training_sentences = []
training_labels = []
labels = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])
logging.info("Created seperated file for my training sentences and training labels and lable and response")
        
num_classes = len(labels)

lbl_encoder = LabelEncoder()
lbl_encoder.fit(training_labels)
training_labels = lbl_encoder.transform(training_labels)
logging.info("Converted lables into numbers of training labels")



##my unique words in senetenses
vocab_size = 1000
#25 will be my features
embedding_dim = 25
#this for padding max to max 21 words user can put 
max_len = 20

oov_token = "<OOV>"
#training_sentences=str(training_sentences).lower().strip()
tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)

'''#USING WORD2VEC
nltk.download('punkt')
tokenizer=nltk.word_tokenize(str(training_sentences).lower())
model = Word2Vec(sentences=training_sentences, vector_size=25, window=2, min_count=1, workers=8,epochs=20)'''

#training_sentences= [lemmatizer.lemmatize(word) for word in training_sentences if word not in stop_words]
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)
#print(padded_sequences)
logging.info("Done Creating Embedding layer")

logging.info("Statrted creating model")
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
#model.add(GlobalAveragePooling1D())
model.add(LSTM(128))  
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', 
              optimizer='adam', metrics=['accuracy'])
logging.info("Compiled the model")

model.summary()
epochs =150
logging.info("Started training the model")
model.fit(padded_sequences, np.array(training_labels), epochs=epochs)

artifacts_folder = "artifacts"
os.makedirs(artifacts_folder, exist_ok=True)
# Save the trained model to the "artifacts" folder
model_filename = os.path.join(artifacts_folder, 'chat_model')
model.save(model_filename)
logging.info('Model saved to ' + model_filename)

# Save the tokenizer object to the "artifacts" folder
tokenizer_filename = os.path.join(artifacts_folder, 'tokenizer.pickle')
with open(tokenizer_filename, 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Tokenizer saved to {tokenizer_filename}")
logging.info("Tokenizer saved to {tokenizer_filename}")
    
#saving the fitted label encoder
# Save the label encoder object to the "artifacts" folder
lbl_encoder_filename = os.path.join(artifacts_folder, 'label_encoder.pickle')
with open(lbl_encoder_filename, 'wb') as enc:
    pickle.dump(lbl_encoder, enc, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Label Encoder saved to {lbl_encoder_filename}")
logging.info("label saved to {lbl_encoder_filename}")





