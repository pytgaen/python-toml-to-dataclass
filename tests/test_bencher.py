# content of test_class.py

import time

from elapsekeeper import ElapseKeeper


class TestB:
    def test_one(self):
        b = ElapseKeeper()
        b.start()
        b.start("by_turn", "turn 1")
        time.sleep(3)
        b.turn("by_turn", "turn 1")
        time.sleep(1)
        b.stop("by_turn")
        b.stop()
        summ = (b.summary())
        print(summ)
        dett = (b.details())
        print(dett)
        assert False
