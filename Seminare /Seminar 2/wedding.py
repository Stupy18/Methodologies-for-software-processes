from z3 import *
xal, xam, xar, xbl, xbm, xbr, xcl, xcm, xcr = Bools('xal xam xar xbl xbm xbr xcl xcm xcr')
s = Solver()

# Alice does not sit next to Charlie
s.add( And( Implies( Or(xal, xar), Not(xcm) ), Implies( xam, And( Not(xcl), Not(xcr)))))

# Alice does not sit on the leftmost chair
s.add( Not(xal) )

# Bob does not sit to the right of Charlie
s.add(And(
    Implies(xcl, And(Not(xbm), Not(xbr))),
    Implies(xcm, Not(xbr))
))

# Each person gets at least one chair
s.add(Or(xal, xam, xar))  # Alice
s.add(Or(xbl, xbm, xbr))  # Bob
s.add(Or(xcl, xcm, xcr))  # Charlie

# Every person gets at most one chair
s.add(Or(Not(xal), Not(xam)), Or(Not(xal), Not(xar)), Or(Not(xam), Not(xar)))  # Alice
s.add(Or(Not(xbl), Not(xbm)), Or(Not(xbl), Not(xbr)), Or(Not(xbm), Not(xbr)))  # Bob
s.add(Or(Not(xcl), Not(xcm)), Or(Not(xcl), Not(xcr)), Or(Not(xcm), Not(xcr)))  # Charlie

# Every chair gets at most one person
s.add(Or(Not(xal), Not(xbl)), Or(Not(xal), Not(xcl)), Or(Not(xbl), Not(xcl)))  # Left
s.add(Or(Not(xam), Not(xbm)), Or(Not(xam), Not(xcm)), Or(Not(xbm), Not(xcm)))  # Middle
s.add(Or(Not(xar), Not(xbr)), Or(Not(xar), Not(xcr)), Or(Not(xbr), Not(xcr)))  # Right

print( s.check() )
if s.check() == sat:
    print(s.model())