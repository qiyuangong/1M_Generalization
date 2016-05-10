#!/usr/bin/env python
# coding=utf-8
from Separation_Gen import Separation_Gen
from utils.make_tree import gen_gh_trees
from utils.read_informs_data import read_data as read_informs
from utils.read_informs_data import read_tree as read_informs_tree
from utils.read_youtube_data import read_data as read_youtube
from utils.read_youtube_data import read_tree as read_youtube_tree
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


def get_result_kl(att_trees, data):
    "change k and l, while fixing dataset"
    print "size of dataset %d" % len(data)
    data_back = copy.deepcopy(data)
    all_qid_ncp = []
    all_sa_ncp = []
    all_rtime = []
    # k_range = range(5, 55, 5):
    k_range = [2, 5, 10, 25, 50, 100]
    l_range = range(2 , 16)
    for k in k_range:
        print '#' * 30
        for l in l_range:
            print '#' * 10
            print "k=%d" % k
            print "l=%d" % l
            result, eval_result = Separation_Gen(att_trees, data, k, l)
            data = copy.deepcopy(data_back)
            print "QID-NCP %0.2f" % eval_result[0] + "%"
            print "SA-NCP %0.2f" % eval_result[1] + "%"
            print "Running time %0.2f" % eval_result[2] + "seconds"
            all_qid_ncp.append(round(eval_result[0], 2))
            all_sa_ncp.append(round(eval_result[1], 2))
            all_rtime.append(round(eval_result[2], 2))
    print '#' * 30
    print "K range", k_range
    print "L range", l_range
    print "All QID-NCP", all_qid_ncp
    print "All SA-NCP", all_sa_ncp
    print "All Running time", all_rtime


def get_result_k(att_trees, data, l=DEFAULT_L):
    "change k, while fixing l"
    print "L=%d" % l
    print "size of dataset %d" % len(data)
    data_back = copy.deepcopy(data)
    all_qid_ncp = []
    all_sa_ncp = []
    all_rtime = []
    # k_range = range(5, 55, 5):
    k_range = [2, 5, 10, 25, 50, 100]
    for k in k_range:
        print '#' * 30
        print "k=%d" % k
        result, eval_result = Separation_Gen(att_trees, data, k, l)
        data = copy.deepcopy(data_back)
        print "QID-NCP %0.2f" % eval_result[0] + "%"
        print "SA-NCP %0.2f" % eval_result[1] + "%"
        print "Running time %0.2f" % eval_result[2] + "seconds"
        all_qid_ncp.append(round(eval_result[0], 2))
        all_sa_ncp.append(round(eval_result[1], 2))
        all_rtime.append(round(eval_result[2], 2))
    print '#' * 30
    print "K range", k_range
    print "All QID-NCP", all_qid_ncp
    print "All SA-NCP", all_sa_ncp
    print "All Running time", all_rtime


def get_result_l(att_trees, data, k=DEFAULT_K):
    "change l, while fixing k"
    print "K=%d" % k
    print "size of dataset %d" % len(data)
    data_back = copy.deepcopy(data)
    all_qid_ncp = []
    all_sa_ncp = []
    all_rtime = []
    l_range = range(2 , 16)
    for l in l_range:
        print '#' * 30
        print "l=%d" % l
        result, eval_result = Separation_Gen(att_trees, data, k, l)
        data = copy.deepcopy(data_back)
        print "QID-NCP %0.2f" % eval_result[0] + "%"
        print "SA-NCP %0.2f" % eval_result[1] + "%"
        print "Running time %0.2f" % eval_result[2] + "seconds"
        all_qid_ncp.append(round(eval_result[0], 2))
        all_sa_ncp.append(round(eval_result[1], 2))
        all_rtime.append(round(eval_result[2], 2))
    print '#' * 30
    print "L range", l_range
    print "All QID-NCP", all_qid_ncp
    print "All SA-NCP", all_sa_ncp
    print "All Running time", all_rtime


def get_result_dataset(att_trees, data, k=DEFAULT_K, l=DEFAULT_L, n=10):
    "fix k and l, while changign dataset size"
    data_back = copy.deepcopy(data)
    length = len(data_back)
    print "K=%d" % k
    print "L=%d" % l
    joint = 5000
    datasets = []
    check_time = length / joint
    if length % joint == 0:
        check_time -= 1
    for i in range(check_time):
        datasets.append(joint * (i + 1))
    # datasets.append(length)
    all_qid_ncp = []
    all_sa_ncp = []
    all_rtime = []
    for pos in datasets:
        qid_ncp = sa_ncp = rtime = 0
        print '#' * 30
        print "size of dataset %d" % pos
        for j in range(n):
            temp = random.sample(data, pos)
            result, eval_result = Separation_Gen(att_trees, temp, k, l)
            qid_ncp += eval_result[0]
            sa_ncp += eval_result[1]
            rtime += eval_result[2]
            data = copy.deepcopy(data_back)
        qid_ncp /= n
        sa_ncp /= n
        rtime /= n
        all_qid_ncp.append(round(qid_ncp, 2))
        all_sa_ncp.append(round(sa_ncp, 2))
        all_rtime.append(round(rtime, 2))
        print "Average QID-NCP %0.2f" % qid_ncp + "%"
        print "Average SA-NCP %0.2f" % sa_ncp + "%"
        print "Running time %0.2f" % rtime + "seconds"
    print '#' * 30
    print "Size of datasets", datasets
    print "All QID-NCP", all_qid_ncp
    print "All SA-NCP", all_sa_ncp
    print "All Running time", all_rtime



if __name__ == '__main__':
    FLAG = ''
    try:
        print sys.argv
        DATA_SELECT = sys.argv[1]
        FLAG = sys.argv[2]
    except:
        DATA_SELECT = 'i'
    # read record
    print '*' * 30
    # read dataset
    if DATA_SELECT == 'i':
        print "INFORMS data"
        DATA = read_informs()
        # gen_gh_trees(DATA_SELECT)
        ATT_TREES = read_informs_tree()
    elif DATA_SELECT == 'y':
        print "Youtube data"
        DATA = read_youtube()
        # gen_gh_trees(DATA_SELECT)
        ATT_TREES = read_youtube_tree()
    else:
        print "INFORMS data"
        DATA = read_informs()
        # gen_gh_trees(DATA_SELECT)
        ATT_TREES = read_informs_tree()
    # Separation_Gen need only GH for transaction
    if FLAG == 'k':
        get_result_k(ATT_TREES, DATA)
    elif FLAG == 'l':
        get_result_l(ATT_TREES, DATA)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREES, DATA)
    elif FLAG == 'kl':
        get_result_kl(ATT_TREES, DATA)
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
