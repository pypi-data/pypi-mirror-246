"""
# Euclidean
"""

def gcd(a, b):
    if a == 0:
        return b

    return gcd(b % a, a)

gcd(20,8)

"""# Extended Euclidean"""

def gcdExtended(a, b):

    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = gcdExtended(b % a, a)

    x = y1 - (b//a) * x1
    y = x1

    return gcd, x, y

a, b = 35, 15
g, x, y = gcdExtended(a, b)
print("gcd(", a, ",", b, ") = ", g)

"""# Vernam Cipher"""

def encrypt(pt,key):
  if(len(pt)!=len(key)):
    k=key
    c=0
    while(len(k)!=len(pt)):
      k=k+key[c]
      if(c==len(key)-1):
        c=0
      else:
        c=c+1
  key=k
  ct=""
  for i in range(len(pt)):
    ct=ct+chr(ord(pt[i])^ord(key[i]))
  return ct

def decrypt(ct,key):
  if(len(ct)!=len(key)):
    k=key
    c=0
    while(len(k)!=len(ct)):
      k=k+key[c]
      if(c==len(key)-1):
        c=0
      else:
        c=c+1
  key=k
  pt=""
  for i in range(len(ct)):
    pt=pt+chr(ord(ct[i])^ord(key[i]))
  return pt

ct=encrypt("HELLO","OC")
decrypt(ct,"OC")

"""# Caeser Cipher"""

def encrypt(pt,key):
  ct=""
  for i in pt:
    if(i.isupper()):
      ct=ct+chr((ord(i)+key-65)%26+65)
    else:
      ct=ct+chr((ord(i)+key-97)%26+97)
  return ct

def decrypt(ct,key):
  pt=""
  for i in ct:
    if(i.isupper()):
      pt=pt+chr((ord(i)-key-65)%26+65)
    else:
      pt=pt+chr((ord(i)-key-97)%26+97)
  return pt

ct=encrypt("ATTACKATONCE",4)
decrypt(ct,4)

ct

"""# Caeser Cipher Decrypt with Brute Force"""

def decrypt(ct,key):
  pt=""
  for i in ct:
    if(i.isupper()):
      pt=pt+chr((ord(i)-key-65)%26+65)
    else:
      pt=pt+chr((ord(i)-key-97)%26+97)
  return pt

def bruteforce(ct):
  for i in range(1,27):
    print(f"Key {i} : {decrypt(ct,i)}")

bruteforce("EXXEGOEXSRGI")

"""# Rail Fence"""

import pandas as pd
def encrypt(pt,key):
  cols=[]
  for i in range(len(pt)):
    cols.append(i)
  df=pd.DataFrame(columns=cols)
  for col in cols:
    df[col]=["" for i in range(key)]
  col=0
  row=0
  bottom=0
  for i in pt:
    if(row==0 and col!=0):
      row=row+1
      bottom=0
    if(row<key and bottom==0):
      df[col][row]=i
      row=row+1
    elif(row==key):
      bottom=1
      row=row-2
      df[col][row]=i
    else:
      row=row-1
      df[col][row]=i
    col=col+1
  ct=""
  for i in range(key):
    for j in cols:
      ct=ct+df[j][i]
  ct=ct.replace(" ","")
  return df,ct

df,ct=encrypt("RailFence1",4)

df

ct

"""# Columnar Transposition"""

import pandas as pd
import math
def encrypt(pt,key):
  cols=[]
  for i in key:
    cols.append(i)

  df=pd.DataFrame(columns=cols)

  rows=int(math.ceil(len(pt)/len(key)))

  for col in cols:
    df[col]=["" for i in range(rows)]

  ptr=0
  pt=pt.replace(" ","_")

  for row in range(rows):
    for col in cols:
      try:
        df[col][row]=pt[ptr]
        ptr=ptr+1
      except:
        df[col][row]="_"

  l1=cols

  l1.sort()

  ct=""

  for col in l1:
    for row in range(rows):
      ct=ct+df[col][row]

  return ct

def decrypt(ct,key):
  cols=[]
  for col in key:
    cols.append(col)
  df=pd.DataFrame(columns=cols)
  rows=int(len(ct)/len(cols))
  for col in cols:
    df[col]=["" for i in range(rows)]
  l1=cols
  l1.sort()
  rang=0
  for col in l1:
    prev_range=rang
    rang=rang+rows
    l2=[]
    roi=ct[prev_range:rang]
    for i in roi:
      l2.append(i)
    df[col]=l2
  pt=""
  cols=[]
  for col in key:
    cols.append(col)
  for row in range(rows):
    for col in cols:
      pt=pt+df[col][row]
  pt=pt.replace("_"," ")
  return pt

encrypt("Atharv","HACK")

decrypt("tvh_Ara_","HACK")

"""# Row Transposition"""

import pandas as pd
def encrypt(pt,key):
  rows=[]
  for i in key:
    rows.append(i)

  cols=math.ceil(len(pt)/len(key))

  columns=[]
  for i in range(cols+1):
    columns.append(i)

  df=pd.DataFrame(columns=columns)
  df[0]=rows

  pt=pt.replace(" ","_")

  ctr=0
  for col in columns[1:]:
    for row in range(len(rows)):
      try:
        df[col][row]=pt[ctr]
        ctr=ctr+1
      except:
        df[col][row]="_"

  l1=rows
  l1.sort()
  ct=""
  for row in l1:
    prow=np.where(df[0]==row)
    place_row=prow[0][0]
    for col in columns[1:]:
      ct=ct+df[col][place_row]

  ct=ct.replace("_"," ")
  return ct,df

ct,df=encrypt("Atharv","HACK")

ct

df

"""# Product Cipher"""

import pandas as pd
import math

def caeser_encrypt(pt,key):
  ct=""
  for i in pt:
    if(i.isupper()):
      ct=ct+chr((ord(i)+key-65)%26+65)
    else:
      ct=ct+chr((ord(i)+key-97)%26+97)
  return ct

def columnar_encrypt(pt,key):
  cols=[]
  for i in key:
    cols.append(i)
  df=pd.DataFrame(columns=cols)
  rows=int(math.ceil(len(pt)/len(key)))
  for col in cols:
    df[col]=["" for i in range(rows)]
  ptr=0
  pt=pt.replace(" ","_")
  for row in range(rows):
    for col in cols:
      try:
        df[col][row]=pt[ptr]
        ptr=ptr+1
      except:
        df[col][row]="_"
  l1=cols
  l1.sort()
  ct=""
  for col in l1:
    for row in range(rows):
      ct=ct+df[col][row]
  return ct

def product_encrypt(pt,key1,key2):
    ct1=caeser_encrypt(pt,key1)
    ct2=columnar_encrypt(ct1,key2)
    return ct2


product_encrypt("AttackOnDJ",3,"HACK")

"""# PlayFair Cipher"""

import pandas as pd
import numpy as np

def encrypt(pt,key):

  df = pd.DataFrame(columns=[0,1,2,3,4])

  for col in df.columns:
    df[col]=[" " for i in range(5)]

  row=0
  col=0
  p=""
  for char in key:
    if char not in p:
      p=p+char

  for i in p:
    df[col][row]=i
    if(col<4):
      col=col+1
    else:
      row=row+1
      col=0

  alphabets=[]
  for i in range(ord('a'),ord('z')+1):
    alphabets.append(chr(i))

  if('i' in p or 'j' in p):
    alphabets.remove('i')
    alphabets.remove('j')

  newL=[]
  for alpha in alphabets:
      if(alpha not in p):
          newL.append(alpha)

  if('i' in newL):
    newL.remove('j')

  for letter in newL:
    df[col][row]=letter
    if(col<4):
      col=col+1
    else:
      row=row+1
      col=0

  pairs=[]

  i=0
  while i<len(pt):
    try:
      if(pt[i]==pt[i+1]):
        pair = pt[i] + "x"
        i=i+1
        pairs.append(pair)
      else:
        pair=pt[i]+pt[i+1]
        i=i+2
        pairs.append(pair)
    except(IndexError):
      pair = pt[i] + "x"
      pairs.append(pair)
      break

  ct=""
  for i in pairs:
    res1=np.where(df==i[0])
    res2=np.where(df==i[1])

    row1=res1[0][0]
    col1=res1[1][0]

    row2=res2[0][0]
    col2=res2[1][0]

    if(col1==col2):
      if(row1==4):
        row1=0
      else:
        row1=row1+1
      if(row2==4):
        row2=0
      else:
        row2=row2+1

    elif(row1==row2):
      if(col1==4):
        col1=0
      else:
        col1=col1+1
      if(col2==4):
        col2=0
      else:
        col2=col2+1

    else:
      temp=col1
      col1=col2
      col2=temp

    l1=df[col1][row1]
    l2=df[col2][row2]
    newPair=l1+l2
    ct=ct+newPair

  return ct, df

ct,df=encrypt('instruments','monarchy')

ct

df

"""# RSA"""

import random
from sympy import isprime,mod_inverse
def gcd(a, b):
    if a == 0:
        return b

    return gcd(b % a, a)

def generatePrime(bits):
  p=random.getrandbits(bits)
  if(isprime(p)):
    return p
  else:
    return generatePrime(bits)

def encrypt(pt,e,n):
  ct=[pow(ord(char),e,n) for char in pt]
  return ct

def decrypt(ct,d,n):
  pt=[chr(pow(char,d,n)) for char in ct]
  p=""
  for i in pt:
    p=p+i
  return p

bits=10
p=generatePrime(bits)
q=generatePrime(bits)

print('Value of p selected: ')
print(p)
print('Value of q selected: ')
print(q)

n=p*q

phi=(p-1)*(q-1)

e=random.randrange(1,phi)
g=gcd(e,phi)
while(g!=1):
  e=random.randrange(1,phi)
  g=gcd(e,phi)

d=mod_inverse(e,phi)

print('Private Key: ')
print((e,n))

print('Public Key: ')
print((d,n))

ct=encrypt('hello',e,n)

ct

decrypt(ct,d,n)

"""# RSA with Digital Signature"""

import random
from sympy import isprime,mod_inverse
from hashlib import sha256
def gcd(a, b):
    if a == 0:
        return b

    return gcd(b % a, a)

def generatePrime(bits):
  p=random.getrandbits(bits)
  if(isprime(p)):
    return p
  else:
    return generatePrime(bits)

def encrypt(pt):
  pt=sha256(pt.encode('utf-8')).hexdigest()
  print("Hashed input")
  print(pt)
  bits=10
  p=generatePrime(bits)
  q=generatePrime(bits)

  print('Value of p selected: ')
  print(p)
  print('Value of q selected: ')
  print(q)

  n=p*q

  phi=(p-1)*(q-1)

  e=random.randrange(1,phi)
  g=gcd(e,phi)
  while(g!=1):
    e=random.randrange(1,phi)
    g=gcd(e,phi)

  d=mod_inverse(e,phi)

  print('Private Key: ')
  print((e,n))

  print('Public Key: ')
  print((d,n))

  ct=""
  for i in pt:
    ct=ct+str(pow(ord(i),e,n))

  return ct

encrypt('hello')

"""# Diffie Hellman"""

from sympy import isprime,mod_inverse
def primitiveCheck(g,p):
  l1=[]
  for i in range(1,p):
    l1.append(pow(g,i)%p)
  for i in l1:
    if(l1.count(i)>1):
      return -1
    return 1

p=random.randrange(1024)
while(True):
  if(isprime(p)):
    break
  else:
    p=random.randrange(1024)

g=random.randrange(p)
while(True):
  if(primitiveCheck(g,p)==1):
    break
  else:
    g=random.randrange(p)

a=int(input("Select private Key for Alice"))
b=int(input("Select private key for Bob"))

x1=pow(g,a)%p
y1=pow(g,b)%p

x2=pow(y1,a)%p
y2=pow(x1,b)%p

if(x2==y2):
  print("Key Exchange successul!")
  print("Shared private Key")
  print(x2)

"""# Diffie Hellman Man In the Middle"""

from sympy import isprime,mod_inverse
def primitiveCheck(g,p):
  l1=[]
  for i in range(1,p):
    l1.append(pow(g,i)%p)
  for i in l1:
    if(l1.count(i)>1):
      return -1
    return 1

p=random.randrange(1024)
while(True):
  if(isprime(p)):
    break
  else:
    p=random.randrange(1024)

g=random.randrange(p)
while(True):
  if(primitiveCheck(g,p)==1):
    break
  else:
    g=random.randrange(p)

a=int(input("Select private Key for Alice"))
b=int(input("Select private key for Bob"))
c=int(input("Select private key for Hacker"))

x1=pow(g,a)%p
h1=pow(g,c)%p
y1=pow(g,b)%p

x2=pow(h1,a)%p
hx2=pow(x1,c)%p

hy2=pow(y1,c)%p
y2=pow(h1,b)%p

if(hx2==x2):
  print("Hacker has connected with Alice")
  print("Shared key of Hacker with Alice")
  print(hx2)

if(hy2==y2):
  print("Hacker has connected with Bob")
  print("Shared key of Hacker with Bob")
  print(hy2)