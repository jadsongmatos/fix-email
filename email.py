import re
from tlds import tlds
from distancia_levenshtein import distancia_levenshtein

def corrigir_email(email_input):
    rfc5322 = r"([A-Za-z0-9-!#$%&'*+/=?^_`{|}~]+(?:\.[A-Za-z0-9-!#$%&'*+/=?^_`{|}~]+)*)@((?:[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\.)*[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*?)"
    
    # Remover espaços
    email = re.sub(r'[ :;<>\[\]\\]', '', email_input)

    # Substituir caracteres estranhos conhecidos
    email = email.replace(",", ".")
    
    # Corrigir '@@' e '..'
    email = re.sub(r'@+', '@', email)
    email = re.sub(r'\.+', '.', email)
    
    if email[0] == '.': # Remove o primeiro caractere se for um ponto
        email = email[1:] 
    if email[-1] == '.': # Remove o último caractere se for um ponto
        email = email[:-1]
        
    email_up = email.upper()
    for tld in tlds:
        if email_up.endswith(tld):
            # Calcula a posição inicial da substring
            posicao_tld = len(email_up) - len(tld)
            if email[posicao_tld-2] == '_':
                email = email[:posicao_tld-2] + '.' + email[posicao_tld-1:]
    
        # Corrigir múltiplos '@'
    email = re.sub(r'@+', '@', email)
    
    # Divide o e-mail na primeira ocorrência do '@'
    parts = email_input.split("@")
    if len(parts) > 2:
        for i,e in enumerate(parts):
            novo_email = parts[i-1] + "@" + parts[i].replace("@", "")
            if re.match(rfc5322, novo_email):
                email = novo_email

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
    
    # Validar o formato do e-mail
    if re.match(rfc5322, email):
        return (email, True)
    else:
        return (email, False)


# Exemplo de uso

# validos no RFC 6854
# '"email..email"@dominio.com',
# 'valid..alias@example.com',
# 'val..id@example.com',
# 'valid..2020@example.com',

valid_rfc5322 = [
    "exemplo@dominio.com",  # básico.
    "nome.sobrenome@empresa.com.br",  # com domínio de nível superior duplo.
    "usuario+tag@exemplo.org",  # com tag.
    "1234567890@dominio.com",  # com números.
    "email_com_ponto@dominio.com",  # com ponto antes do @.
    "underscore_in_name@dominio.com",  # com underscore.
    "nome-e-sobrenome@web-email.com",  # com hífen no nome e no domínio.
    "nome*+.%-@dominio.com",  # com caracteres especiais no nome.
    "v@example.com",
    "v@e.com",
    "v@e.me",
    "valid@123.com",
    "valid@example.com",
    "valid+1@example.com",
    "valid+1@ex.ample.com",
    "valid+1@ex-ample.com",
    "valid+1@ex_ample.com",
    "valid+01@example.com",
    "valid+01@ex.ample.com",
    "valid+01@ex-ample.com",
    "valid+01@ex_ample.com",
    "vali.d@example.com",
    "va-lid@example.com",
    "v-a-l-i-d@example.com",
    "v.a-lid@example.com",
    "v.ali-d@example.com",
    "v_ali-d@example.com",
    "va_li-d@example.com",
    "v_a_li_d@example.com",
    "v.ali-d@example.com",
    "v.ali.d@example.com",
    "v0.ali.d@example.com",
    "v0.ali.d1@example.com",
    "valid@e-x_ample.com",
    "valid@e.x-ample.c.om",
    "valid+alias@example.com",
    "valid+1+alias@example.com",
    "valid+alias+user@example.com",
    "valid+xyz+alias@example.com",
    "valid01@example.com",
    "valid-01@example.com",
    "valid_01@example.com",
    "valid.01@example.com",
    "va-lid-0-1@example.com",
    "va.lid-0-1@example.com",
    "val-id.0-1@example.com",
    "0.vali.d@example.com",
    "0.vali.1@example.com",
    "valid++alias@example.com",
    "valid--alias@example.com",
    "valid__alias@example.com",
    "v.-alid@example.com",
    "v-.-alid@example.com",
    "vali-.-d@example.com",
    "va--lid@example.com",
    "val_-id@example.com",
    "val-.id@example.com",
    "valid__2020@example.com",
    "valid+-2020@example.com",
]

corrigir = [
    "usuario@@gmail.com",  # com dois @
    " usuario@hotmail.com ",  # com espaços no começo e no final
    "usuario@gmail.a",  # TLD parecido
    "usuario@dominio..com",  # Ponto duplo após o domínio.
    ".usuario@dominio.com",  # Ponto no início do nome.
    "usuario@dominio.com.",  # Ponto no final do domínio.
    "usuario@dom inio.com",  # Espaço no domínio.
    "nome@dominio,com",  # Vírgula em vez de ponto.
    "usuario@dominio_com",  # Uso de underscore no domínio.
    "nome@dominio@empresa.com"  # Múltiplos caracteres @.
]

erro = [
    "@dominio.com",  # Falta o nome do usuário.
    "userfdomin@",  # Falta o domínio.
    "usuario@.com",  # Falta o nome do domínio, apenas TLD presente.
    "usuário@domínio.com",  # Caracteres não ASCII.
    "usuario..2020@dominio.com"  # Ponto duplo no nome.
    "usuario@dominio",  # Falta o TLD (Top-Level Domain) após o domínio.
]


for email in valid_rfc5322:
    email_corrigido, v_email = corrigir_email(email)
    comp_email = email == email_corrigido
    print(f"{comp_email}|{v_email}|{email}|{email_corrigido}|")
    if comp_email == False and v_email == True:
        print(f"\nTeste de {email} não passou\n")
        break

print("\n")

for email in corrigir:
    email_corrigido, v_email = corrigir_email(email)
    comp_email = email == email_corrigido
    print(f"{comp_email}|{v_email}|{email}|{email_corrigido}|")


print("\n")

for email in erro:
    email_corrigido, v_email = corrigir_email(email)
    comp_email = email == email_corrigido
    print(f"{comp_email}|{v_email}|{email}|{email_corrigido}|")
