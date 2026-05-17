from z3 import *
xal, xam, xar, xbl, xbm, xbr, xcl, xcm, xcr = Bools('xal xam xar xbl xbm xbr xcl xcm xcr')
s = Solver()

# Alice does not sit next to Charlie
s.add( And( Implies( Or(xal, xar), Not(xcm) ), Implies( xam, And( Not(xcl), Not(xcr)))))

# Alice does not sit on the leftmost chair
s.add( Not(xal) )

# Bob does not sit to the right of Charlie

# Each person gets a chair

# Every person gets at most one chair




# Every chair gets at most one person




print( s.check() )
