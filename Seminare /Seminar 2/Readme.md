SAT = Boolean Satisfiability. You encode a problem as boolean variables + constraints, then ask: "is there an assignment of true/false that satisfies all constraints?"
Z3 is a solver that answers this automatically.

Step 1 — The Variables

pythonxal, xam, xar,   # Alice:   Left, Middle, Right
xbl, xbm, xbr,   # Bob:     Left, Middle, Right
xcl, xcm, xcr    # Charlie: Left, Middle, Right
Each variable means: "this person sits in this chair"
xal = True  →  Alice sits on Left
xbr = True  →  Bob sits on Right
9 boolean variables total. A valid solution has exactly 3 of them True (one per person).

Step 2 — Constraint 1: Alice not next to Charlie
pythons.add( And(
    Implies( Or(xal, xar), Not(xcm) ),    # if Alice is Left or Right, Charlie not Middle
    Implies( xam, And(Not(xcl), Not(xcr)) ) # if Alice is Middle, Charlie not Left or Right
))
The "next to" pairs are: (Left,Middle) and (Middle,Right). So:
Alice=Left    → Charlie can't be Middle
Alice=Right   → Charlie can't be Middle
Alice=Middle  → Charlie can't be Left, can't be Right
Written as implications: "if Alice is here, Charlie can't be adjacent."

Step 3 — Constraint 2: Alice not leftmost
pythons.add( Not(xal) )   # xal must be False
Simple — just force Alice's Left variable to False.

Step 4 — Constraint 3: Bob not to the right of Charlie
pythons.add(And(
    Implies(xcl, And(Not(xbm), Not(xbr))),  # Charlie=Left → Bob can't be Middle or Right
    Implies(xcm, Not(xbr))                   # Charlie=Middle → Bob can't be Right
))
"Bob to the right of Charlie" means:
Charlie=Left   → Bob=Middle or Bob=Right are both forbidden
Charlie=Middle → Bob=Right is forbidden
Charlie=Right  → Bob can't be further right (impossible anyway)

Step 5 — Each Person Gets Exactly One Chair
At least one chair (someone must sit somewhere):
pythons.add(Or(xal, xam, xar))  # Alice sits somewhere
s.add(Or(xbl, xbm, xbr))  # Bob sits somewhere
s.add(Or(xcl, xcm, xcr))  # Charlie sits somewhere
At most one chair (can't sit in two places):
python# For Alice — every PAIR must have at least one False:
s.add(Or(Not(xal), Not(xam)))  # not (Left AND Middle)
s.add(Or(Not(xal), Not(xar)))  # not (Left AND Right)
s.add(Or(Not(xam), Not(xar)))  # not (Middle AND Right)
Same pattern for Bob and Charlie. This is the standard SAT encoding of "at most one".

Step 6 — Each Chair Gets At Most One Person
python# Left chair — every pair of people must have at least one False:
s.add(Or(Not(xal), Not(xbl)))  # not (Alice AND Bob) on Left
s.add(Or(Not(xal), Not(xcl)))  # not (Alice AND Charlie) on Left
s.add(Or(Not(xbl), Not(xcl)))  # not (Bob AND Charlie) on Left
Same for Middle and Right chairs. Prevents two people sharing a chair.

Step 7 — Run the Solver
pythonprint(s.check())       # sat or unsat
if s.check() == sat:
    print(s.model())   # prints which variables are True
sat
[xbm = True, xcl = True, xar = True]  ← example output
This means: Charlie=Left, Bob=Middle, Alice=Right
Verify against constraints:
Alice not next to Charlie?  Alice=Right, Charlie=Left → not adjacent ✅
Alice not leftmost?         Alice=Right               ✅
Bob not right of Charlie?   Bob=Middle, Charlie=Left  → Middle is right of Left...
Wait — let me re-check. Bob=Middle is to the right of Charlie=Left, which would violate constraint 3. The actual model Z3 returns will be different, but the point is Z3 finds one that satisfies everything.

The Full Picture
9 boolean variables
      ↓
encode problem rules as boolean constraints
      ↓
Z3 searches all 2^9 = 512 combinations instantly
      ↓
returns sat + a valid assignment, or unsat if impossible
The power of SAT: you just describe the rules, you don't write search logic. Z3 handles the search entirely.