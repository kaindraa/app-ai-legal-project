import re, functools, collections
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import pandas as pd

def basic_tokenize(text):
    return text.lower().split()

def extract_referenced_pasals(text):
    return set(re.findall(r"[Pp]asal\s+(\d+[A-Za-z]?)", text))

chunks_df = pd.read_csv("pasal_chunks.csv")
all_chunks = chunks_df.to_dict(orient="records")

tokenized_corpus = [basic_tokenize(chunk["text"]) for chunk in all_chunks]
bm25 = BM25Okapi(tokenized_corpus)

judul_pasal_map = collections.defaultdict(dict)
for ch in all_chunks:
    judul_pasal_map[ch['judul']][str(ch['pasal'])] = ch

@functools.lru_cache(maxsize=256)
def bm25_scores(query):
    return bm25.get_scores(basic_tokenize(query))

def _recursive_references(nomor_chain, chunk, visited, depth, max_depth, context_chunks):
    if depth > max_depth:
        return
    refs = extract_referenced_pasals(chunk['text'])
    sub_number = 1
    for ref_pasal in refs:
        ref_chunk = judul_pasal_map[chunk['judul']].get(ref_pasal)
        if not ref_chunk:
            continue
        ref_key = (ref_chunk['judul'], ref_chunk['pasal'])
        if ref_key in visited:
            continue
        visited.add(ref_key)

        nomor = f"[{nomor_chain}-{sub_number}]"
        context_chunks.append({
            "nomor": nomor,
            "judul": ref_chunk['judul'],
            "pasal": ref_chunk['pasal'],
            "text": ref_chunk['text'],
            "tipe": f"Referensi dari {chunk['judul']} Pasal {chunk['pasal']}",
        })
        sub_number += 1

        _recursive_references(
            nomor_chain=nomor[1:-1], 
            chunk=ref_chunk,
            visited=visited,
            depth=depth + 1,
            max_depth=max_depth,
            context_chunks=context_chunks
        )


def search_bm25_recursive(query, topk=50, max_depth=3):
    visited = set()
    context_chunks = []
    scores = bm25_scores(query)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:topk]

    for i, idx in enumerate(top_indices):
        root_chunk = all_chunks[idx]
        nomor = f"[{i+1}]"
        root_key = (root_chunk['judul'], root_chunk['pasal'])
        if root_key in visited:
            continue
        visited.add(root_key)

        context_chunks.append({
            "nomor": nomor,
            "judul": root_chunk['judul'],
            "pasal": root_chunk['pasal'],
            "text": root_chunk['text'],
            "tipe": "BM25",
        })

        _recursive_references(
            nomor_chain=nomor[1:-1],  # remove [ ]
            chunk=root_chunk,
            visited=visited,
            depth=1,
            max_depth=max_depth,
            context_chunks=context_chunks
        )

    return context_chunks
