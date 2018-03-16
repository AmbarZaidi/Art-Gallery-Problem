from numpy.random import randint
from easygui import multenterbox
from numpy import lexsort,asarray,append
from matplotlib.pyplot import figure,show

msg = "Enter the value of 'n'"
title = "Polygon with 'n' sides"
fieldNames = ["  n"]
fieldValues = multenterbox(msg,title,fieldNames)
while 1:
    if fieldValues == None: break
    errmsg = ""
    try:
        int(fieldValues[0])
    except:
        errmsg = errmsg + ('%s is a required to be a number.\n\n' % fieldNames[0])
    if fieldValues[0].strip() == "":
        errmsg = errmsg + ('%s is a required field.\n\n' % fieldNames[0])
    if errmsg == "": break
    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    

n = int(fieldValues[0])
fi = 0

for i in range (1,10):
    fi += 1
    coords = randint(-90,90, size=(2,n))
    x = coords[0] 
    y = coords[1]
    ind = lexsort((y,x))
    coords = [(x[i],y[i]) for i in ind] 
    x = asarray([c[0] for c in coords])
    y = asarray([c[1] for c in coords])
    pivot = coords[0]

    y_diff_pivot = y-pivot[1]
    x_diff_pivot = x-pivot[0]
    tan = (y_diff_pivot[1:]+0.0)/x_diff_pivot[1:]

    pairs = zip(tan,coords[1:])
    pairs = sorted(pairs, key = lambda (x,y): x)
    
    coords = asarray([pivot])
    coords = append(coords, asarray( zip(*pairs)[-1] ), axis=0 )
    coords = append(coords, asarray([pivot]), axis=0 )

    print ("Points:", coords)

    ### Plotting generated polygon

    fig = figure('Figure '+str(fi))
    ax = fig.add_subplot(111)
    x = coords[:,0]
    y = coords[:,1]
    ax.plot(x, y, "go")
    ax.fill(x, y, "r")   
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)

    show()