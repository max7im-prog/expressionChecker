import my_parser
import lark
from equiv import Equiv
from searchnode import SearchNode
from expressionchecker import ExpressionChecker
import time
from rapidfuzz.distance import Levenshtein


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np







def main():
    
    eq1 = '''
    fraq(
        sum(
            mul(
                var(b),
                var(c),
                var(a)
            ),
            mul(
                var(d),
                var(c),
                var(e)                
            ),
            mul(
                pow(var(a),num(7)),
                pow(var(a),num(7)),
                pow(var(a),num(4))
            )
        ),
        var(h)
    )
    '''
    
    eq2 = '''
    sum(
        mul(
            var(a),
            var(b),
            var(c),
            pow(var(h),num(-1))           
        ),
        fraq(
            sum(
                mul(
                    var(d),
                    var(c),
                    var(e)                
                ),
                mul(
                    pow(var(a),num(8)),
                    pow(var(a),num(6)),
                    pow(var(a),num(4))
                )
            ),
            var(h)
        )
    )
    '''
    
    
    
    checker: ExpressionChecker = ExpressionChecker(eq1,eq2)
    
    numIter = 200
    run = checker.search(numIter)
    (s,n1,n2) = next(run)
    print("--------------------------------------------------")
    print("equation 1:")
    print(checker.strRepr1)
    print("--------------------------------------------------")
    print("equation 2:")
    print(checker.strRepr2)
    print("--------------------------------------------------")
    print("result:")
    print(s)
    print("--------------------------------------------------")
    print(n1.lineagePretty(8))
    print("--------------------------------------------------")
    print(n2.lineagePretty(8))
    

if __name__ == "__main__":
    main()
