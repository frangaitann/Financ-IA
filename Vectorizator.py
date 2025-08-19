from imports import *
import imports

model = SentenceTransformer('all-MiniLM-L6-v2')


json_lines = []
with open("movs.jsonl", "r", encoding="utf-8") as f:
    for i in f:
        json_lines.append(json.loads(i.strip()))
        

texts=[f"{x['Fecha']} {x['Persona']} {x['Monto']} {x['Movimiento']} {x['Horario']}" for x in json_lines]
vectors = model.encode(texts, convert_to_numpy=True)


vec_dimension = vectors.shape[1]
index = faiss.IndexFlatL2(vec_dimension)
index.add(vectors)

faiss.write_index(index, "movs.index")

with open("index_txt.json", "w", encoding="utf-8") as f:
    json.dump(texts, f, ensure_ascii=False)
    
index_read = faiss.read_index("movs.index")

with open("index_txt.json", "r", encoding="utf-8") as f:
    texts= json.load(f)
    
prompt = "abc"
prompt_vector = model.encode([prompt])

D, I = index_read.search(prompt_vector, k=12)

for idx in I[0]:
    print(texts[idx])