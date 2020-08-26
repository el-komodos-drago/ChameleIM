print("This file contains sub routines that were created for but not used in the main program")
def RandomPrime(cap,prime=([True] * 100000000)):
    #Sieve of Eratosthenes using
    #https://www.geeksforgeeks.org/python-program-for-sieve-of-eratosthenes/
    #as a reference implimentation
    #returns the largest random prime before the cap
    
    #creates a list of length cap with all values being True.
    print("bg")
#    prime = [True for i in range(cap + 1)] 
#     prime = []
#     for i in range (0,cap+1):
#         prime.append(True)
    
    print("2")
    for itteration in range(2, int(sqrt(cap)+1)):
        if prime[itteration] == True: #if itteration is prime...
            #print(str(itteration))
            for i in range(itteration*2, cap+1, itteration):
                prime[i] = False #mark all multiples of itteration as not prime
    print("as")
    for itteration in range(cap,0,-1):
        if prime[itteration] == True:
            return(itteration)

def CheckPrime (number): # checks if a number is prime
    # Primes are numbers that can not be formed by multiplying two other whole numbers
    # numbers that aren't prime are known as composit numbers and the whole numbers they can
    # be divided by are known as factors.
    if number == 1:
        return(False) # discards 1
    if number % 2 == 0:
        return(False) # excludes even numbers
    if number % 3 == 0:
        return(False) # excludes numbers that are multiples of 3
    limit = sqrt(number) + 2 # set the limit to the square root of the number.
    # If the smallest of the two numbers being multiplied is larger than the square root of
    # the number being tested then the result will be larger than the number being tested.
    # We only need to test the smaller of the potential factors because that will also test
    # the larger factor they pair up with.
    
    for iteration in range(3, int(limit)+1, 2):
        #checks odd numbers between 3 and half the value of the number
        #Dev note, upgrade to check 6i - 1 and 6i + 1
        if number % iteration == 0:
            return(False)
    return(True)