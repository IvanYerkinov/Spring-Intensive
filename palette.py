

def getHSL(px):
    # Calculate HSL color based on RGB tuple
    # Returns HSL calculation in tuple form.
    R = px[0]/255
    G = px[1]/255
    B = px[2]/255
    Cmax = max(R, G, B)
    Cmin = min(R, G, B)
    delta = Cmax - Cmin
    H = 0

    L = ((Cmax + Cmin)/2)
    S = 0
    if delta == 0:
        H = 0
        return (H, S, L)
    else:
        S = delta / (1 - abs(2 * L - 1))

    if Cmax == R:
        H = 60 * (((G - B) / delta) % 6)
        return (H, S, L)
    elif Cmax == G:
        H = 60 * (((B - R) / delta) + 2)
        return (H, S, L)
    elif Cmax == B:
        H = 60 * (((R - G) / delta) + 4)
        return (H, S, L)

    return (H, S, L)
    pass


def formatrgbd(H, C, X):
    if H >= 0 and H < 60:
        return (C, X, 0)
    elif H >= 60 and H < 120:
        return (X, C, 0)
    elif H >= 120 and H < 180:
        return (0, C, X)
    elif H >= 180 and H < 240:
        return (0, X, C)
    elif H >= 240 and H < 300:
        return (X, 0, C)
    else:
        return (C, 0, C)


def calcRGB(rgbd, m):
    return (((rgbd[0] + m) * 255)//1, ((rgbd[1] + m) * 255)//1, ((rgbd[2] + m) * 255)//1)


def getRGB(hsl):
    # Calculate RGB color based on HSL tuple
    # Returns RGB calculation in tuple form.
    C = (1 - abs(2 * hsl[2] - 1)) * hsl[1]
    X = C * (1 - abs((hsl[0] / 60) % 2 - 1))
    m = hsl[2] - C/2

    RGB = calcRGB(formatrgbd(hsl[0], C, X), m)

    return RGB
    pass


def _getaverageHue(hue1, hue2):
    hueDiff = abs(hue1 - hue2)
    X = 0
    if hueDiff <= 180:
        X = 0
    else:
        X = 180

    hue = (hue1 + hue2) / 2 + X % 360
    return hue


def complimentaryHues(hsl):
    mainDiff = (hsl[0] + 180) % 360
    hueDiff = (hsl[0] + 150) % 360
    hueDiff2 = (abs(hsl[0] + 200)) % 360
    return [(mainDiff, 1, 0.5), (hueDiff, 1, 0.5), (hueDiff2, 1, 0.5)]

    # return [(mainDiff, hsl[1], hsl[2]), (hueDiff, hsl[1], hsl[2]), (hueDiff2, hsl[1], hsl[2])]


def supportingHues(hsl):
    mainDiff = (hsl[0] + 30) % 360
    hueDiff = (hsl[0] + 50) % 360
    hueDiff2 = (abs(hsl[0] - 30)) % 360
    return [(mainDiff, 1, 0.5), (hueDiff, 1, 0.5), (hueDiff2, 1, 0.5)]
    # return [(mainDiff, hsl[1], hsl[2]), (hueDiff, hsl[1], hsl[2]), (hueDiff2, hsl[1], hsl[2])]


def averageHslHue(hsl1, hsl2):
    hue = _getaverageHue(hsl1[0], hsl2[0])
    return (hue, hsl1[1], hsl1[2])
