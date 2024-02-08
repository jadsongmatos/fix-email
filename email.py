import re
from tlds import tlds
from distancia_levenshtein import distancia_levenshtein

def corrigir_email(email_input):
    # Remover espaços
    email = re.sub(r'[ :;<>\[\]\\]', '', email_input)

    # Substituir caracteres estranhos conhecidos
    email = email.replace(",", ".")
    
    # Corrigir múltiplos '@'
    email = re.sub(r'@+', '@', email)
    
    # Validar o formato do e-mail
    if not re.match(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", email):
        return email
    
    tld = email.split('.')[-1].upper()

    if tld in tlds:
        return email

    # Calcular a distância de Levenshtein entre o TLD incorreto e todos os TLDs válidos
    distancias = {tld_valido: distancia_levenshtein(tld, tld_valido) for tld_valido in tlds}

    # Encontrar o TLD com a menor distância
    tld_correto = min(distancias, key=distancias.get)

    # Substituir o TLD incorreto pelo correto
    email_corrigido = email.rsplit('.', 1)[0] + '.' + tld_correto.lower()
    return email_corrigido

# Exemplo de uso
emails = [
    "usuario@@gmail.com",
    " usuario@hotmail.com ",
    "usuario@yaho.a"
]

for email in emails:
    email_corrigido = corrigir_email(email)
    print(f"|{email}|{email_corrigido}|")
    