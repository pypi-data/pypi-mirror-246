import matplotlib

import dotscanner.strings as strings
import settings.config as cfg


def getWindowDimensions(measuredHeight, measuredWidth):
    if cfg.DYNAMIC_WINDOW:
        height = measuredHeight - 180
        detectedWidth = measuredWidth - 180

        if height + 88 < detectedWidth:  # buttonBar width = 88
            width = height + 88
        else:
            width = detectedWidth

    else:
        height = cfg.WINDOW_HEIGHT
        width = cfg.WINDOW_WIDTH

    if height < 650:
        print(strings.WINDOW_SIZE_WARNING)

    return width, height


def printProgressBar(iteration, total, prefix="", suffix="", decimals=1, barLength=50, fill="█",
                     printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(barLength * iteration // total)
    bar = fill * filledLength + "-" * (barLength - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)

    if iteration == total:
        print()


def setupWindow():
    matplotlib.rcParams["toolbar"] = "None"
    matplotlib.rcParams["figure.facecolor"] = "gray"
    matplotlib.rcParams["figure.subplot.left"] = 0.01
    matplotlib.rcParams["figure.subplot.bottom"] = 0.01
    matplotlib.rcParams["figure.subplot.right"] = 0.99
    matplotlib.rcParams["figure.subplot.top"] = 0.99
    matplotlib.rcParams["xtick.bottom"] = False
    matplotlib.rcParams["xtick.labelbottom"] = False
    matplotlib.rcParams["ytick.left"] = False
    matplotlib.rcParams["ytick.labelleft"] = False
