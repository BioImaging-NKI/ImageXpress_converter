// Groovy macro to retrieve metadata from tif files created with the NKI ImageXpress converter

import ij.IJ
import groovy.json.JsonSlurper

// Open an image
imp = IJ.openImage("C:/ImageXpress/A01 Site 1.tif")
def jsonSlurper = new JsonSlurper()
def metadata = jsonSlurper.parseText(imp.getInfoProperty()) 

// Print Description (a single string with information about the data)
println("\n"+metadata.Description) 

// PlaneInfo contains many fields with image information
println("\nPlaneInfo has " + metadata.PlaneInfo.size() + " fields:")
metadata.PlaneInfo.each({println(it)})

// You can also get the value of a single field
println("\nValue of zoom-percent is : " + metadata.PlaneInfo."zoom-percent")
