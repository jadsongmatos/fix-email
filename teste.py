import re

email = '"email..email"@dominio.com'

regex = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
regex = r"^(([A-Za-z0-9]+((.|-|_|+)?[A-Za-z0-9]?)[A-Za-z0-9]+)|[A-Za-z0-9]+)@(([A-Za-z0-9]+)+((.|-)?([A-Za-z0-9]+)+))+.([A-Za-z]{2,})+$"


print(re.match(regex, email))