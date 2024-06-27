import random

popa = [100]
list_ver = []

for i in popa:
    a = i
    while i != 0:
        list_ver.append(a)
        i -= 1

print(len(list_ver))
print(random.choice(list_ver))
print(int('-3'))