import helper as h
from quad import QuadTree
from rect import Rect


def main():
    # Temporary
    l1 = h.imageToArray("samples/pic2.png")
    q = QuadTree(l1)
    l2, size = q.mask(Rect(1, 1, 2, 2))

    h.arrayToImage(l2, size).save("test.png")


if __name__ == "__main__":
    main()
