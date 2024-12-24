import helper as h
from quad import QuadTree


def main():
    # Temporary
    frames = h.sequenceToLists("samples/seq1.gif")
    compressed = QuadTree.sequenceCompress(frames, 64)

    h.listsToSequence("test.gif", compressed, (64, 64))


if __name__ == "__main__":
    main()
