from rapidfuzz import fuzz

def item_relevante(busca, titulo, score_minimo=55):
    busca = busca.lower().strip()
    titulo = titulo.lower().strip()

    score = fuzz.token_set_ratio(busca, titulo)

    return score >= score_minimo