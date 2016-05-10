#!/usr/bin/env python
# coding=utf-8

import pickle
from utils.utility import cmp_str
from make_tree import pickle_static_income
from models.gentree import GenTree
from models.numrange import NumRange
import pdb

__DEBUG = False
ATT_NAMES = ['video_ID', 'uploader', 'age', 'category', 'length',
             'views', 'rate', 'ratings', 'comments', 'related_ID']
QI_INDEX = [2, 3, 4, 5, 6, 7, 8]
IS_CAT = [False, True, True, True, True, True, True, True]
SA_INDEX = 9

def read_data():
    """
    read youtube dataset
    """
    QI_num = len(QI_INDEX)
    data = []
    numeric_dict = []
    for i in range(QI_num):
        numeric_dict.append(dict())
    # oder categorical attributes in intuitive order
    # here, we use the appear number
    data_file = open('data/youtube.txt', 'rU')
    for line in data_file:
        line = line.strip()
        # remove empty and incomplete lines
        # only 30162 records will be kept
        if len(line) == 0:
            continue
        line = line.replace(' ', '')
        temp = line.split('\t')
        ltemp = []
        if len(temp) < 9:
            # remove line only have single id
            continue
        for i in range(QI_num):
            index = QI_INDEX[i]
            if IS_CAT[i] is False:
                try:
                    numeric_dict[i][temp[index]] += 1
                except KeyError:
                    numeric_dict[i][temp[index]] = 1
            ltemp.append(temp[index])
        # add all related id as a list
        ltemp.append(temp[9:])
        data.append(ltemp)
    # pickle numeric attributes
    for i in range(QI_num):
        if IS_CAT[i] is False:
            static_file = open('data/youtube_' + ATT_NAMES[QI_INDEX[i]] + '_static.pickle', 'wb')
            sort_value = list(numeric_dict[i].keys())
            sort_value.sort(cmp=cmp_str)
            pickle.dump((numeric_dict[i], sort_value), static_file)
            static_file.close()
    return data


def read_tree():
    """read tree from data/tree_*.txt, store them in att_tree
    """
    att_names = []
    att_trees = []
    for t in QI_INDEX:
        att_names.append(ATT_NAMES[t])
    att_names.append('related_ID')
    for i in range(len(att_names)):
        if IS_CAT[i]:
            att_trees.append(read_tree_file(att_names[i]))
        else:
            att_trees.append(pickle_static_income(QI_INDEX[i]))
    return att_trees


def read_tree_file(treename):
    """read tree data from treename
    """
    leaf_to_path = {}
    att_tree = {}
    prefix = 'data/informs_'
    postfix = ".txt"
    treefile = open(prefix + treename + postfix, 'rU')
    att_tree['*'] = GenTree('*')
    if __DEBUG:
        print "Reading Tree" + treename
    for line in treefile:
        # delete \n
        if len(line) <= 1:
            break
        line = line.strip()
        temp = line.split(';')
        # copy temp
        temp.reverse()
        for i, t in enumerate(temp):
            isleaf = False
            if i == len(temp) - 1:
                isleaf = True
            if t not in att_tree:
                # always satisfy
                att_tree[t] = GenTree(t, att_tree[temp[i - 1]], isleaf)
    if __DEBUG:
        print "Nodes No. = %d" % att_tree['*'].support
    treefile.close()
    return att_tree


def read_pickle_file(att_name):
    """
    read pickle file for numeric attributes
    return numrange object
    """
    with open('data/youtube_' + att_name + '_static.pickle', 'rb') as static_file:
        (numeric_dict, sort_value) = pickle.load(static_file)
        result = NumRange(sort_value, numeric_dict)
        return result