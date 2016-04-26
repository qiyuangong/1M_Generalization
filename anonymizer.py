#!/usr/bin/env python
# coding=utf-8
from Separation_Gen import Separation_Gen
from utils.make_tree import gen_gh_trees
from utils.read_data import read_data, read_tree
import random
import sys
import copy
import pdb
import cProfile


__DEBUG = False
# set k=10, l=5 as default!
DEFAULT_K = 10
DEFAULT_L = 5


def get_result_one(att_trees, data, k=DEFAULT_K, l=DEFAULT_L):
    "fix k=10, l=5"
    print "K=%d" % k
    print "L=%d" % l
    print "size of dataset %d" % len(data)
    data_back = copy.deepcopy(data)
    result, eval_result = Separation_Gen(att_trees, data, k, l)
    data = copy.deepcopy(data_back)
    print "QID-NCP %0.2f" % eval_result[0] + "%"
    print "SA-NCP %0.2f" % eval_result[1] + "%"
    print "Running time %0.2f" % eval_result[2] + "seconds"
    # save_to_file((att_trees, data, result, k, l))


def get_result_k(att_trees, data, l=DEFAULT_L):
    "change k, while fixing l"
    print "L=%d" % l
    print "size of dataset %d" % len(data)
    data_back = copy.deepcopy(data)
    # for k in range(5, 55, 5):
    for k in [2, 5, 10, 25, 50, 100]:
        print '#' * 30
        print "k=%d" % k
        result, eval_result = Separation_Gen(att_trees, data, k, l)
        data = copy.deepcopy(data_back)
        print "QID-NCP %0.2f" % eval_result[0] + "%"
        print "SA-NCP %0.2f" % eval_result[1] + "%"
        print "Running time %0.2f" % eval_result[2] + "seconds"
        # save_to_file((att_trees, data, result, k, l))


def get_result_l(att_trees, data, k=DEFAULT_K):
    "change l, while fixing k"
    print "K=%d" % k
    print "size of dataset %d" % len(data)
    data_back = copy.deepcopy(data)
    for l in range(2, 16):
        print '#' * 30
        print "l=%d" % l
        result, eval_result = Separation_Gen(att_trees, data, k, l)
        data = copy.deepcopy(data_back)
        print "QID-NCP %0.2f" % eval_result[0] + "%"
        print "SA-NCP %0.2f" % eval_result[1] + "%"
        print "Running time %0.2f" % eval_result[2] + "seconds"
        # save_to_file((att_trees, data, result, k, l))


def get_result_dataset(att_trees, data, k=DEFAULT_K, l=DEFAULT_L, n=10):
    "fix k and l, while changign dataset size"
    data_back = copy.deepcopy(data)
    length = len(data_back)
    print "K=%d" % k
    print "L=%d" % l
    joint = 5000
    h = length / joint
    if length % joint == 0:
        h += 1
    for i in range(1, h + 1):
        pos = i * joint
        all_qid_ncp = all_sa_ncp = all_rtime = 0
        if pos > length:
            continue
        print '#' * 30
        print "size of dataset %d" % pos
        for j in range(n):
            temp = random.sample(data, pos)
            result, eval_result = Separation_Gen(att_trees, temp, k, l)
            all_qid_ncp += eval_result[0]
            all_sa_ncp += eval_result[1]
            all_rtime += eval_result[2]
            data = copy.deepcopy(data_back)
            # save_to_file((att_trees, temp, result, k, l))
        all_qid_ncp /= n
        all_sa_ncp /= n
        all_rtime /= n
        print "Average QID-NCP %0.2f" % all_qid_ncp + "%"
        print "Average SA-NCP %0.2f" % all_sa_ncp + "%"
        print "Running time %0.2f" % all_rtime + "seconds"
        print '#' * 30


if __name__ == '__main__':
    FLAG = ''
    try:
        FLAG = sys.argv[1]
    except:
        pass
    # read record
    print '*' * 30
    # make generalization hierarchies
    gen_gh_trees()
    # read gentree tax
    ATT_TREES = read_tree()
    # read record
    DATA = read_data()
    # Separation_Gen need only GH for transaction
    if FLAG == 'k':
        get_result_k(ATT_TREES, DATA)
    elif FLAG == 'l':
        get_result_l(ATT_TREES, DATA)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREES, DATA)
    elif FLAG == '':
        if __DEBUG:
            cProfile.run('get_result_one(ATT_TREE, DATA)')
        else:
            get_result_one(ATT_TREES, DATA)
    else:
        try:
            INPUT_K = int(FLAG)
            if __DEBUG:
                cProfile.run('get_result_one(ATT_TREE, DATA, INPUT_K)')
            else:
                get_result_one(ATT_TREES, DATA, INPUT_K)
        except ValueError:
            print "Usage: python anonymizer [k | l | data]"
            print "k: varying k"
            print "l: varying l"
            print "data: varying size of dataset"
            print "example: python anonymizer 10"
            print "example: python anonymizer k"
    # anonymized dataset is stored in result
    print "Finish 1M_Generalization!!"
