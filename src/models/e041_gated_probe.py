"""E054 measurement: flatten only final gated UNHCR predictions."""
import numpy as np
from src.models import supervised_retrieval as retrieval


def apply_probe(vectors, frame, schema):
    if 's3_11_intent_return_12m_lbl' not in schema['items']:
        return vectors
    names = [n for n, r in schema['items'].items() if r['class'] == 'PREDICT']
    blank = frame[names].isna().to_numpy()
    if int(blank.sum()) != len(vectors):
        raise ValueError('Canonical prediction count differs')
    gated = np.array([schema['items'][n].get('gate') is not None for n in names])
    result = list(vectors)
    index = 0
    for row in blank:
        for target, is_gated in zip(row, gated):
            if target:
                if is_gated:
                    result[index] = np.full(len(vectors[index]), 1.0 / len(vectors[index]))
                index += 1
    return result


def predict(frame, schema):
    return apply_probe(retrieval.predict(frame, schema), frame, schema)
