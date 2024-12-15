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

    eq1 = """
    udf(f, pow(var(c), sum(sum(num(2), num(3)), var(e))))
    """

    eq2 = """
    udf(f, pow(var(a), sum(sum(var(b), num(1)), num(4))))
    """

    # eq2 = "sum(fraq(mul(var(M_{1}), mul(var(b_{1}), var(T_{1}))), var(W_{1})), fraq(mul(num(-1), mul(var(M_{2}), mul(var(D_{2}), var(T_{2})))), var(W_{2})))"

    eq1 = """
        sum(mul(pow(var(x), fraq(num(1), num(2))), fraq(var(b), var(c))), log(var(a), var(x)))
        """
    eq2 = """
        sum(mul(var(h), var(theta)), log(mul(num(-1), pow(num(6), var(d))), var(dnu)))
        """

    checker: ExpressionChecker = ExpressionChecker(eq1, eq2, True)
    numIter = 500
    run = checker.search(numIter)
    (s, d, n1, n2) = next(run)
    print("--------------------------------------------------")
    print("equation 1:")
    print(checker.strRepr1)
    print("--------------------------------------------------")
    print("equation 2:")
    print(checker.strRepr2)
    print("--------------------------------------------------")
    print("result: ", s, "similarity: ", d)
    print("--------------------------------------------------")
    print(n1.lineagePretty(8))
    print("--------------------------------------------------")
    print(n2.lineagePretty(8))

    print(checker.forest1.forestPretty())
    print(checker.forest2.forestPretty())

    print(n1.getGrammarStringRepr())
    print(SearchNode(n1.getGrammarStringRepr()))

    # ans = ExpressionChecker.getEqualUpToVariables(checker.forest1,checker.forest2)

    # print(ans)


if __name__ == "__main__":
    main()
