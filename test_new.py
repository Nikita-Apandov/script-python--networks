# строку ip в список 
ip = "192.168.100.1"
ip.split(".")

# метод чтения файла
f = open("file.txt","r")
for line in f: 
    print(line.rstrip)

# если надо из одного файла перенести значения в другой 
with open('r1.txt') as src, open('result.txt', 'w') as dest:
    for line in src:
        if line.startswith('service'):
            dest.write(line)