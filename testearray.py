array = [0,1,6,4,8,2,6,6,4,4,4,4]
Ac = [0]*10

a=0

for i in range(len(array)):
    if (array[i]!=0 and array[i] not in Ac):
        Ac[a] = array[i]
        a+=1


Ac.sort()
Ac= list(filter(None, Ac))

print(Ac)


decimal=0
decimais=[None]*19

for i in Ac:
    for l in range(len(array)):
        if array[l] == i:
            decimais[l] = decimal
            decimal += 1
    decimal = (decimal * 2)
    
print
