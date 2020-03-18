import sys
import colorsys
from PIL import Image
from palette import getHSL, getRGB, averageHslHue


def loadFilePixel(filename):
    im = Image.open(filename)
    px = im.load()
    return (px, im.size)


def loopThroughPx(pxnsize):
    pxbox = {}
    px = pxnsize[0]
    size = pxnsize[1]
    ix = size[0]
    iy = size[1]
    for x in range(ix):
        for y in range(iy):
            pixels = px[x, y]
            pixel = (pixels[0], pixels[1], pixels[2])
            if pixel in pxbox:
                pxbox[pixel] += 1
            else:
                pxbox[pixel] = 1
    return pxbox


def countTrueAverageColor(pxbox):
    r = 0
    g = 0
    b = 0
    avg = 0

    for px in pxbox:
        count = pxbox[px]
        r += px[0] * count
        g += px[1] * count
        b += px[2] * count
        avg += count

    r = r//avg
    g = g//avg
    b = b//avg

    return (r, g, b)


def countAverageColor(pxbox):
    r = 0
    g = 0
    b = 0
    avg = 0

    for px in pxbox:
        count = 1
        r += px[0] * count
        g += px[1] * count
        b += px[2] * count
        avg += count

    r = r//avg
    g = g//avg
    b = b//avg

    return (r, g, b)


def countMostCol(pxbox):
    pxList = [None, None, None]
    highest = [0, 0, 0]
    pos = 0
    for px in pxbox:
        num = pxbox[px]
        lp = True
        while(lp is True):
            if num >= highest[pos]:
                pxList[pos] = px
                highest[pos] = num
                lp = False
            else:
                pos += 1
                if pos > 2:
                    lp = False
                    pos = 0
    return pxList[0:3]


def countLeastCol(pxbox):
    pxList = [None, None, None]
    lowest = [0, 0, 0]
    pos = 0
    for px in pxbox:
        num = pxbox[px]
        lp = True
        while(lp is True):
            if num <= lowest[pos] or lowest[pos] == 0:
                pxList[pos] = px
                lowest[pos] = num
                lp = False
            else:
                pos += 1
                if pos > 2:
                    lp = False
                    pos = 0
    return pxList[0:3]


if __name__ == "__main__":
    images = sys.argv[1]
    pxbox = loopThroughPx(loadFilePixel(images))

    print(countTrueAverageColor(pxbox))
    avg = countAverageColor(pxbox)
    print(avg)
    hsl = getHSL(avg)
    hsl2 = getHSL((36, 150, 237))
    print(hsl)
    avghue = averageHslHue(hsl, hsl2)
    print(getRGB(avghue))
    print(countMostCol(pxbox))
    print(countLeastCol(pxbox))
