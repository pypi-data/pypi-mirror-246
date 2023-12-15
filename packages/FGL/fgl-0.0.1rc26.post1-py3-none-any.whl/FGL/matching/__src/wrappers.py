from .. import __lib
import networkx
import scipy
import copy
from typing import Optional
# This file contains python wrappers for our C functions.
# The whole purpose of that is to make it easier for
# auto-completions to know our function definitions.

# __lib is the compiled library containing our c functions.

def max_cardinality_matching(rows, cols, matching):
    return __lib.match_wrapper(rows, cols, matching)

def max_cardinality_matching(G: networkx.Graph, init_list: Optional[list] = []):
    sparse = networkx.to_scipy_sparse_array(G,format="csr")
    rows = sparse.indptr.tolist()
    cols = sparse.indices.tolist()
    result_matching = []
    __lib.match_wrapper(rows, cols, init_list, result_matching)
    return copy.deepcopy(result_matching)
