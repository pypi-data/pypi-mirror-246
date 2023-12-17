import gc
import tkinter as tk

import dotscanner.density as density
import dotscanner.files as files
import dotscanner.lifetime as lifetime
from dotscanner.programtype import ProgramType
import dotscanner.strings as strings
from dotscanner.ui.UserSettings import UserSettings
from dotscanner.ui.ThresholdAdjuster import ThresholdAdjuster
from dotscanner.ui.RegionSelector import RegionSelector
from dotscanner.ui.MicroscopeImage import MicroscopeImage
import settings.config as cfg
import settings.configmanagement as cm

cm.runChecks()


def main():
    print(strings.WELCOME_MESSAGE)
    window = tk.Tk().withdraw()
    while True:
        userSettings = UserSettings(window)
        directory, filenames = files.getDirectoryAndFilenames(userSettings)
        if userSettings.program == ProgramType.DENSITY:
            getDensityData(window, directory, filenames, userSettings)
        elif userSettings.program == ProgramType.LIFETIME:
            getLifetimeData(window, directory, filenames, userSettings)
        else:
            raise Exception(strings.PROGRAM_NAME_EXCEPTION)

        del userSettings
        gc.collect()


def getDensityData(window, directory, filenames, userSettings):
    if userSettings.reanalysis:
        if len(filenames) == 1:
            density.reanalyzeSingleDensityFile(
                window, directory, filenames[0], userSettings)
        else:
            density.reanalyzeDensityData(window, directory, userSettings)
        return

    density.checkUnitsConsistent(directory)
    alreadyMeasured = density.getAlreadyMeasured(directory)
    targetPath = files.getAnalysisTargetPath(
        directory, cfg.DENSITY_OUTPUT_FILENAME)
    for filename in filenames:
        if filename in alreadyMeasured:
            print(strings.alreadyMeasuredNotification(filename))
            continue

        print(f"\n----------\nDisplaying {filename}\n----------")
        microscopeImage = MicroscopeImage(directory, filename, userSettings)

        thresholdAdjuster = ThresholdAdjuster(
            window, microscopeImage, userSettings)
        # Updating with the threshold adjustments
        userSettings = thresholdAdjuster.userSettings
        if microscopeImage.skipped:
            density.skipFile(directory, filename, targetPath,
                             userSettings, microscopeImage)
            continue

        RegionSelector(window, microscopeImage, userSettings)
        if microscopeImage.skipped:
            density.skipFile(directory, filename, targetPath,
                             userSettings, microscopeImage)
            continue

        density.measureDensity(directory, filename,
                               targetPath, microscopeImage, userSettings)

    del microscopeImage
    del thresholdAdjuster
    del userSettings
    gc.collect()


def getLifetimeData(window, directory, filenames, userSettings):
    lifetime.checkEnoughFramesForLifetimes(filenames, userSettings)

    middleIndex = len(filenames) // 2
    middleMicroscopeImage = MicroscopeImage(
        directory, filenames[middleIndex], userSettings)

    thresholdAdjuster = ThresholdAdjuster(
        window, middleMicroscopeImage, userSettings, skipButton=False)
    # Updating with the threshold adjustments
    userSettings = thresholdAdjuster.userSettings
    RegionSelector(window, middleMicroscopeImage,
                   userSettings, skipButton=False)

    lifetime.measureLifetime(directory, filenames,
                             middleMicroscopeImage, userSettings)

    del middleMicroscopeImage
    del thresholdAdjuster
    del userSettings
    gc.collect()


if __name__ == '__main__':
    main()
