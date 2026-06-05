
##EVANGELOS BASDAVANOS 4962 ##

def function1(x):
#{
    while (x - 2) > 0:
    #{
        if (x-4) == 0:
            return 2
        elif x == 4:
            return 3
        else:
            return 5
        x = x -1
    #}
#}

def function2(y):
#{
    while y > 0:
    #{
        if y > 5:
            return 6
        else:
            return 4
        y = y - 2
    #}
#}

def function3(z):
#{
    while z < 8:
    #{
        if z % 7 == 0:
            return 4
        elif z == 6:
            return 6
        z = z + 1
    #}
#}

def function4(a):
#{
    while a < 5:
    #{
        if a == 3:
            return 3
        else:
            return -1
        a = a + 1
    #}
#}

#def main

print(function1(8))
print(function2(8))
print(function3(6))
print(function4(1))