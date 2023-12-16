Sun Path Diagrams
===================

**Sun Path Diagrams** is an application that outputs, as png images, the horizontal and vertical sun path diagrams. The input parameters are completed using a GUI built with Tkinter. The algorithms and formulas used to calculate the sun position were taken from the paper *'Solar position algorithm for solar radiation applications'
(I. Reda, A. Andreas, 2003)*.

Installation
------------
Create a virtual environment, activate it and run the command below in your terminal:

```
pip install sun-path-diagrams
```

Usage
-----
Once the installation process is finished, run

```
sun-path-diagrams
``` 

in your terminal and the **Sun Path Diagrams** GUI should appear. The input parameters in the GUI are (hopefully) self-explanatory. Note that there is input validation built in the GUI but it is not exhaustive.

Some extra notes:

* The minimum year is 1900 and the maximum is 2100
* The image files are automatically named as *VerticalSunPath_year-month-day.png* and *HorizontalSunPath_year-month-day.png* where year-month-day is the date for which the sun-path is calculated
* The resolution of the output images is 800x800 pixels, enough for most reports or presentations
* The plotting data is saved (if selected) as a csv file with the fields: **dates**, **azimuths** and **altitudes**. There are 365/366 records (one for each day of the year) and the azimuths and altitudes contain 24 values each (for every hour of the day). The csv file is named *SunPositions_year-month-day.csv*

Release History
---------------
* 1.0.0 
	* First working release

Licence
---------------------------
The **Sun Path Diagrams** app is available under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)



