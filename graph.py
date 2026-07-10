
"""
post semantic structure that im thinking:
{
    head : xyz
    edges : a b c d
    children : qw we er rt 
}

group similar head into one to reduce the redundency
"""
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

data = {}

with open("triplets.json","r") as f:
    data = json.load(f)


