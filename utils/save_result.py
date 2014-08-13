#!/usr/bin/env python
#coding=utf-8

# store

import socket
import pickle
from datetime import datetime
from utils.ftp_upload import ftp_upload

def save_to_file(result, flag=0):
    """save results to files 
    if flag=0, then pickle (att_trees, data, result, K, L)) to file
    else, save result to file
    """
    print "Saving result...."
    hostname = socket.gethostname()
    # file_tail = datetime.now().strftime('%Y-%m-%d-%H') + '.txt'
    file_tail = "Size%dK%dL%d" % (len(result[1]), result[3], result[4])
    file_tail = file_tail + '.txt'
    file_path = 'output/'
    file_name = hostname + '-' + file_tail
    if flag:
        # write file in text
        # only restore result
        file_result = open(file_path + file_name,'w')
        for record in result[2]:
            line = ';'.join(record) + '\n'
            file_result.write(line)
    else:
        # write file using pickle
        file_result = open(file_path + file_name,'wb')
        pickle.dump(result, file_result)
    file_result.close()
    # try:
    #     ftp_upload(file_name, file_path)
    # except:
    #     print "Upload Fail!"
    print "Save Complete!"
