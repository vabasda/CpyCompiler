#EVANGELOS BASDAVANOS 4962
import sys
import copy

state = 0
myList = []
family = []
line_number = []
returnlist = []
C_true = []
C_false = []
BT_true = []
BT_false = []
BF_true = []
BF_false = []
ifListTemp = []
quads = []
flagreturn = 0
scopes = []
current_scope = []
scopes_tobeprinted = []
produceflag = 0
lCounter = 1
alreadyInDef = 0
flag_for_scope = 0
line_counter = 1
label = 1
changed = 0 
scope_temp = []
varCounter = 1
nestingLevel = 0
taken = ["main","def","#def","#int","global","if","elif","else","while","print","return","input","int","and","or","not"]
word =''
checkifmissed = False

#LEX ANALYSIS----------------------------------------------------------

def lex(file):
	global state 
	global line_counter
	global word
	global checkifmissed
	file = open(file, 'r')
	a = file.read(1)
	while state != "OK" and state != -1:
		
		if checkifmissed == False:
			if a == "\n":
				line_counter += 1
			a = file.read(1)
		if state == 9 and a.isspace():
			if word == "int":
				myList.append("#int")
				family.append("taken")
				line_number.append(line_counter)
				state = 0 
				checkifmissed = True 
				word = ""
			elif word == "def":
				myList.append("#def")
				family.append("taken")
				line_number.append(line_counter)
				state = 0 
				checkifmissed = True 
				word = ""
			else:
				print("Expected #int or #def")
				raise SystemExit
				state = -1
		elif a != '=' and state == 6:
			myList.append('=')
			family.append("celebrant")
			line_number.append(line_counter)
			state = 0 
			checkifmissed = True
		elif a != '=' and state == 4:
			myList.append('<')
			family.append("rel_op")
			line_number.append(line_counter)
			state = 0
			checkifmissed = True
		elif state == 5 and a != '=' :
			myList.append('>')
			family.append("rel_op")
			line_number.append(line_counter)
			state = 0 
			checkifmissed = True
		elif (a.isalpha() or a.isdigit()) and state == 1:
			state = 1
			word += a
			checkifmissed = False
		elif state == 1 and (not a.isalpha() or not a.isdigit()):
			if len(word) > 30:
				word = word[:30]
			myList.append(word)
			if word in taken :
				family.append("taken")
				line_number.append(line_counter)
			else:
				family.append("identifier")
				line_number.append(line_counter)
			word = ''
			checkifmissed = True
			state = 0
		elif state == 2 and not (a.isdigit()):
			if a.isalpha():
				print("Expected number and not letter on line",line_counter)
				raise SystemExit
				state = -1
			elif int(word) < 32767 :
				myList.append(word)
				family.append("constant")
				line_number.append(line_counter)
				word = ''
				state = 0 
				checkifmissed = True
			else:
				state = -1
		elif a.isalpha() and state == 0:
			state = 1
			word += a
			checkifmissed = False
		elif a.isdigit() and state == 0 :
			word += a
			state = 2
			checkifmissed = False
		elif state == 2 and a.isdigit():
			state = 2
			word += a
			checkifmissed = False
		elif a == "+":
			myList.append("+")
			family.append("add_op")
			line_number.append(line_counter)
			state = 0
			checkifmissed = False
		elif a =='-':
			myList.append('-')
			family.append("add_op")
			line_number.append(line_counter)
			state = 0 
			checkifmissed = False
		elif a == '*':
			myList.append('*')
			family.append("mul_op")
			line_number.append(line_counter)
			state = 0
			checkifmissed = False
		elif a == '/' and state == 0:
			state = 3
			checkifmissed = False
		elif a == '/' and state == 3:
			myList.append("//")
			family.append("mul_op")
			line_number.append(line_counter)
			state = 0 
			checkifmissed = False
		elif a != '/' and state == 3:
			print("Expected / after / on line",line_counter)
			raise SystemExit
			state = -1
		elif a == '%':
			myList.append("%")
			family.append("mul_op")
			line_number.append(line_counter)
			state = 0 
			checkifmissed = False
		elif a == '<' and state == 0:
			state = 4
			checkifmissed = False
		elif a == '=' and state == 4:
			myList.append("<=")
			family.append("rel_op")
			line_number.append(line_counter)
			state = 0
			checkifmissed = False
		elif a == '>' and state == 0:
			state = 5
			checkifmissed = False
		elif a == '=' and state == 5:
			myList.append(">=")
			family.append("rel_op")
			line_number.append(line_counter)
			state = 0
			checkifmissed = False
		elif a == '=' and state == 0:
			state = 6 
			checkifmissed = False
		elif a == '=' and state == 6:
			myList.append("==")
			family.append("rel_op")
			line_number.append(line_counter)
			state = 0
			checkifmissed = False
		elif a == '!' and state == 0:
			state = 7
			checkifmissed = False
		elif a != '=' and state == 7:
			state = -1
			print("Expected = after ! at line",line_counter)
			raise SystemExit
		elif a == '=' and state == 7:
			myList.append('!=')
			family.append("rel_op")
			line_number.append(line_counter)
			state = 0	
			checkifmissed = False
		elif a == ',' and state == 0:
			myList.append(',')
			family.append("celebrant")
			line_number.append(line_counter)
			state = 0	
			checkifmissed = False
		elif a == ':':
			myList.append(':')
			family.append("celebrant")
			line_number.append(line_counter)
			state = 0	
			checkifmissed = False
		elif a == '(':
			myList.append("(")
			family.append("celebrant")
			line_number.append(line_counter)
			state = 0 
			checkifmissed = False
		elif a == ')':
			myList.append(")")
			family.append("celebrant")
			line_number.append(line_counter)
			state = 0 
			checkifmissed = False
		elif a == '#' and state == 0:
			state = 8
			checkifmissed = False
		elif state == 8 and a == '{':
			myList.append("#{")
			family.append("celebrant")
			line_number.append(line_counter)
			state = 0
			checkifmissed = False
		elif state == 8 and a == '}':
			myList.append("#}")
			family.append("celebrant")
			line_number.append(line_counter)
			state = 0
			checkifmissed = False
		elif state == 8 and a == '#':
			myList.append("##") 
			family.append("comment")
			line_number.append(line_counter)
			state = 0
			checkifmissed = False
		elif state == 8 and a.isalpha() :
			state = 9
			word +=a
			checkifmissed = False
		elif state == 9 and a.isalpha():
			state = 9
			word += a
			checkifmissed = False
		elif state == 8 and (a != ("{","}","#") or not a.isalpha()):
			print("Expected {,},# or #int after # at line",line_counter)
			raise SystemExit
			state = -1
		elif a.isspace():
			state = 0 
			word = ''
			checkifmissed = False
		elif a == "":
			state = "OK"


		
	myList.append("end_of_myList")
	family.append("end_of_family")

