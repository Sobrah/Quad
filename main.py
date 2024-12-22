import helper as h
from quad import QuadTree


def main():
    # Temporary
    q = QuadTree(h.imageToList("samples/pic2.png"))
    q.searchSubspacesWithRange(1,1,3,3)
    q.mask(1,1,3,3)


if __name__ == "__main__":
    main()
