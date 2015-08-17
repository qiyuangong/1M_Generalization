#!/usr/bin/env python
# coding=utf-8


import pdb
from models.numrange import NumRange
from models.gentree import GenTree
from utils.utility import cmp_str
from utils.utility import list_to_str


__DEBUG = False
QI_LEN = 10
GL_L = 0
RESULT = []
ATT_TREES = []
QI_RANGE = []


class Partition:

    """Class for Group, which is used to keep records
    Store tree node in instances.
    self.width: width of this partition on each domain
    self.middle: save the generalization result of this partition
    self.member: records in group
    self.allow: 0 donate that not allow to split, 1 donate can be split
    """

    def __init__(self, data, width, middle, allow=None):
        """
        initialize with data, width and middle
        """
        self.member = data[:]
        self.width = width[:]
        self.middle = middle[:]
        if allow is not None:
            self.allow = allow[:]
        else:
            self.allow = [1] * QI_LEN


def check_L_diversity(partition):
    """check if partition satisfy l-diversity
    return True if satisfy, False if not.
    """
    sa_dict = {}
    if isinstance(partition, Partition):
        records_set = partition.member
    else:
        records_set = partition
    num_record = len(records_set)
    for record in records_set:
        sa_value = list_to_str(record[-1])
        try:
            sa_dict[sa_value] += 1
        except KeyError:
            sa_dict[sa_value] = 1
    if len(sa_dict.keys()) < GL_L:
        return False
    for sa in sa_dict.keys():
        # if any SA value appear more than |T|/l,
        # the partition does not satisfy l-diversity
        if sa_dict[sa] > 1.0 * num_record / GL_L:
            return False
    return True


def get_normalized_width(partition, index):
    """return Normalized width of partition
    similar to NCP
    """
    width = partition.width[index]
    return width * 1.0 / QI_RANGE[index]


def choose_dimension(partition):
    """chooss dim with largest normlized Width
    """
    max_witdh = -1
    max_dim = -1
    for i in range(QI_LEN):
        if partition.allow[i] == 0:
            continue
        normWidth = get_normalized_width(partition, i)
        if normWidth > max_witdh:
            max_witdh = normWidth
            max_dim = i
    if max_witdh > 1:
        print "Error: max_witdh > 1"
        pdb.set_trace()
    return max_dim


def frequency_set(partition, dim):
    """get the frequency_set of partition on dim
    """
    frequency = {}
    for record in partition.member:
        try:
            frequency[record[dim]] += 1
        except:
            frequency[record[dim]] = 1
    return frequency


def find_median(partition, dim):
    """find the middle of the partition,
    return splitVal
    """
    frequency = frequency_set(partition, dim)
    splitVal = ''
    value_list = frequency.keys()
    value_list.sort(cmp=cmp_str)
    total = sum(frequency.values())
    middle = total / 2
    if middle < GL_L:
        print "Error: size of group less than 2*K"
        return ''
    index = 0
    split_index = 0
    for i, t in enumerate(value_list):
        index += frequency[t]
        if index >= middle:
            splitVal = t
            split_index = i
            break
    else:
        print "Error: cannot find splitVal"
    return (splitVal, split_index)