counter = 0

#SYNTAX ANALYSIS----------------------------------------------------------

def program():
	path = sys.argv[1]
	lex(path)
	global counter
	createScope()
	defcomment()
	hashtagint()
	defdef()
	hashtagdef()
	scopes_tobeprinted.append(copy.deepcopy(scopes))
	deleteScope()
	
def hashtagint():
	global counter
	while myList[counter] == "#int":
		counter += 1
		if(family[counter] == "identifier"):
			insertEntityVariable(myList[counter],"variable")
			counter += 1 
			while myList[counter] == "," and family[counter+1] == "identifier":
				insertEntityVariable(myList[counter+1],"variable")
				counter += 2		
		else:
			print("Expected identifier after #int at line ",line_number[counter] -1)
			raise SystemExit 

def defdef():
	global counter,alreadyInDef,flag_for_scope
	while myList[counter] == "def":
		alreadyInDef += 1
		flag_for_scope +=1
		counter += 1
		if (family[counter] ==  "identifier"):
			name = myList[counter]
			genQuad("begin_block",name,"_","_")
			defstart = len(quads)-1
			counter += 1
			if myList[counter] == "(":
				counter += 1
				argumentList = actual_par_list()
				args = createArgumentList(argumentList)
				insertEntityFunction(name,quads[-1][0]+1,args,"_")
				createScope()
				for argument in argumentList:
					insertEntityParameter(argument[0],"CV")
				if myList[counter] == ")":
					counter += 1
					if myList[counter] == ":":
						counter += 1
						defcomment()
						if myList[counter] == "#{":
							counter += 1
							defcomment()
							hashtagint()
							defcomment()
							defdef()
							defcomment()
							defglobal()
							defcomment()
							block()
							if myList[counter] == "#}":
								scopes[-2][0][-1][-1] = updateOffset()
								backPatch(returnlist,nextQuad())
								returnlist.clear()
								genQuad("end_block",name,"_","_")
								defend = len(quads)
								alreadyInDef -=1
								if(alreadyInDef==0):
									writeFinal(defstart,defend)
								scopes_tobeprinted.append(copy.deepcopy(scopes))
								deleteScope()
								counter += 1
							else:
								print("Expected #} at the end of the function at line ",line_number[counter])
								raise SystemExit
						else:
							print("Expected #{ at line ",line_number[counter]-1)
							raise SystemExit
					else:
						print("Expected : at line ",line_number[counter]-1)
						raise SystemExit
				else:
					print("Expected ) at line ",line_number[counter])	
					raise SystemExit
			
