import unittest
from bayes.parameters import *


class TestParameters(unittest.TestCase):
    def setUp(self):
        self.p = ModelParameters()
        self.p.define("pA", 0.0)
        self.p.define("pB", 0.0)

    def test_parameter(self):
        self.p.update(["pA"], [42.0])
        self.assertEqual(self.p["pA"], 42.0)
        self.assertEqual(self.p["pB"], 0.0)

    def test_concat(self):
        p1 = ModelParameters()
        p1.define("A", 17)

        p1 += self.p
        self.assertEqual(p1["A"], 17)
        self.assertEqual(p1["pA"], 0.0)
        self.assertEqual(p1["pB"], 0.0)

    def test_has(self):
        self.assertTrue(self.p.has("pA"))
        self.assertFalse(self.p.has("pC"))

    def test_copy(self):
        import copy

        self.assertEqual(self.p["pA"], 0.0)
        copy_p = copy.deepcopy(self.p)
        copy_p["pA"] = 42.0
        self.assertEqual(copy_p["pA"], 42)
        self.assertEqual(self.p["pA"], 0.0)

    def test_define(self):
        self.assertRaises(Exception, self.p.__setitem__, "new_key", 0.2)


class TestSingleModel(unittest.TestCase):
    def setUp(self):
        self.p = ModelParameters()
        self.p.define("pA", 0.0)
        self.p.define("pB", 0.0)
        self.l = JointLatent()
        self.l.add_model_parameters(self.p)

    def test_joint_list(self):
        self.l.add("pA")
        updated = self.l.update([42], return_copy=False)
        self.assertEqual(self.p["pA"], 42.0)
        self.assertEqual(self.p["pB"], 0.0)

        # not allowed to set latent, if you use these prior classes
        self.assertRaises(Exception, UncorrelatedNormalPrior, self.l)

    def test_prior(self):
        prior = UncorrelatedNormalPrior(self.l)
        prior.add("pA", mean=0, sd=2)
        prior.add("pB", mean=1, sd=4)

        mvn = prior.to_MVN()
        self.assertAlmostEqual(mvn.mean[0], 0.0)
        self.assertAlmostEqual(mvn.std_diag[0], 2.0)

        self.assertAlmostEqual(mvn.mean[1], 1.0)
        self.assertAlmostEqual(mvn.std_diag[1], 4.0)


class TestJointLatent(unittest.TestCase):
    def setUp(self):
        self.pA = ModelParameters()
        self.pA.define("only_in_A", 0)
        self.pA.define("shared", 2)
        self.keyA = "A"

        self.pB = ModelParameters()
        self.pB.define("only_in_B", 1)
        self.pB.define("shared", 2)
        self.keyB = "B"

        self.l = JointLatent()
        self.l.add_model_parameters(self.pA, self.keyA)
        self.l.add_model_parameters(self.pB, self.keyB)

    def test_add(self):
        l, keyA, keyB = self.l, self.keyA, self.keyB
        index = l.add("only_in_A", keyA)
        self.assertEqual(index, 0)
        self.assertRaises(Exception, self.l.add, "only_in_A", self.keyA)

        index = l.add("shared", keyB)
        self.assertEqual(index, 1)

        self.assertTrue(l.exists("shared", keyB))
        self.assertRaises(Exception, l.add_shared, index, "shared", keyB)
        l.add_shared(index, "shared", keyA)

        self.assertTrue(l.exists("shared", keyA))

        self.assertListEqual(l.indices_of(keyA), [0, 1])
        self.assertListEqual(l.indices_of(keyB), [1])

        updated_prm = l.update([42, 17])
        self.assertEqual(updated_prm[keyA]["only_in_A"], 42)
        self.assertEqual(updated_prm[keyA]["shared"], 17)
        self.assertEqual(updated_prm[keyB]["shared"], 17)


if __name__ == "__main__":
    unittest.main()
