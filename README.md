# ImageXpress converter
Windows executable program for combining separate .tif files (channels, timepoints, ..) obtained from the ImageXpress Micro 4 microscope into ImageJ hyperstacks `.tif` files.

All images in the input folder (including subfolders) are read and - using the image metadata - combined into hyperstacks images, each containing a single site (xy position).
The naming scheme of the output files is `<well name> site <site number>.tif`.

## Installation and run instructions
- [Download](https://github.com/BioImaging-NKI/ImageXpress_converter/releases/download/v1.2/ImageXpress_converter_v1.2.zip) and unzip the file
- Double-click `ImageXpress_converter.exe`
- Specify input folder and output folder and click 'Run'

### Running via the command window
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

Version 1.2: Added GUI

## How to parse ImageXpress metadata from the generated tif files
The original ImageXpress metadata is stored in the ImageDescription tag in JSON format, printed a single line. It consists of 6 keys. Some of the corresponding values contain info in a string, others contain info as a list. Below is an example groovy macro how to correctly retrieve the metadata:
```
import ij.IJ
import groovy.json.JsonSlurper

// Open an image
imp = IJ.openImage("C:/ImageXpress/A01 Site 1.tif")
def jsonSlurper = new JsonSlurper()
def metadata = jsonSlurper.parseText(imp.getInfoProperty()) 

// Print the metadata keys
println("\nMetadata keys:")
metadata.each({println(it.key)})

// Description is a single string with information about the data
println("\nDescription:\n"+metadata.Description)

// PlaneInfo contains many fields with image information
println("\nPlaneInfo has " + metadata.PlaneInfo.size() + " fields:")
metadata.PlaneInfo.each({println(it)})

// You can also get the value of a single field
println("\nValue of zoom-percent is : " + metadata.PlaneInfo."zoom-percent")
```
