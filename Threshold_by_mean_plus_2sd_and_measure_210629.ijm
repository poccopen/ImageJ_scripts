macro "threshold_by_mean_plus_2sd_and_measure [6]" {
 
 //shortcut is assigned at the key [6]
 
 //threshlold setting in the previous time will be reset
 resetThreshold;

 //get the raw statistic properties (in the ROI)
 getRawStatistics(nPixels, mean, min, max, std);

 //[for debugging] the properties related to the whole ROI will be output in "Log" window
 //print(nPixels, mean, min, max, std, mean+std*2);

 //new threshold setting. lower boundary = mean+2SD
 setThreshold(mean+std*2, max);

 //"Measure" command will be executed.
 //measured values are dependent on "Set Measurements" command
 doCommand("Measure");

}


