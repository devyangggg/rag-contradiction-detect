
"""
post semantic structure that im thinking:
{
    "cloudsync_docs.pdf": [
        {"id": 0, "sentence": "...", "vector": [...]},
        {"id": 1, "sentence": "...", "vector": [...]},
    ],
    "vaultkeep_docs.pdf": [
        {"id": 0, "sentence": "...", "vector": [...]},
    ],
}

group similar head into one to reduce the redundency
"""
import json
import lancedb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv  

load_dotenv() 

model = SentenceTransformer("all-MiniLM-L6-v2")

json_data = {}

with open("triplets.json","r") as f:
    json_data = json.load(f)


file_arr = []
db = lancedb.connect("./my_db")

embedding_cache = {}

for d in json_data:
    triplets = json_data[d]

    for i, f in enumerate(triplets):
        sentence = f["sentence"]
        embedding = model.encode(sentence).tolist()

        if sentence not in embedding_cache:
            embedding_cache[sentence] = model.encode(sentence).tolist()
        
        embedding = embedding_cache[sentence]

        triplet_data = {
            "id" : i,
            "file_name" : d,
            "sentence" : sentence,
            "vector" : embedding
        }
        file_arr.append(triplet_data)



table = db.create_table("my_vectors", file_arr)






    







        
        


