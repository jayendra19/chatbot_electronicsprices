import spacy

# Load your custom spaCy NER model
custom_ner_model_path = r'C:\Users\jayen\chatbot_electronicsprices\NER'
custom_nlp = spacy.load(custom_ner_model_path)

# Function to extract entities using your custom spaCy NER model
def extract_entities(text):
    doc = custom_nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Example usage
user_input = "asus rog "
entities = extract_entities(user_input)
print(entities[0][0])

print(entities)
