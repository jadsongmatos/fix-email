import re

email = 'valid..alias@example.com'

rfc5322 = r"([A-Za-z0-9-!#$%&'*+/=?^_`{|}~]+(?:\.[A-Za-z0-9-!#$%&'*+/=?^_`{|}~]+)*)@((?:[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\.)*[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*?)"


print(re.match(rfc5322, email))

email = "nome@dominio@empresa.com"
parts = email.split("@", 1)  # Divide o e-mail na primeira ocorrência do '@'
if len(parts) == 2:
    # Reconstrói o e-mail com apenas o primeiro '@'
    corrected_email  = parts[0] + "@" + parts[1].replace("@", "")
else:
    corrected_email = email
    
print(corrected_email)