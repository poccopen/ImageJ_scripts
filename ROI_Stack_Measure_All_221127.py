from ij import IJ
from ij.plugin.frame import RoiManager
import os

imp = IJ.getImage()
TotalFrames = imp.getNFrames()

rm = RoiManager().getInstance()
ROIs = rm.getRoisAsArray()


for index in range(len(ROIs)):
	rm.select(index)
	for f in range(TotalFrames):
		imp.setSlice(f)
		IJ.run("Measure")