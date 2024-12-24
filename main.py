import helper as h
from quad import QuadTree


def main():
    # Temporary
    frames = h.sequenceToLists("samples/seq1.gif")
    compressed = QuadTree.sequenceCompress(frames, 64)

    h.listsToSequence("test.gif", compressed, (64, 64))
    
    q = QuadTree(h.imageToList("samples/pic6.png"))
    q.searchSubspacesWithRange(7,7,8,8).show()


if __name__ == "__main__":
    main()
