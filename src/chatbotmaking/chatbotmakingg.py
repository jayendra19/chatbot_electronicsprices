#   IF U USE THIS CODE IT WILL NOT RECOGNISE IT WILL ONLY RECOGNISE PRODUCT THAT ARE PRESENT IN THE PATTERN THATS NOT MY GOAL GOAL AFTER CATEGORY 
#SLECTION USER CAN PUT ANY PRODUCT NAME THAT HE WANTS.
import json 
import numpy as np
from tensorflow import keras
import colorama 
colorama.init()
from colorama import Fore, Style, Back
import pickle
import spacy
from src.chatbotmaking.api_calling import get_price
import logging


with open("json/json_file.json") as file:
   data = json.load(file)
logging.info("imported json file for chatbot")

def chat():

    # load trained model
    model = keras.models.load_model('artifacts/chat_model')
    logging.info("loaded chat model for chat")

    # load tokenizer object
    with open('artifacts/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    logging.info("tokkenizer loaded for tokkenze text")

    # load label encoder object
    with open('artifacts/label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
    logging.info("lablel loaded successfully")

    # parameters
    max_len = 20

    # Load your custom spaCy NER model
    custom_ner_model_path = r'C:\Users\jayen\chatbot_electronicsprices\NER'
    custom_nlp = spacy.load(custom_ner_model_path)
    logging.info("loaded custom NER model ")

    # Function to extract entities using your custom spaCy NER model
    def extract_entities(text):
        doc = custom_nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    logging.info("Returning entities successfully")

    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = input()

        if inp.lower() == "quit":
            break

        # The user has selected a category, now handle product name
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                            truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]
        #print(tag)

        entities = extract_entities(inp)#This is condition for any text that is present in entities will be recognize as prduct name.Otherwise its impossible to create this chatbot
        if entities:
            # If a product name is detected, send it to the API
            product_name = entities[0][0]  # Get the first entity's text
            api_response = get_price(product_name)
            fulfillment_text = api_response.json.get('fulfillmentText', 'Error: No fulfillmentText in response')
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, fulfillment_text)          
        else:
            # Handle other tags as usual
            for i in data['intents']:
                if i['tag'] == tag:
                    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, np.random.choice(i['responses']))


#search chatbot who learns from its user'''


if __name__ == '__main__': 
    chat()

        






