#!/usr/bin/env python
# coding=utf-8


import pdb
from models.numrange import NumRange
from models.gentree import GenTree


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


def list_to_str(value_list, cmpfun=cmp, sep=';'):
    """covert sorted str list (sorted by cmpfun) to str
    value (splited by sep). This fuction is value safe, which means
    value_list will not be changed.
    """
    temp = value_list[:]
    temp.sort(cmp=cmpfun)
    return sep.join(temp)


def check_L_diversity(partition):
    """check if partition satisfy l-diversity
    """
    sa_dict = {}
    if isinstance(partition, Partition):
        ltemp = partition.member
    else:
        ltemp = partition
    for temp in ltemp:
        stemp = list_to_str(temp[-1])
        try:
            sa_dict[stemp] += 1
        except:
            sa_dict[stemp] = 1
            if len(sa_dict) >= GL_L:
                return True
    return False


def cmp_str(element1, element2):
    """compare number in str format correctley
    """
    return cmp(int(element1), int(element2))


def getNormalizedWidth(partition, index):
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
        normWidth = getNormalizedWidth(partition, i)
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


def find_median(frequency):
    """find the middle of the partition,
    return splitVal
    """
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
            frequency = frequency_set(partition, dim)
            (splitVal, split_index) = find_median(frequency)
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


def mondrian_l_diversity(att_trees, data, L):
    """
    """
    global GL_L, RESULT, QI_LEN, ATT_TREES, QI_RANGE
    ATT_TREES = att_trees
    middle = []
    QI_LEN = len(data[0]) - 1
    GL_L = L
    RESULT = []
    result = []
    QI_RANGE = []
    for i in range(QI_LEN):
        if isinstance(ATT_TREES[i], NumRange):
            QI_RANGE.append(ATT_TREES[i].range)
            middle.append(ATT_TREES[i].value)
        else:
            QI_RANGE.append(ATT_TREES[i]['*'].support)
            middle.append(ATT_TREES[i]['*'].value)
    partition = Partition(data, QI_RANGE[:], middle)
    anonymize(partition)
    ncp = 0.0
    for p in RESULT:
        rncp = 0.0
        for i in range(QI_LEN):
            rncp += getNormalizedWidth(p, i)
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
