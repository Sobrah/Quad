import helper as h
from quad import QuadTree
from rect import Rect


def main():
    # Temporary
    l1 = h.imageToList("samples/pic2.png")
    q = QuadTree(l1)
    l2, size = (q.mask(Rect(1, 1, 2, 2)), (4, 4))

    h.listToImage(l2, size).save("test.png")


if __name__ == "__main__":
    main()
