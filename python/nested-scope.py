#!/bin/python

X = 11

def firstlevel():
    def secondlevel():
        X = 88 #This is an assignment, it creates or changes the name X in the current scope ( local function scope )
        print(X) #This will reference the local x^^^
    secondlevel()
    print("First level: ", X)

def firstlevelnonlocal():
    X = 88 
    def secondlevel():
        nonlocal X #this assigngs the changes to the namx X in the closest enclosing function's local scope ^This one right above
        X = "188"
        print(X)
    secondlevel()
    print("First level: ", X)

firstlevel() #this should print 88 
firstlevelnonlocal()
print(X) #This will print the global X = 11


