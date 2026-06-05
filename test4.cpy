
##EVANGELOS BASDAVANOS 4962##

#int i 
def factorial(n):
#{
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
#}

#def main


i = int(input())
print(factorial(i))