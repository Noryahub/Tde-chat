import sys
import os

# ajouter le dossier racine au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nlu.ner import extract_entities

text = "Il y a une fuite à Agoè"

entities = extract_entities(text)
from nlu.ner import model
print(entities)
print(extract_entities("fuite à Agoè"))
print(extract_entities("coupure d'eau à Lomé"))
print(extract_entities("eau sale dans le quartier Adidogomé"))
print(model.config.id2label)