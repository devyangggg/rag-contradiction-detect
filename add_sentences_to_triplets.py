import json
data = {}

with open("triplets.json", "r") as f:
    data = json.load(f)

for file in data:
    triplet_arr = data[file]

    for triplet in triplet_arr:
        sentence = f"{triplet["head"]} {triplet["type"]} {triplet["tail"]}"
        triplet["sentence"] = sentence

with open("triplets_w_sentence.json", "w") as f:
    json.dump(data, f, indent=2)
