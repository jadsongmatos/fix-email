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

    email_tld = email.split('.')
    
    if len(email_tld) > 1:
        tld = email_tld[-1].upper()
        if tld not in tlds:
            # Calcular a distância de Levenshtein entre o TLD incorreto e todos os TLDs válidos
            distancias = {tld_valido: distancia_levenshtein(
                tld, tld_valido) for tld_valido in tlds}

            # Encontrar o TLD com a menor distância
            tld_correto = min(distancias, key=distancias.get)

            # Substituir o TLD incorreto pelo correto
            email = email.rsplit('.', 1)[0] + '.' + tld_correto.lower()
            
    else:
        return (email, False)
    
    

    #regex = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    regex = r"\".+\"@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"

    # Validar o formato do e-mail
    if re.match(regex, email):
        return (email, True)
    else:
        return (email, False)


# Exemplo de uso
valid = [
    # Válidos
    "exemplo@dominio.com",  # básico.
    "nome.sobrenome@empresa.com.br",  # com domínio de nível superior duplo.
    "usuario+tag@exemplo.org",  # com tag.
    "1234567890@dominio.com",  # com números.
    "email_com_ponto@dominio.com",  # com ponto antes do @.
    "underscore_in_name@dominio.com",  # com underscore.
    "nome-e-sobrenome@web-email.com",  # com hífen no nome e no domínio.
    '"email..email"@dominio.com',# com aspas e ponto seguido dentro do local part (válido segundo RFC 5322).
    "nome*+.%-@dominio.com"  # com caracteres especiais no nome.
]

corrigir = [
    "usuario@@gmail.com",  # com dois @
    " usuario@hotmail.com ",  # com espaços no começo e no final
    "usuario@gmail.a",  # TLD parecido
    "usuario@dominio",  # Falta o TLD (Top-Level Domain) após o domínio.
    "usuario@dominio..com",  # Ponto duplo após o domínio.
    ".usuario@dominio.com",  # Ponto no início do nome.
    "usuario@dominio.com.",  # Ponto no final do domínio.
    "usuario@dom inio.com",  # Espaço no domínio.
    "nome@dominio,com",  # Vírgula em vez de ponto.
    "usuario@dominio_com",  # Uso de underscore no domínio.
    "usuario@yaho.a",  # TLD parecido
]

erro = [
    "@dominio.com",  # Falta o nome do usuário.
    "userfdomin@",  # Falta o domínio.
    "usuario@.com",  # Falta o nome do domínio, apenas TLD presente.
    "usuário@domínio.com",  # Caracteres não ASCII.
    "usuario..2020@dominio.com",  # Ponto duplo no nome.
    "nome@dominio@empresa.com"  # Múltiplos caracteres @.
]

for email in valid:
    email_corrigido, v_email = corrigir_email(email)
    comp_email = email == email_corrigido
    print(f"{comp_email}|{v_email}|{email}|{email_corrigido}|")
    if comp_email == False and v_email == True:
        print(f"\nTeste de {email} não passou\n")
        break

print("\n")

for email in erro:
    email_corrigido, v_email = corrigir_email(email)
    comp_email = email == email_corrigido
    print(f"{comp_email}|{v_email}|{email}|{email_corrigido}|")
