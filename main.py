import helper as h
from quad import QuadTree
from rect import Rect


def main():
    # Temporary
    l1 = h.csvToList("samples/img4.csv")

    q = QuadTree(l1)
    q.compress(256)
    l2 = q.export()

    h.listToImage("test.png", l2)


if __name__ == "__main__":
    main()
