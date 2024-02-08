def distancia_levenshtein(s1, s2):
    if len(s1) < len(s2):
        return distancia_levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    matriz = range(len(s2) + 1)
    for i1, c1 in enumerate(s1):
        nova_matriz = [i1 + 1]
        for i2, c2 in enumerate(s2):
            if c1 == c2:
                nova_matriz.append(matriz[i2])
            else:
                nova_matriz.append(1 + min((matriz[i2], matriz[i2 + 1], nova_matriz[-1])))
        matriz = nova_matriz

    return matriz[-1]