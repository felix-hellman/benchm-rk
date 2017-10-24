from Crypto.Util import number
from Crypto.PublicKey import RSA
import random
import time

class Key:
    exponent = ""
    n = ""

    def __init__(self,exponent,n):
        self.exponent = exponent
        self.n = n

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_keypair(p, q):
    if p == q:
        raise ValueError('p and q cannot be equal')
    #n = pq
    n = p * q

    #Phi is the totient of n
    phi = (p-1) * (q-1)

    #Choose an integer e such that e and phi(n) are coprime
    e = long(3)

    #Use Euclid's Algorithm to verify that e and phi(n) are comprime
    #This should be somewhat unnecessary if e is prime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return (Key(e, n), Key(d, n))

primes = []

keylengths =    [ 512,  1024,   2048,   4096 ]
amountOfKeys =  [ 10,   100,    1000 ]

public = []
private = []

iterations = 5


for nrkeys in amountOfKeys:
    for length in keylengths:
        del primes[:]
        #Generate primes to be used for keys
        for i in xrange(0,nrkeys*2-1):
            primes.append(number.getPrime(length))
        for iter in xrange(iterations):
            file = open(str(nrkeys),"a");
            #Make sure lists are empty before generation
            del public[:]
            del private[:]
            #Generate keys to crack
            for i in xrange(0,nrkeys*2,2):
                a = i
                b = (i+1)%(nrkeys*2-1)
                pub, priv = generate_keypair(primes[a],primes[b])
                public.append(pub)
                private.append(priv)
            #Run GCD on public keys
            start = time.time()
            ###Start timer here
            for y in xrange(len(public)):
                for x in xrange(len(public)):
                    if x != y:
                        answer = gcd(public[y].n ,   public[x].n)
                        ##if answer != 1 key is cracked but who cares?
            ###End timer here
            end = time.time() - start
            unit = "seconds"
            print("Test completed in %s %s, with %d keys with the keysize %d" % (str(end), unit, nrkeys, length) )
            file.write("%s %d\n" % (str(end), length))
            file.close()

