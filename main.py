import helper
from quad import QuadTree
from rect import Rect


def main():
    
    match input("Level: "):
        
        # LV.1: GRAYSCALE with png
        case '1':
            l = helper.imageToList("samples/pic5.png")
            q = QuadTree(l)
            
            # treeDepth
            print(f"TREE DEPTH: {q.treeDepth()}")
            
            # pixelDepth
            x, y = 0, 0
            print(f"DEPTH OF ({x},{y}): {q.pixelDepth(x, y)}")
            
            # searchSubspacesWithRange and mask
            x, y, w, h = 0, 0, 3, 3
            helper.listToImage("searchSubspaces.png", q.searchSubspaces(Rect(x, y, w, h)).export())
            helper.listToImage("mask.png", q.mask(Rect(x, y, w, h)).export())
            
            # compress
            q.compress(size=8)
            helper.listToImage("compressedImage.png", q.export())
            
        # LV.2: GRAYSCALE with csv
        case '2':
            l = helper.csvToList("samples/img3.csv")
            q = QuadTree(l)
            
            # treeDepth
            print(f"TREE DEPTH: {q.treeDepth()}")
            
            # pixelDepth
            x, y = 0, 0
            print(f"DEPTH OF ({x},{y}): {q.pixelDepth(x, y)}")
            
            # searchSubspacesWithRange and mask
            x, y, w, h = 0, 0, 3, 3
            helper.listToImage("searchSubspaces.png", q.searchSubspaces(Rect(x, y, w, h)).export())
            helper.listToImage("mask.png", q.mask(Rect(x, y, w, h)).export())
            
            # compress
            q.compress(size=32)
            helper.listToImage("compressedImage.png", q.export())
            
        # LV.3: RGB with png
        case '3':
            l = helper.imageToList("samples/pic7.png")
            q = QuadTree(l)
            
            # treeDepth
            print(f"TREE DEPTH: {q.treeDepth()}")
            
            # pixelDepth
            x, y = 0, 0
            print(f"DEPTH OF ({x},{y}): {q.pixelDepth(x, y)}")
            
            # searchSubspacesWithRange and mask
            x, y, w, h = 0, 0, 3, 2
            helper.listToImage("searchSubspaces.png", q.searchSubspaces(Rect(x, y, w, h)).export())
            helper.listToImage("mask.png", q.mask(Rect(x, y, w, h)).export())
            
            # compress
            q.compress(size=4)
            helper.listToImage("compressedImage.png", q.export())
            
        # LV.4: RGB with csv
        case '4':
            l = helper.csvToList("samples/img4.csv")
            q = QuadTree(l)
            
            # treeDepth
            print(f"TREE DEPTH: {q.treeDepth()}")
            
            # pixelDepth
            x, y = 0, 0
            print(f"DEPTH OF ({x},{y}): {q.pixelDepth(x, y)}")
            
            # searchSubspacesWithRange and mask
            x, y, w, h = 0, 0, 3, 3
            helper.listToImage("searchSubspaces.png", q.searchSubspaces(Rect(x, y, w, h)).export())
            helper.listToImage("mask.png", q.mask(Rect(x, y, w, h)).export())
            
            # compress
            q.compress(size=64)
            helper.listToImage("compressedImage.png", q.export())

        # LV.5: GIF
        case '5':
            gif = helper.sequenceToLists("samples/seq1.gif")
            compressed_gif = QuadTree.sequenceCompress(gif, 64)
            helper.listsToSequence("compressedGif.mp4v", "mp4v", 10, compressed_gif)
            
        # LV.6: VIDEO
        case '6':
            video = helper.sequenceToLists("samples/vid1.mov")
            compressed_video = QuadTree.sequenceCompress(video, 128)
            helper.listsToSequence("compressedVideo.mp4", "mp4v", 25, compressed_video)


if __name__ == "__main__":
    main()
