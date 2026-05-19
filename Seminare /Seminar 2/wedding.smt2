

; We introduce a variable XY to indicate that guest X sits in chair Y
(declare-const AL Bool)
(declare-const AM Bool)
(declare-const AR Bool)
(declare-const BL Bool)
(declare-const BM Bool)
(declare-const BR Bool)
(declare-const CL Bool)
(declare-const CM Bool)
(declare-const CR Bool)

; Still, we have to specify to Z3 that:
; Every person sits in exactly one chair and 
; Every chair holds exactly one person.

; The hidden rules implementation

; 1. Each person gets exactly one chair

(assert 
    (and 
        (or AL AM AR)
        (not (and AL AM))
        (not (and AL AR))
        (not (and AM AR))
    )
)

(assert
    (and 
        (or BL BM BR)
        (not (and BL BM))
        (not (and BL BR))
        (not (and BM BR))
    )
)

(assert 
    (and
        (or CL CM CR)
        (not (and CL CM))
        (not (and CL CR))
        (not (and CM CR))
    )
)

; 2. Each chair holds exactly one person

(assert
    (and
        (or AL BL CL)
        (not (and AL BL))
        (not (and AL CL))
        (not (and BL CL))
    )
)

(assert
    (and
        (or AM BM CM)
        (not (and AM BM))
        (not (and AM CM))
        (not (and BM CM))
    )
)

(assert
    (and
        (or AR BR CR)
        (not (and AR BR))
        (not (and AR CR))
        (not (and BR CR))
    )
)

; Alice does not want to sit on the leftmost chair
(assert (not AL))

; Alice does not want to sit next to Charlie
(assert 
    (and
        (=> (or AL AR) (not CM))
        (=> AM (and (not CL) (not CR)))
    )
)

; Bob does not want to sit to the right of Charlie
; if CM => not BR
; if CL => not BM and not BR
; if CR => BL or BM

(assert
    (and
        (=> CL (and (not BM) (not BR)))
        (=> CM (not BR))
    )
)

(check-sat)
; (get-model) ; this line fails if unsat, and the problem is indeed unsatisfied