def expression(): 
	global counter
	oper = None
	op_sign = optional_sign()
	if(op_sign != None):
		T1_place = op_sign + term()
	else:
		T1_place = term()
	while family[counter] == "add_op":
		addop = add_oper(oper)
		T2_place = term()
		w = newTemp()
		genQuad(addop,T1_place ,T2_place ,w)
		insertEntityTempVar(w)
		T1_place = w
	return T1_place

def term(): 
	global counter
	oper = None
	F1_place = factor()
	while(family[counter] == "mul_op"):
		muloper = mul_oper(oper)
		F2_place = factor()
		w  = newTemp()
		insertEntityTempVar(w)
		genQuad(muloper,F1_place,F2_place,w)
		F1_place = w
	return F1_place

def factor(): 
	global counter
	if family[counter] == "constant":
		counter += 1
		return myList[counter -1]
	elif myList[counter] == "(":
		counter += 1
		returnpar = expression()
		if myList[counter] == ")":
			counter += 1
		else:
			print("Expected ) at line ",line_number[counter])
			raise SystemExit
		return returnpar
	elif family[counter] == "identifier":
		name = myList[counter]
		counter += 1
		x = idtail(name)
		if(x != None):
			return x
		else:
			return name

def idtail(name): 
	global counter
	returnpar = None
	if myList[counter] == "(":
		counter += 1
		returnpar = funcparam()
		genQuad("call",name,"_","_")
		if myList[counter] == ")":
			counter +=1 
		else:
			print("Expected ) at the parameter list at line ",line_number[counter])
			raise SystemExit
	return returnpar

def funcparam():
	global counter
	argumentList = []
	E1_place = expression()
	genQuad("par",E1_place,"CV","_")
	while myList[counter] == ",":
		counter += 1
		E2_place = expression()
		genQuad("par",E2_place,"CV","_")
	w = newTemp()
	genQuad("par",w,"RET","_")
	insertEntityTempVar(w)
	return w

def actual_par_list():
	global counter
	argumentList = []
	param = expression()
	argumentList.append([param, "CV"])
	while(myList[counter] == ","):
		counter +=1
		param = expression()
		argumentList.append([param, "CV"])
	return argumentList

def defstatement():
	global counter 
	if family[counter] == "identifier":
		name = myList[counter]
		counter += 1
		defassignment(name)
	elif myList[counter] == "if":
		defif()
	elif myList[counter] == "return":
		counter += 1
		defreturn()
	elif myList[counter] == "while":
		counter += 1
		defwhile()
	elif myList[counter] == "print":
		counter += 1
		defprint()
	else:
		print("Error occured at line ",line_number[counter])
		raise SystemExit

def block():
	defstatement()
	max_value = len(myList)
	if counter <= max_value - 1:
		while (myList[counter] in ["#int","global","if","return","def","while","print"] or family[counter] in ["identifier","comment"] ):
			defstatement()
			if counter > max_value - 1:
				break

def optional_sign():
	global counter
	oper = None
	op_sign = None
	if myList[counter] == "+" or myList[counter] == "-" :
		op_sign = add_oper(oper)
	return op_sign
	
def mul_oper(oper):
	global counter 
	if(myList[counter] == "*"):
		oper = myList[counter]
		counter+=1
	elif(myList[counter] == "//"):
		oper = myList[counter]
		counter+=1
	elif(myList[counter] == "%"):
		oper = myList[counter]
		counter+=1
	else:
		print("Expected *,//,%  at line ",line_number[counter])
		raise SystemExit 
	return oper

