with open("moby.txt", "r") as file:
    with open("moby_clean.txt", "w") as new_file:
        for line in file:
            line = ''.join(c for c in line if c not in ".,!?;-")
            for word in line.split(' '):
                new_file.write(word + '\n')
