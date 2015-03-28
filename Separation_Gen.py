from partition_for_transaction import partition
from mondrian_l_diversity import mondrian_l_diversity
import time
import pdb


_DEBUG = False
gl_att_trees = []
gl_data = []


def Separation_Gen(att_trees, data, K=10, L=5):
    """Using partition_for_transaction to anonymize SA (transaction) partition,
    while applying anatomy to separate QID and SA
    """
    global gl_att_trees, gl_data
    gl_att_trees = att_trees
    gl_data = data
    start_time = time.time()
    if _DEBUG:
        print "size of dataset %d" % len(data)
    result = []
    trans = [t[-1] for t in data]
    trans_set, tncp = partition(att_trees[-1], trans, K)
    partition_data = []
    for ttemp in trans_set:
        (index_list, tran_value) = ttemp
        for t in index_list:
            gl_data[t][-1] = tran_value[:]
            partition_data.append(gl_data[t][:])
    if _DEBUG:
        print "Begin Mondrian"
    result, rncp = mondrian_l_diversity(gl_att_trees, partition_data, L)
    if _DEBUG:
        print("--- %s seconds ---" % (time.time() - start_time))
    # transform data format (QID1,.., QIDn, SA set, GroupID, 1/|group size|, Group SA domain)
    # 1/|group size|, Group SA domain will be used in evaluation
    return (result, rncp, tncp)
