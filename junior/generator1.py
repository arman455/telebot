import time

start = time.time()
spisok_cifr = []
for i in range(100000000):
    spisok_cifr.append(i*2)
end = time.time()

print(end - start)

start = time.time()
generator_cifr = [print(i) for i in range(10)]
end = time.time()

print(end - start)
