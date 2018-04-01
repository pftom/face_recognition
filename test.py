from os import walk

f = []

for (dirpath, dirnames, filenames) in walk('./known_people/'):
    f.extend(filenames)
    break

print(f)