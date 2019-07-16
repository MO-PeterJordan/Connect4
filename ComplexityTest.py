a = True
b = False
c = True
d = False
e = True
f = False
g = True
h = False


for i in range(5):
    success = False
    while success == False:
        if a:
            if b:
                if c:
                    if e:
                        if f:
                            print("Moo?")
                        elif g:
                            print("Baaa!")
                        elif h:
                            print("Cluck!")
                    else:
                        print(1)
                elif d:
                    print("Whyyy?")
                else:
                    success = True
                    print(2)
            elif c:
                print("  ")
            else:
                print(3)
        else:
            print("Good Grief!")