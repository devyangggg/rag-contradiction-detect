from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from dotenv import load_dotenv  
import json
import nltk  
from nltk.tokenize import sent_tokenize 

load_dotenv() 

nltk.download('punkt_tab')

def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
gen_kwargs = {
    "max_length": 256,
    "length_penalty": 0,
    "num_beams": 3,
    "num_return_sequences": 1,
}

data = {}

with open("metadata.json","r") as f:
    data = json.load(f)

all_file_data = {}

for d in data:
    entry = data[d]

    file_name = entry["name"]
    text = entry["text"]

    sentences = sent_tokenize(text)
    all_triplets = []


    for sentence in sentences:

        model_inputs = tokenizer(sentence, max_length=256, padding=True, truncation=True, return_tensors='pt')


        generated_tokens = model.generate(
            model_inputs["input_ids"].to(model.device),
            attention_mask=model_inputs["attention_mask"].to(model.device),
            **gen_kwargs,
            output_scores=True,
            return_dict_in_generate=True
        )

        decoded_preds = tokenizer.batch_decode(generated_tokens.sequences, skip_special_tokens=False)


        for pred in decoded_preds:       
            triplets = extract_triplets(pred)
            all_triplets.extend(triplets) 

    all_file_data[file_name] = all_triplets
    


for file in all_file_data:
    triplet_arr = all_file_data[file]

    for triplet in triplet_arr:
        triplet["sentence"] = f"{triplet['head']} {triplet['type']} {triplet['tail']}"

with open("triplets.json", "w") as f:
    json.dump(all_file_data, f, indent=2)