def rel_oper(oper):
	global counter 
	if(myList[counter] == "=="):
		oper = myList[counter]
		counter+=1
	elif(myList[counter] == "<"):
		oper = myList[counter]
		counter+=1
	elif(myList[counter] == ">"):
		oper = myList[counter]
		counter+=1
	elif(myList[counter] == "!="):
		oper = myList[counter]
		counter+=1
	elif(myList[counter] == ">="):
		oper = myList[counter]
		counter+=1
	elif(myList[counter] == "<="):
		oper = myList[counter]
		counter+=1
	else:
		print("Expected ==,>,<,>=,<=,!= at line ",line_number[counter])
		raise SystemExit
	return oper

def add_oper(oper):
	global counter 
	if(myList[counter] == "+"):
		oper = myList[counter]
		counter+=1
	elif(myList[counter] == "-"):
		oper = myList[counter]
		counter+=1
	else:
		print("Expected + or - at line ",line_number[counter])
		raise SystemExit
	return oper

def defcomment():
	global counter
	flag = 0
	while(family[counter] == "comment"):
		counter += 1
		start_line = line_number[counter]
		while myList[counter] != "##":
			counter += 1
			if line_number[counter] - start_line > 6:
				flag = 1
				break
		if  flag == 1:
			print("Comment longer than usual, check for correct syntax. Comments should start and end with ##")
		counter += 1

def defglobal():
	global counter 
	while myList[counter] == "global":
		counter += 1
		if (family[counter] == "identifier"):
			counter += 1
			while(myList[counter] == "," and family[counter+1] == "identifier"):
				counter += 2
		else:
			print("Expected identifier after global at line ",line_number[counter] -1) 

def defassignment(name):
	global counter
	if myList[counter] == "=":
		counter += 1
		if myList[counter] == "int":
			counter += 1
			if myList[counter] == "(":
				counter += 1
				if myList[counter] == "input":
					w = newTemp()
					genQuad("inp","_","_",w)
					genQuad(":=",w,"_",name)
					insertEntityTempVar(w)
					counter += 1
					if myList[counter] == "(":
						counter += 1
						if myList[counter] == ")":
							counter += 1
							if myList[counter] == ")":
								counter += 1
							else:
								print("Expected ) at line ",line_number[counter])
								raise SystemExit
						else:
							print("Expected ) at line ",line_number[counter])
							raise SystemExit
					else:
						print("Expected ( at line ",line_number[counter])
						raise SystemExit
				else:
					print("Expected input at line ",line_number[counter])
					raise SystemExit
			else:
				print("Expected ( at line ",line_number[counter])
				raise SystemExit
		else:
			E_place = expression()
			genQuad(":=",E_place,"_",name)
		

def defif():
	global counter 
	global C_true
	global C_false
	global ifList
	global ifTrue
	global flagreturn
	flag = 3
	flag2=0
	flagreturn=0
	ifList = []
	tempElifList= []
	counter += 1
	condition()
	ifTrue = []
	ifFalse = []
	ifTrue = C_true.copy()
	ifFalse = C_false.copy()
	if myList[counter] == ":":
		counter += 1
		start_line = line_number[counter]
		if myList[counter] == "#{":
			counter += 1
			backPatch(ifTrue,nextQuad())
			block()
			ifList.append(makeList(nextQuad()))
			genQuad("jump","_","_","_")
			backPatch(ifFalse,nextQuad())
			if myList[counter] == "#}":
				counter += 1
			else:
				print("#} expected at line ",line_number[counter])
				raise SystemExit
		else:
			backPatch(ifTrue,nextQuad())
			defstatement()
			if flagreturn ==0:
				ifList.append(makeList(nextQuad()))
				genQuad("jump","_","_","_")
			backPatch(ifFalse,nextQuad())
		if myList[counter] == "elif":
			tempElifList = defelif(ifList)
			flag = 2
		if myList[counter] == "else":
			counter += 1
			flag2=1
			if(flag == 2):
				defelse(tempElifList)
			else:
				defelse(ifList)
		if(flag2==0):
			backPatch(ifList,nextQuad())
	else:
		print("Check the syntax of the if condition on line",line_number[counter]-1)
		raise SystemExit