def anonymize(partition):
    """recursively partition groups until not allowable
    """
    global RESULT
    if len(partition.member) < 2 * GL_L:
        RESULT.append(partition)
        return
    allow_count = sum(partition.allow)
    pwidth = partition.width
    pmiddle = partition.middle
    # pallow = partition.allow
    for index in range(allow_count):
        dim = choose_dimension(partition)
        if dim == -1:
            print "Error: dim=-1"
            pdb.set_trace()
        if isinstance(ATT_TREES[dim], NumRange):
            # numeric attributes
            (splitVal, split_index) = find_median(partition, dim)
            if splitVal == '':
                print "Error: splitVal= null"
                pdb.set_trace()
            middle_pos = ATT_TREES[dim].dict[splitVal]
            lmiddle = pmiddle[:]
            rmiddle = pmiddle[:]
            temp = pmiddle[dim].split(',')
            low = temp[0]
            high = temp[1]
            lmiddle[dim] = low + ',' + splitVal
            rmiddle[dim] = splitVal + ',' + high
            lhs = []
            rhs = []
            for temp in partition.member:
                pos = ATT_TREES[dim].dict[temp[dim]]
                if pos <= middle_pos:
                    # lhs = [low, means]
                    lhs.append(temp)
                else:
                    # rhs = (means, high]
                    rhs.append(temp)
            lwidth = pwidth[:]
            rwidth = pwidth[:]
            lwidth[dim] = split_index
            rwidth[dim] = pwidth[dim] - split_index
            if check_L_diversity(lhs) is not True or check_L_diversity(rhs) is not True:
                partition.allow[dim] = 0
                continue
            # anonymize sub-partition
            anonymize(Partition(lhs, lwidth, lmiddle))
            anonymize(Partition(rhs, rwidth, rmiddle))
            return
        else:
            # normal attributes
            if partition.middle[dim] != '*':
                splitVal = ATT_TREES[dim][partition.middle[dim]]
            else:
                splitVal = ATT_TREES[dim]['*']
            sub_node = [t for t in splitVal.child]
            sub_partition = []
            for i in range(len(sub_node)):
                sub_partition.append([])
            for temp in partition.member:
                qid_value = temp[dim]
                for i, node in enumerate(sub_node):
                    try:
                        node.cover[qid_value]
                        sub_partition[i].append(temp)
                        break
                    except:
                        continue
            flag = True
            for p in sub_partition:
                if len(p) == 0:
                    continue
                if check_L_diversity(p) is not True:
                    flag = False
                    break
            if flag:
                for i, p in enumerate(sub_partition):
                    if len(p) == 0:
                        continue
                    wtemp = pwidth[:]
                    mtemp = pmiddle[:]
                    wtemp[dim] = sub_node[i].support
                    mtemp[dim] = sub_node[i].value
                    anonymize(Partition(p, wtemp, mtemp))
                return
            else:
                partition.allow[dim] = 0
                continue
    RESULT.append(partition)


def init(att_trees, data, L):
    """
    resset global variables
    """
    global GL_L, RESULT, QI_LEN, ATT_TREES, QI_RANGE
    ATT_TREES = att_trees
    QI_LEN = len(data[0]) - 1
    GL_L = L
    RESULT = []
    QI_RANGE = []


def mondrian_l_diversity(att_trees, data, L):
    """
    Mondrian for l-diversity.
    This fuction support both numeric values and categoric values.
    For numeric values, each iterator is a mean split.
    For categoric values, each iterator is a split on GH.
    The final result is returned in 2-dimensional list.
    """
    init(att_trees, data, L)
    middle = []
    result = []
    for i in range(QI_LEN):
        if isinstance(ATT_TREES[i], NumRange):
            QI_RANGE.append(ATT_TREES[i].range)
            middle.append(ATT_TREES[i].value)
        else:
            QI_RANGE.append(ATT_TREES[i]['*'].support)
            middle.append('*')
    whole_partition = Partition(data, QI_RANGE[:], middle)
    anonymize(whole_partition)
    ncp = 0.0
    for p in RESULT:
        rncp = 0.0
        for i in range(QI_LEN):
            rncp += get_normalized_width(p, i)
        temp = p.middle
        for i in range(len(p.member)):
            result.append(temp[:])
        rncp *= len(p.member)
        ncp += rncp
    ncp /= QI_LEN
    ncp /= len(data)
    ncp *= 100
    if __DEBUG:
        print "L=%d" % L
        print "size of partitions"
        print len(RESULT)
        # print [len(t.member) for t in RESULT]
        print "NCP = %.2f %%" % ncp
        # pdb.set_trace()
    return (result, ncp)
