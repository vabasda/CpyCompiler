
##EVANGELOS BASDAVANOS 4962##
#int grade

def checkgrade(score):
#{
    global grade 
    grade = 10
    if score >= 90:
        return 90
    elif score >= 80:
        return 80
    elif score >= 70:
        return 70
    elif score >= 60:
        return 60
    else:
        return 50
#}

def maxOfThree(a,b,c):
#{
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c
#}

def isThree(n):
#{
    if n == 2:
        return 1
    elif n != 3:
        return -1
#}


#def main
#int scores

scores = 100

while scores > 50:
#{
    print(checkgrade(scores))
    scores = scores - 10
#}

print(maxOfThree(2,6,8))

print(maxOfThree(2,5,9))

print(maxOfThree(34,65,8))

print(isThree(4))

print(isThree(6))
print(isThree(8))