def defelif(ifList):
	global counter 
	global C_true
	global C_false
	global elifListTemp
	global flagreturn
	flagreturn = 0
	elifList = []
	while myList[counter] == "elif":
		counter += 1
		condition()
		elifTrue = []
		elifFalse = []
		elifTrue = C_true.copy()
		elifFalse = C_false.copy()
		if myList[counter] == ":":
			counter += 1
			start_line = line_number[counter]
			if myList[counter] == "#{":
				counter += 1
				backPatch(elifTrue,nextQuad())
				block()
				genQuad("jump","_","_","_")
				backPatch(elifFalse,nextQuad())
				if myList[counter] == "#}":
					counter += 1
				else:
					print("#} expected at line ",line_number[counter])
					raise SystemExit
			else:
				backPatch(elifTrue,nextQuad())
				defstatement()
				if flagreturn == 0:
					elifList.append(makeList(nextQuad()))
					genQuad("jump","_","_","_")
				backPatch(elifFalse,nextQuad())
			elifList = mergeList(ifList,elifList)
			elifListTemp = elifList.copy()
		else:
			print("Check the syntax of the elif condition on line ",line_number[counter]-1)
			raise SystemExit
	return elifList

	
def defelse(elifList):
	global counter ,flagreturn
	flagreturn=0
	if myList[counter] == ":":
		counter += 1
		if myList[counter] == "#{":
			counter += 1
			block()
			if myList[counter] == "#}":
				counter += 1
			else:
				print("#} expected at line ",line_number[counter])
				raise SystemExit
		else:
			defstatement()
		backPatch(elifList,nextQuad())
	else:
		print("Check the syntax of the else condition on line ",line_number[counter]-1)
		raise SystemExit

def defwhile():
	global counter 
	global C_true
	global C_false
	flag = 0
	B_quad = nextQuad()
	condition()
	whileFalse = []
	whileTrue = []
	whileFalse = C_false.copy()
	whileTrue = C_true.copy()
	if myList[counter] == ":":
		counter += 1
		if myList[counter] == "#{":
			counter += 1
			backPatch(whileTrue,nextQuad())
			block()
			genQuad("jump","_","_",B_quad)
			backPatch(whileFalse,nextQuad())
			if myList[counter] == "#}":
				counter += 1
			else:
				print("#} expected at line ",line_number[counter])
				raise SystemExit
		else:
			backPatch(whileTrue,nextQuad())
			defstatement()
			genQuad("jump","_","_",B_quad)
			backPatch(whileFalse,nextQuad())
	else:
		print(": expected on line", line_number[counter]-1)
		raise SystemExit

def condition():
	global counter
	global C_true
	global C_false
	C_true = []
	C_false = []
	bool_term()
	for row in BT_true :
		C_true.append(row)
	for row in BT_false :
		C_false.append(row)
	while myList[counter] == "or":
		counter += 1 
		backPatch(C_false,nextQuad())
		bool_term()
		C_true = mergeList(C_true,BT_true)
		C_false = BT_false

def bool_term():
	global counter
	global BT_true
	global BT_false
	BT_true = []
	BT_false = []
	bool_factor()
	for row in BF_true :
		BT_true.append(row)
	for row in BF_false :
		BT_false.append(row)
	while myList[counter] == "and" :
		counter += 1
		backPatch(BT_true,nextQuad())
		bool_factor()
		BT_true = BF_true
		BT_false = mergeList(BT_false,BF_false)

def bool_factor():
	global counter
	global BF_true
	global BF_false
	BF_true = []
	BF_false = []
	oper = None 
	if myList[counter] == "not":
		counter += 1
		E1_place = expression()
		if myList[counter] == "rel_op":
			oper = rel_oper(myList[counter])
			E2_place = expression()
			BF_true.append(makeList(nextQuad()))
			genQuad(oper,E1_place,E2_place,"_")
			BF_false.append(makeList(nextQuad()))
			genQuad("jump","_","_","_")
	else:
		E1_place = expression()
		if family[counter] == "rel_op":
			oper = rel_oper(myList[counter])
			E2_place = expression()
			temp1 = makeList(nextQuad())
			BF_true.append(temp1) 
			genQuad(oper,E1_place,E2_place,"_")
			temp2 = makeList(nextQuad())
			BF_false.append(temp2)
			genQuad("jump","_","_","_")

