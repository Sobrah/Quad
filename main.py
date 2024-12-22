import helper as h
from quad import QuadTree


def main():
    # Temporary
    q = QuadTree(h.csvToList("samples/img1.csv"))
    q.searchSubspacesWithRange(10,10,70,70)


if __name__ == "__main__":
    main()
