from partition_for_transaction import partition
from mondrian import mondrian
import time
import pdb


_DEBUG = True
gl_att_tree = []
gl_data = []

def Separation_Gen(att_tree, data, K=10, L=5):
    """Using partition_for_transaction to anonymize SA (transaction) partition, 
    while applying anatomy to separate QID and SA
    """
    global gl_att_tree, gl_data
    gl_att_tree = att_tree
    gl_data = data
    start_time = time.time()
    print "size of dataset %d" % len(data)
    result = []
    trans = [t[-1] for t in data]
    trans_set = partition(att_tree, trans, K)
    partition_data = []
    for ttemp in trans_set:
        (index_list, tran_value) = ttemp
        for t in index_list:
            gl_data[t][-1] = tran_value[:]
            partition_data.append(gl_data[t][:])
    print "Begin Mondrian"
    print "L=%d" % L
    result = mondrian(partition_data, L)
    print("--- %s seconds ---" % (time.time()-start_time))
    # transform data format (QID1,.., QIDn, SA set, GroupID, 1/|group size|, Group SA domain)
    # 1/|group size|, Group SA domain will be used in evaluation
    return result