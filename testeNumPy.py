import numpy as np

A = np.array([[1,2,3,4], [4,3,2,1]])

B = np.delete(A, [0,0], axis=1) #elimina o objeto na posição [0,0] dos dois arrays

print(A)
print(B)

C = np.array(["ola", "adeus", "ate amanha"], dtype=object)
print(C)
D=np.append(C, "tudo bem")
print(D)

D = np.array([1,5,8,2,7,2,9,1,1])
print(np.argmax(D))