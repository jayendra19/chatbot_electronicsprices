import streamlit as st
import keras
import pickle
import json
import numpy as np
from src.chatbotmaking.api_calling import get_price
import spacy

# load trained mod
model = keras.models.load_model('artifacts/chat_model')

# load tokenizer object
with open('artifacts/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


# load label encoder object
with open('artifacts/label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

with open("json/json_file.json") as file:
   data = json.load(file)

max_len = 20  # Set the maximum length as needed

# Load your custom spaCy NER model
#custom_ner_model_path = r'C:\Users\jayen\chatbot_electronicsprices\NER'
custom_ner_model_path = '/app/NER'
custom_nlp = spacy.load(custom_ner_model_path)

# Function to extract entities using your custom spaCy NER model
def extract_entities(text):
    doc = custom_nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

    

st.title("Chatbot Streamlit App")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("You: "):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # The user has selected a category, now handle product name
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([user_input]),
                                        truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]

    entities = extract_entities(user_input)#This is condition for any text that is present in entities will be recognize as prduct name.Otherwise its impossible to create this chatbot
    if entities:
            try:
                 # If a product name is detected, send it to the API
                product_name = entities[0][0]

                # Call your API to get product details
                api_response = get_price(product_name)
                fulfillment_text = api_response.json.get('fulfillmentText', 'Error: No fulfillmentText in response')
                st.session_state.messages.append({"role": "assistant", "content": fulfillment_text})
                with st.chat_message("assistant"):
                    st.markdown(fulfillment_text)
            except Exception as e:
                raise e
    else:
            try:
                # Handle other tags as usual
                for intent in data['intents']:
                    if intent['tag'] == tag:
                        response = np.random.choice(intent['responses'])
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        with st.chat_message("assistant"):
                            st.markdown(response)
            except Exception as e:
                raise e
