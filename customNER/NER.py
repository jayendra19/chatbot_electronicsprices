from spacy.tokens import DocBin
from tqdm import tqdm
import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example
import random

import json
# https://www.kaggle.com/datasets/finalepoch/medical-ner 
with open('json/ner.json', 'r') as f:
    data = json.load(f)
    #print(data)
    #print(data[0].keys())

# Loading a blank English model
nlp = spacy.blank("en")

# Adding the NER component to the pipeline
ner = nlp.add_pipe("ner")

# Adding custom entity labels to the NER model
ner.add_label("PRODUCT")

TRAIN_DATA = []
for item in data:
    text = item['text']
    entities = [(annotation['start'], annotation['end'], annotation['label']) for annotation in item['annotations']]

    TRAIN_DATA.append((text, {"entities": entities}))

nlp.initialize(lambda: [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in TRAIN_DATA])#It initializes the spaCy NLP model with training data. It creates spaCy Example objects from the training data and uses them to initialize the model. The Example.from_dict method is used to create Example instances from dictionaries containing text and annotations.
 
for epoch in range(100):
    random.shuffle(TRAIN_DATA)#It shuffles the training data to introduce randomness into the training process.
    losses = {}

    for batch in minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001)):#It shuffles the training data to introduce randomness into the training process.
        for text, annotations in batch:
            doc = nlp.make_doc(text)#It tokenizes the input text using the spaCy NLP model to create a Doc object.
            example = Example.from_dict(doc, annotations)#It creates a spaCy Example instance from the tokenized Doc and the annotations.
            nlp.update([example], losses=losses)#It performs an update step on the spaCy NLP model using the current example. This updates the model's parameters based on the provided training example and minimizes the loss

    print(f"Losses at iteration {epoch} - {losses}")


# Save the trained model
nlp.to_disk("NER")








     
    