def defreturn():
	global counter
	global flagreturn
	if myList[counter] == "(":
		counter += 1
		E_place = expression()
		if myList[counter] == ")":
			counter += 1
		else:
			print("Expected ) at line" ,line_number[counter])
			raise SystemExit
		genQuad("retv",E_place,"_","_")
		temp = makeList(nextQuad())
		returnlist.append(temp)
		genQuad("jump","_","_","_")
		flagreturn=1
	else:
		E_place = expression()
		genQuad("retv",E_place,"_","_")
		temp = makeList(nextQuad())
		returnlist.append(temp)
		genQuad("jump","_","_","_")
		flagreturn=1

def defprint():
	global counter
	if myList[counter] == "(":
		counter += 1
		E_place = expression()
		if myList[counter] == ")":
			counter += 1
		else:
			print("Expected ) on line" ,line_number[counter]-1)
			raise SystemExit
		genQuad("out",E_place,"_","_")
	else:
		print("Expected ( on line" ,line_number[counter])
		raise SystemExit

def hashtagdef():
	global counter
	if myList[counter] == "#def":
		defstart = len(quads)
		counter += 1
		if myList[counter] == "main":
			genQuad("begin_block","main","_","_")
			insertEntityFunction("main",quads[-1][0]+1,[],"_")
			createScope()
			counter += 1
			defcomment()
			hashtagint()
			defcomment()
			block()
			defcomment()
			genQuad("halt","_","_","_")
			scopes[-2][0][-1][-1] = updateOffset()
			genQuad("end_block","main","_","_")
			defend = len(quads)
			writeFinal(defstart,defend)
			scopes_tobeprinted.append(copy.deepcopy(scopes)) 
			deleteScope()
		else:
			print("main expected after #def at line " ,line_number[counter]-1)
	else:
		print("Main def is required! If main is in the code please check that you write below the first line of your editor.")
		raise SystemExit

#ENDIAMESOS KODIKAS----------------------------------------------------------

def genQuad(operator,operand1, operand2, operand3):
	global label
	quad = [label,operator,operand1,operand2,operand3]
	quads.append(quad)
	label += 1
	return quad

def nextQuad():
	global label
	return label 

def emptyList():
	newEmptyList = []

def makeList(x):
	newList = []
	newList.append(x)
	return newList

def backPatch(list,label):
	for sublist in list:
		labelOfList = sublist[0]
		for quad in quads:
			if quad[0] == labelOfList :
				quad[4] = label

def mergeList(list1, list2):
    merged_list = list1 + list2
    return merged_list

def newTemp():
	global varCounter
	newTemp = "T_"+ str(varCounter)
	varCounter += 1
	return newTemp

def saveEndiamesos():
    with open("endiamesos.int", 'w') as file:
        for quad in quads:
            file.write(f"{quad[0]} : {quad[1]} {quad[2]} {quad[3]} {quad[4]}\n")

#PINAKAS SYMVOLON----------------------------------------------------------

def createScope():
	global scopes 
	global current_scope
	global nestingLevel
	listEntities = []
	scope = [listEntities,nestingLevel] 
	scopes.append(scope)
	scope_temp.append(scope)
	nestingLevel+=1
	current_scope = scopes[-1]

def deleteScope():
	global scopes
	global current_scope
	global nestingLevel
	global flag_for_scope
	if scopes:
		del scopes[-1]
		nestingLevel -= 1
	if alreadyInDef == 0 and flag_for_scope>0:
		del scope_temp[-flag_for_scope:]
		flag_for_scope = 0
	if len(scopes) != 0:
		current_scope = scopes[-1]

def insertEntityVariable(name,type):
	global current_scope
	offset = updateOffset()
	entity = [name,"variable",offset]
	current_scope[0].append(entity)
	
def insertEntityFunction(name,startQuad,argumentList,frameLength):
	global current_scope
	entity = [name,"function",startQuad,argumentList,frameLength]
	current_scope[0].append(entity)

def insertEntityConstant(name,type,value):
	global current_scope
	entity = [name,"constant",value]

def insertEntityParameter(name,parMode):
	global current_scope
	offset = updateOffset()
	entity = [name,"parameter",offset,parMode]
	current_scope[0].append(entity)

def insertEntityTempVar(name):
	global current_scope
	offset = updateOffset()
	entity = [name,"tempVar",offset]
	current_scope[0].append(entity)

def searchEntity(entity):
	found = 0
	result = -1
	for scope in scope_temp:
		nestingLevelTemp = scope[1]
		for element in scope[0]:
			if element[0] == entity:
				result = [element,nestingLevelTemp]
	return result

