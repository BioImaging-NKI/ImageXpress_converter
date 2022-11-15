# ImageXpress converter
Script and executable for combining separate .tif files (channels, timepoints, ..) obtained from the ImageXpress Micro 4 microscope into ImageJ hyperstacks .tif files.

The image metadata is used to generate output files containing a single position. Naming is `<well name> site <site number>`.

## Installation instructions
- Download and unzip the file
- Open a command window (Windows-Key + r, type `cmd` and enter).
- Go to the folder where you unzipped it (type `cd C:\myCustomFolder\myCustomSubfolder\ImageXpress_converter`) or add the folder to the Path.
- usage: `ImageXpress_converter.exe [-h] [-i InputFolder] [-o OutputFolder]  [-l LogLevel]`

Options:
  -h, --help               show this help message and exit
  -i InputFolder        the root input folder containing all the separate tif images (put between " " if the inputFolder contains spaces).
  -o OutputFolder    Output folder
  -l LogLevel             LogLevel: 0 error, 1 warning, 2 info (default: 0)

Example: `ImageXpress_converter.exe -i "C:\Input images" -o "C:\Output images"`


## Changelog
Version 1.1: ImageXpress metadata is now included in the ImageDescription tag ("Show Info" in ImageJ).
