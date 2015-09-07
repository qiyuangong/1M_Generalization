import unittest
import pdb
from models.gentree import GenTree
from Separation_Gen import Separation_Gen

# Build a GenTree object
ATT_TREE = {}


def init_tree():
    global ATT_TREE
    ATT_TREE = {}
    root = GenTree('*')
    ATT_TREE['*'] = root
    lt = GenTree('A', root)
    ATT_TREE['A'] = lt
    ATT_TREE['a1'] = GenTree('a1', lt, True)
    ATT_TREE['a2'] = GenTree('a2', lt, True)
    rt = GenTree('B', root)
    ATT_TREE['B'] = rt
    ATT_TREE['b1'] = GenTree('b1', rt, True)
    ATT_TREE['b2'] = GenTree('b2', rt, True)


class test_1M_Generalization(unittest.TestCase):

    def test_1M_Generalization_AA_case(self):
        init_tree()
        att_trees = [ATT_TREE, ATT_TREE]
        data = [['a1', ['a1']],
                ['b2', ['a1', 'a2']],
                ['b1', ['b1', 'b2']],
                ['b2', ['b1', 'b2']],
                ['b1', ['a1', 'a2', 'b2']],
                ['b2', ['a1', 'a2', 'b2']],
                ['a1', ['a1', 'a2', 'b1', 'b2']]]
        result, eval_result = Separation_Gen(att_trees, data, 2, 2)
        self.assertTrue(abs(eval_result[0] - 0) <= 0.001)
        self.assertTrue(abs(eval_result[1] - 350.0 / 17) <= 0.001)

    def test_1M_Generalization__parititon_case(self):
        init_tree()
        att_trees = [ATT_TREE, ATT_TREE]
        data = [['a1', ['a1', 'b1', 'b2']],
                ['a1', ['a2', 'b1']],
                ['a2', ['a2', 'b1', 'b2']],
                ['a2', ['a1', 'a2', 'b2']]]
        result, eval_result = Separation_Gen(att_trees, data, 2, 2)
        self.assertTrue(abs(eval_result[0] - 0) <= 0.001)
        self.assertTrue(abs(eval_result[1] - 350.0 / 11) <= 0.001)

if __name__ == '__main__':
    unittest.main()