def updateOffset():
	if(current_scope[0] == []):
		offset = 12
	else:
		lastoffset = -1
		for listEntities in current_scope[0]:
			if listEntities[1] == "variable" or listEntities[1] == "parameter" or listEntities[1] == "tempVar":
				lastoffset = listEntities[2] + 4
		offset = lastoffset
	return offset

def findLastOffset():
	for listEntities in current_scope[0]:
			if listEntities[1] == "variable" or listEntities[1] == "parameter" or listEntities[1] == "tempVar":
				offset = listEntities[2] 
	return offset

def createArgumentList(argumentList):
	paramMode = []
	for argument in argumentList:
		paramMode.append(argument[1])
	return paramMode

def saveSymbol():
	with open("symbol.sym", 'w') as file:
	    for scope in scopes_tobeprinted:
	    	for innerscope in scope:
	    		file.write("\n")
	    		file.write(f"Scope {innerscope[1]} \n")
	    		file.write("\n")
	    		file.write(f"{innerscope[0]} \n")
	    	file.write("\n-----------------------------------------------------------------------------\n\n")

#FINAL CODE----------------------------------------------------------

def gnlvcode(entity):
    global lCounter
    element = searchEntity(entity)
    if element != -1:
        flag = (nestingLevel) - element[1]
        if flag > 0:
            repeated_code = "     lw t0,-4(t0)" * (flag)
            produce(f"	lw t0,-4(sp)\n")
            produce(f"{repeated_code}\n")
            produce(f"     addi t0,t0,-{element[0][2]}\n")
        else:
            produce(f"lw t0,-4(sp)\n")  
            produce(f"     addi t0,t0,-{element[0][2]}\n")
    else:
        print("Couldn't find",entity,".Please ensure that the init is correct!")
        raise SystemExit


def loadvr(v,reg):
	global lCounter
	if(v.isdigit() or v.startswith('-') and v[1:].isdigit()):
		produce(f"	li {reg},{v}\n")
	else:
		element = searchEntity(v)
		if element != -1:
			if ((element[0][1] == "variable"  or element[0][1] == "parameter")  and nestingLevel-1 == element[1]) or element[0][1] == "tempVar":
				produce(f"	lw {reg},-{element[0][2]}(sp)\n")
			elif(element[1] == 0):
				produce(f"	lw {reg},-{element[0][2]}(gp)\n")
			else:
				gnlvcode(v)
				produce(f"	lw {reg},-0(t0)\n")
		else:
			print("Couldn't find",v,".Please ensure that the init is correct!")
			raise SystemExit

def storerv(r,v):
	global lCounter
	element = searchEntity(v)
	if element != -1:
		if(element[1] == 0):
			produce(f"	sw {r},-{element[0][2]}(gp)\n")
			
		elif ((element[0][1] == "variable"  or element[0][1] == "parameter")  and nestingLevel-1 == element[1]) or element[0][1] == "tempVar":
			produce(f"	sw {r},-{element[0][2]}(sp)\n")
		else:
			gnlvcode(v)
			produce(f"	sw {r},-0(t0)\n")
	else:
		print("Couldn't find",v,".Please ensure that the init is correct!")
		raise SystemExit

