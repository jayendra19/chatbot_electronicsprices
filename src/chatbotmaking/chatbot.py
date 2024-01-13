import spacy
import random
import keras
import pickle
import numpy as np
from colorama import Fore, Style
import json 
from flask import Flask, request, jsonify
import numpy as np
from tensorflow import keras
import colorama 
colorama.init()
from colorama import Fore, Style, Back
import pickle
from src.chatbotmaking.api_calling import get_price

with open("json/json_file.json") as file:
   data = json.load(file)




def chat(user_input):
    # load trained model
    model = keras.models.load_model('artifacts/chat_model')

    # load tokenizer object
    with open('artifacts/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('artifacts/label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20



    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        user_input = input()

        if user_input.lower() == "quit":
            break

        if user_input.lower() in ["mobile", "laptop","mobiles", "laptops","tablets","tablet"]:
            # The user has selected a category, now handle product name
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, "Cool! Can you please tell me the product name you're interested in?")
            product_name = input()

            # Call your API to get product details
            api_response = get_price(product_name)
            #print(api_response)
            fulfillment_text = api_response.json.get('fulfillmentText', 'Error: No fulfillmentText in response')
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, fulfillment_text)

        else:
            # The user input doesn't match any predefined category, handle it accordingly
            result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([user_input]),
                                                truncating='post', maxlen=max_len))
            tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]

            found_response = False
            for intent in data['intents']:
                if intent['tag'] == tag:
                    found_response = True
                    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, np.random.choice(intent['responses']))

            if not found_response:
                print(Fore.YELLOW + "ChatBot:" + Style.RESET_ALL, "I'm sorry, I didn't understand that. Can you please rephrase?")

#print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)

