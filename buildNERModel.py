from __future__ import unicode_literals, print_function

import os

import plac
import random
from pathlib import Path
import spacy
import json
from tqdm import tqdm

RAW_DATA = open('TrainingData/annotations.json')
data = json.load(RAW_DATA)
TRAIN_DATA = data['annotations']
print(TRAIN_DATA)


model = None
output_dir=Path(os.getcwd()+"\\NERModelOut\\")
print(output_dir)
n_iter=100


#load the model

if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')
    print("Created blank 'en' model")

#set up the pipeline

if 'ner' not in nlp.pipe_names:
    ner = nlp.add_pipe('ner', last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(TRAIN_DATA):
            print(annotations['entities'])
            nlp.update(
                [text],
                [annotations['entities']],
                drop=0.2,
                sgd=optimizer,
                losses=losses)
        print(losses)

if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)