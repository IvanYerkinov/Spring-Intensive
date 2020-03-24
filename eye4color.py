import sys
from PIL import Image
from palette import getHSL, getRGB, averageHslHue, complimentaryHues, supportingHues


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


def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n


def getAdjustedHues(lis, avgcol, contrast=0):
    comphue = lis
    hslavg = getHSL(avgcol)
    comphue_lst = []
    for i in range(len(comphue)):
        hue = comphue[i]

        if contrast == 0:
            hue = (hue[0], (hslavg[1] + 0.5)/2, clamp(((hslavg[2] + 0.5)/2), 0.3, 0.65))
        else:
            hue = (hue[0], clamp((abs(1 - hslavg[1]) + hue[1])/2, 0.3, 0.6), clamp((abs(1 - hslavg[2]) + hue[2] + 0.5)/3, 0.3, 0.65))

        hue = getRGB(hue)
        comphue_lst.append(hue)
    return comphue_lst


def runImage(filename):
    pxbox = loopThroughPx(loadFilePixel(filename))
    avg = countAverageColor(pxbox)
    trueavg = countTrueAverageColor(pxbox)
    hsl = getHSL(avg)
    hsl2 = getHSL(trueavg)
    mosthue = countMostCol(pxbox)

    avghue_hsl = averageHslHue(hsl, hsl2)
    comphue = complimentaryHues(hsl)
    suphue = supportingHues(hsl)

    comphue_lst = getAdjustedHues(comphue, trueavg, 1)
    suphue_lst = getAdjustedHues(suphue, trueavg)



    print("Image: " + filename)
    print("Average color: ", end="")
    print(avg)
    print("True average: ", end="")
    print(trueavg)
    print("Average hue: ", end="")
    print(getRGB(avghue_hsl))
    print("Suggested complimentary colors:")
    for i in comphue_lst:
        print(i, end=", ")
    print("")
    print("Suggested analogous colors:")
    for i in suphue_lst:
        print(i, end=", ")
    print("")
    print("")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        runImage(arg)