def writeFinal(defstart,defend):
	global lCounter	
	if defstart == 0:
		produce(".data \n")
		produce('str_nl: .asciz "\\n" \n')
		produce(".text\n")
		produce("L0: jal Lmain\n")
	icount = 0
	rel_map = {"<": "blt",">": "bgt","!=": "bne",">=": "bge","<=": "ble","==": "beq"}
	addmul_map = {"+":"add","-":"sub","//":"div","*":"mul","%":"rem"}
	lastfunccalled = 0
	for quad in quads[defstart:defend]:
		match quad:
			case [u,"jump",_,_,x]:
				produce(f"L{lCounter}: jal L{x}\n")
				lCounter+=1
				icount = 0
			case [u,":=",x,_,z]:
				produce(f"L{lCounter}:")
				loadvr(x,"t1")
				storerv("t1",z)
				lCounter+=1
				icount = 0
			case [u,op,x,y,z] if op in ("<",">","!=",">=","<=","=="):
				produce(f"L{lCounter}:")
				loadvr(x,"t1")
				loadvr(y,"t2")
				asm_op = rel_map[op]
				produce(f"	{asm_op} t1,t2,L{z}\n")
				lCounter+=1
				icount = 0
			case [u,op,x,y,z] if op in ("+","-","//","*","%"):
				produce(f"L{lCounter}:")
				loadvr(x,"t1")
				loadvr(y,"t2")
				asm_op = addmul_map[op]
				produce(f"	{asm_op} t1,t1,t2\n")
				lCounter+=1
				icount = 0
				storerv("t1",z)
			case [u,"retv",x,"_","_"]:
				produce(f"L{lCounter}:")
				loadvr(x,"t1")
				produce(f"	lw t0,-8(sp)\n")
				produce(f"	sw t1,0(t0)\n")
				lCounter+=1
				icount = 0
			case [u,"par",x,"CV","_"]:
				produce(f"L{lCounter}:")
				if(icount == 0):
					index =quads[defstart:defend].index(quad)
					for quad in quads[defstart+index:defend]:
						if quad[1] == "call":
							function = quad[2]
							break
					element = searchEntity(function)
					produce(f"	addi fp,sp,{element[0][-1]}\n")
				loadvr(x,"t0")
				calc=12+(4*icount)
				produce(f"	sw t0,-{calc}(fp)\n")
				lCounter+=1
				icount+=1
			case [u,"par",x,"RET","_"]:
				element = searchEntity(x)
				produce(f"L{lCounter}:")
				produce(f"addi t0,sp,-{element[0][2]}\n")
				produce(f"	sw t0,-8(fp)\n")
				lCounter+=1
				icount=0
			case [u,"call",f,"_","_"]:
				element = searchEntity(f)
				for quad in quads:
					if quad[1] == "begin_block" and quad[2]==f:
						number = quad[0]
				produce(f"L{lCounter}:")
				if element[1] == nestingLevel-1 :
					produce(f"	lw t0,-4(sp)\n")
					produce("   sw t0,-4(fp)\n")
					produce(f"	addi sp,sp,{element[0][-1]}\n")
					produce(f"	jal L{number}\n")
					produce(f"	addi sp,sp,-{element[0][-1]}\n")
					lCounter+=1
				else:
					produce(f"	sw sp,-4(fp)\n")
					produce(f"	addi sp,sp,{element[0][-1]}\n")
					produce(f"	jal L{number}\n")
					produce(f"	addi sp,sp,-{element[0][-1]}\n")
					lCounter+=1
				icount=0
			case [u,"begin_block","main","_","_"]:
				produce(f"Lmain:\n")
				produce(f"L{lCounter}:")
				element = searchEntity("main")
				produce(f"	addi sp,sp,{element[0][-1]}\n")
				produce(f"	addi gp,gp,{element[0][-1]}\n")
				lCounter+=1
				icount=0
			case  [u,"halt","_","_","_"]:
				produce(f"L{lCounter}:")
				produce(f"	li a0,0\n")
				produce(f"	li a7,93\n")
				produce(f"	ecall\n")
				lCounter+=1
				icount=0
			case [u,"begin_block",f,"_","_"]:
				produce(f"L{lCounter}:")
				produce(f"	sw ra,0(sp)\n")
				lCounter+=1
				icount=0
			case [u,"end_block",f,"_","_"]:
				if(f != "main"):
					produce(f"L{lCounter}:")
					produce(f"	lw ra,-0(sp)\n")
					produce(f"	jr ra\n")
					lCounter+=1
					icount=0
			case [u,"out",i,"_","_"]:
				produce(f"L{lCounter}:")
				loadvr(i,"t1")
				produce("	mv a0,t1\n")
				produce("	li a7,1\n")
				produce("	ecall\n")
				produce("	la a0,str_nl \n")
				produce("	li a7,4 \n")
				produce("	ecall\n")
				lCounter+=1
				icount=0
			
			case [u,"inp","_","_",temp]:
				produce(f"L{lCounter}:")
				produce(f"	li a7,5\n")
				produce("	ecall\n")
				storerv("a0",temp)
				lCounter+=1
				icount=0		

def produce(x):
	global produceflag
	if produceflag==1:
	    with open('final.asm', 'a') as file:
	        file.write(str(x))
	else:
		with open('final.asm', 'w') as file:
			file.write(str(x))
			produceflag =1

program()
saveEndiamesos()
saveSymbol()
print("endiamesos.int, symbol.sym and final.asm files are ready!")