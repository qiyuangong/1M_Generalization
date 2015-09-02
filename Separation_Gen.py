from partition_for_transaction import partition
from mondrian_l_diversity import mondrian_l_diversity
import time
import pdb


_DEBUG = False
ATT_TREES = []
DATA = []


def Separation_Gen(att_trees, data, k=10, l=5):
    """Using partition_for_transaction to anonymize SA (transaction) partition,
    while applying anatomy to separate QID and SA
    return (result, eval_result)
    result is 2-dimensional list
    eval_result is a tuple (rncp, tncp, rtime)
    """
    global ATT_TREES, DATA
    ATT_TREES = att_trees
    DATA = data
    start_time = time.time()
    if _DEBUG:
        print "size of dataset %d" % len(data)
    result = []
    trans = [t[-1] for t in data]
    trans_set, tncp = partition(att_trees[-1], trans, k)
    partition_data = []
    for ttemp in trans_set:
        (index_list, tran_value) = ttemp
        for t in index_list:
            DATA[t][-1] = tran_value[:]
            partition_data.append(DATA[t][:])
    if _DEBUG:
        print "Begin Mondrian"
    result, rncp = mondrian_l_diversity(ATT_TREES, partition_data, l)
    rtime = float(time.time() - start_time)
    if _DEBUG:
        print "Total running time = %.2f seconds" % rtime
    # transform data format (QID1,.., QIDn, SA set, GroupID, 1/|group size|, Group SA domain)
    # 1/|group size|, Group SA domain will be used in evaluation
    return (result, (rncp, tncp, rtime))
