email = 'test-@example.com'

local_part = email.find('@')
if email[local_part-1]
print(local_part,email[local_part-1])