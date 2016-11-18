1M_Generalization
=================

1:M dataset denotes dataset allowing mulitple records of the same user. It is more general than microdata, which allows one record for one user. To simplify the dataset, I transformed 1:M dataset to relational and transaction dataset, in which mulitple records of the same user are merge to single record. This single record is consitute of relational part (treat as QID) and transaction part (treat as SA). 

1M_Generalization[(KBS 2017)](http://dx.doi.org/10.1016/j.knosys.2016.10.012) is a simple anonymization algorithm for 1:M dataset. It contains two sub-algorithms: Mondrian (for relational part) and Partition (transaction part). Both of them are straight forward, and can be repalced by more powerful algorithm with limtied modification.

**Publication:**

Q. Gong, J. Luo, M. Yang, W. Ni, and X.-B. Li, Anonymizing 1:M Microdata with High Utility, Knowledge-Based Systems, vol. 115, pp. 15–26, 2017.


## ATTENTION
This project is the evaluation part of my new paper (not published). So don't use it without my permission.


### Usage:
My Implementation is based on Python 2.7 (not Python 3.0). Please make sure your Python environment is collect installed. You can run Mondrian in following steps:

1) Download (or clone) the whole project.

2) Run "anonymized.py" in root dir with CLI.

    # Usage: python anonymizer [i | y] [k | l | data]
    # I:INFORMS, y:youtube
    # k: multiple experiments by varying k
    # l: multiple experiments by varying l
    # data: multiple experiments by varying size of dataset

	# run Mondrian with default K(K=10)
	python anonymizer.py

	# run Mondrian with adult data, K=20
	python anonymized.py a 20
	