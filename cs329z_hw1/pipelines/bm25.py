from collections import Counter
from cs329z_hw1.tokenizer import tokenize
import math


def build_index(docs: list[str]) -> dict:
    postings = {}
    doc_len = []
    for doc_id, text in enumerate(docs):
        # 分词，把这篇长度为 len(tokens) 的文档的长度记下来
        tokens = tokenize(text)
        doc_len.append(len(tokens))
        # 数出这篇文档里每个词各出现几次
        counter = Counter(tokens)
        # 对每个 (词, 次数)，把 (doc_id, 次数) 追加到 postings[词] 的 list 末尾
        for term, count in counter.items():
            if term not in postings:
                postings[term] = []
            postings[term].append((doc_id, count))
        
    # 算出 N 和 avgdl
    N = len(docs)
    avgdl = sum(doc_len) / N if N > 0 else 0
    return {"postings": postings, "doc_len": doc_len, "N": N, "avgdl": avgdl}

def search(index: dict, query: str, k: int, k1=1.5, b=0.75) -> list:
    postings = index["postings"]
    doc_len = index["doc_len"]
    N = index["N"]
    avgdl = index["avgdl"]
    scores = {}
    # 查询分词
    query_tokens = tokenize(query)
    #去重
    query_tokens = set(query_tokens)
    # 计算 BM25 分数，
    for term in query_tokens:
        if term not in postings:
            continue
        # 计算 df 和 idf
        df = len(postings[term])
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        # 对每个 (doc_id, tf) 计算 BM25 分数
        for doc_id, tf in postings[term]:
            score = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len[doc_id] / avgdl))
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += score
    # 按分数排序，返回前 k 个 doc_id和分数
    ranked_docs = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return [(doc_id, score) for doc_id, score in ranked_docs[:k]]


