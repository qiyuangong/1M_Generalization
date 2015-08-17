1M_Generalization
=================

1:M dataset denotes dataset allowing mulitple records of the same user. It is more general than microdata, which allows one record for one user. To simplify the dataset, I transformed 1:M dataset to relational and transaction dataset, in which mulitple records of the same user are merge to single record. This single record is consitute of relational part (treat as QID) and transaction part (treat as SA). 

1M_Generalization is a simple anonymization algorithm for 1:M dataset. It contains two sub-algorithms: Mondrian (for relational part) and Partition (transaction part). Both of them are straight forward, and can be repalced by more powerful algorithm with limtied modification.


## ATTENTION
This project is the evaluation part of my new paper (not published). So don't use it without my permission.