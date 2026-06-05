
##EVANGELOS BASDAVANOS 4962 ##
#int positive,negative

def categorizenumber(number):
#{
    global positive,negative 
    positive = positive + 4
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0
#}

def factorial(n):
#{
    #int result
    global negative 
    negative = negative - 4
    if n < 0:
        return -1
    elif n == 0:
        return 1
    else:
        result = 1
        while n > 0:
        #{
            result = result * n
            n = n - 1
        #}
        return result
#}    
     
def countdown(n):
#{
    while n > 0:
    #{
        print(n)
        n = n - 1
    #}
    return n 
#}

def printsamenumber(n):
#{
    if n == 0 :
        return (n+2)
    else:
        return printsamenumber(n-1)

#}
        
#def main
#int i
positive = 5
negative = -10


i = int(input())
print(i)

while i<=15:
#{
    print(i)
    i = i + 1
#}
print(factorial(negative))
print(factorial(4))
print(categorizenumber(3))
print(countdown(5))
print(printsamenumber(3))


print(negative)

