"""Public smoke tests. Run from repository root:
python -m unittest discover -s benchmarks/scheduled-model-20261025 -p public_tests.py -v
"""
from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOLUTIONS = ROOT / "results" / "scheduled-model-20261025"

def load(problem):
    f = SOLUTIONS / (problem + ".py")
    if not f.exists():
        raise AssertionError(f"Missing submitted solution: {f}")
    spec = importlib.util.spec_from_file_location("candidate_" + problem, f)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class TestP01(unittest.TestCase):
    def test_example(self):
        f = load("P01").merge_windows
        a = [
            dict(event_id="e1", tenant="x", start=0, end=5),
            dict(event_id="e2", tenant="x", start=7, end=9),
            dict(event_id="e3", tenant="x", start=9, end=10),
            dict(event_id="e4", tenant="y", start=1, end=3),
            dict(event_id="e2", tenant="x", start=7, end=9),
        ]
        self.assertEqual(f(a, 2), [
            dict(tenant="x",start=0,end=10,count=3),
            dict(tenant="y",start=1,end=3,count=1)])
    def test_zero_gap_and_negative(self):
        f = load("P01").merge_windows
        self.assertEqual(f([
            dict(event_id="a", tenant="t",start=-4,end=-1),
            dict(event_id="b", tenant="t",start=-1,end=0),
            dict(event_id="c", tenant="t",start=1,end=2)],0),
            [dict(tenant="t",start=-4,end=0,count=2),
             dict(tenant="t",start=1,end=2,count=1)])
    def test_empty(self):
        self.assertEqual(load("P01").merge_windows([], 0), [])
    def test_invalid(self):
        f = load("P01").merge_windows
        a = dict(event_id="a",tenant="x",start=0,end=2)
        with self.assertRaises(ValueError):
            f([a, dict(event_id="a",tenant="x",start=0,end=3)],0)
        with self.assertRaises(ValueError):
            f([dict(event_id="a",tenant="x",start=True,end=2)],0)
        with self.assertRaises(ValueError):
            f([a], -1)

class TestP02(unittest.TestCase):
    def test_example(self):
        f = load("P02").replay
        a = [
            dict(event_id="e1",order_id="o1",revision=1,kind="SET",amount=50),
            dict(event_id="e2",order_id="o1",revision=3,kind="DELETE"),
            dict(event_id="e3",order_id="o1",revision=2,kind="SET",amount=70),
            dict(event_id="e4",order_id="o2",revision=1,kind="SET",amount=20),
            dict(event_id="e4",order_id="o2",revision=1,kind="SET",amount=20)]
        self.assertEqual(f(a),dict(active=[dict(order_id="o2",amount=20,revision=1)],
                                  deleted=[dict(order_id="o1",revision=3)],total_amount=20))
    def test_resurrection(self):
        f=load("P02").replay
        self.assertEqual(f([dict(event_id="b",order_id="x",revision=2,kind="SET",amount=0),
                            dict(event_id="a",order_id="x",revision=1,kind="DELETE")]),
                         dict(active=[dict(order_id="x",amount=0,revision=2)],
                              deleted=[],total_amount=0))
    def test_empty(self):
        self.assertEqual(load("P02").replay([]),dict(active=[],deleted=[],total_amount=0))
    def test_invalid_revision(self):
        f=load("P02").replay
        with self.assertRaises(ValueError):
            f([dict(event_id="a",order_id="o",revision=1,kind="DELETE"),
               dict(event_id="b",order_id="o",revision=1,kind="DELETE")])
        with self.assertRaises(ValueError):
            f([dict(event_id="a",order_id="o",revision=1,kind="DELETE",amount=None)])
        with self.assertRaises(ValueError):
            f([dict(event_id="a",order_id="o",revision=True,kind="DELETE")])

class TestP03(unittest.TestCase):
    def test_example(self):
        f=load("P03").schedule
        jobs=[dict(id="a",depends=[],cost=2,priority=5),
              dict(id="b",depends=[],cost=2,priority=4),
              dict(id="c",depends=["a"],cost=1,priority=10),
              dict(id="d",depends=[],cost=1,priority=3)]
        self.assertEqual(f(jobs,[],3),
                         dict(waves=[dict(job_ids=["a","d"],load=3),
                                     dict(job_ids=["c","b"],load=3)],total_waves=2))
    def test_with_completed(self):
        f=load("P03").schedule
        self.assertEqual(f([dict(id="a",depends=[],cost=2,priority=0),
                            dict(id="b",depends=["a"],cost=1,priority=0)],["a"],2),
                         dict(waves=[dict(job_ids=["b"],load=1)],total_waves=1))
    def test_empty(self):
        self.assertEqual(load("P03").schedule([],[],3),dict(waves=[],total_waves=0))
    def test_cycle_even_if_completed(self):
        f=load("P03").schedule
        jobs=[dict(id="a",depends=["b"],cost=1,priority=0),
              dict(id="b",depends=["a"],cost=1,priority=0)]
        with self.assertRaises(ValueError):
            f(jobs,["a","b"],2)
        with self.assertRaises(ValueError):
            f([dict(id="x",depends=["missing"],cost=1,priority=0)],[],2)

class TestP04(unittest.TestCase):
    def test_example(self):
        f=load("P04").reconcile_versions
        a=[dict(event_id="u1",key="k",clock={"A":1},value="a",timestamp=10),
           dict(event_id="u2",key="k",clock={"B":1},value="b",timestamp=11),
           dict(event_id="u3",key="k",clock={"A":2},value="c",timestamp=9),
           dict(event_id="u4",key="z",clock={"A":1,"B":1},value=None,timestamp=3)]
        self.assertEqual(f(a),[
            dict(key="k",winner_id="u2",value="b",conflict_ids=["u2","u3"],superseded_ids=["u1"]),
            dict(key="z",winner_id="u4",value=None,conflict_ids=[],superseded_ids=[])])
    def test_equal_clock_is_conflict(self):
        f=load("P04").reconcile_versions
        a=[dict(event_id="z",key="k",clock={"A":0},value=None,timestamp=1),
           dict(event_id="a",key="k",clock={},value="old",timestamp=1)]
        self.assertEqual(f(a),[
            dict(key="k",winner_id="z",value=None,conflict_ids=["a","z"],superseded_ids=[])])
    def test_empty(self):
        self.assertEqual(load("P04").reconcile_versions([]),[])
    def test_invalid_duplicate(self):
        f=load("P04").reconcile_versions
        with self.assertRaises(ValueError):
            f([dict(event_id="a",key="k",clock={},value="x",timestamp=1),
               dict(event_id="a",key="k",clock={},value="y",timestamp=1)])
        with self.assertRaises(ValueError):
            f([dict(event_id="a",key="k",clock={"A":True},value=None,timestamp=1)])

if __name__ == "__main__":
    unittest.main()
