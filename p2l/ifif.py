def a():
    PRINT(0)

def b():
    PRINT(1)

def c():
    PRINT(2)

# Should print 0
if 3 > 2:
    if 2 < 10:
        a()
    else:
        b()
else:
    c()

# Should print 1
if 3 > 2:
    if 2 > 10:
        a()
    else:
        b()
else:
    c()


# Should print 2
if 3 < 2:
    if 2 < 10:
        a()
    else:
        b()
else:
    c()
#0
#1
#2
