def gen(lst,idx = 0):
    yield lst[idx]
    idx += 1

a = [1,2,3,4,5]
gen_a = gen(a)
for i in gen_a:
    print(i)