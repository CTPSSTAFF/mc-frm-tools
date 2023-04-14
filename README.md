# mc-frm-tools
A set of tools for performing overlay analysis on a collection of point, line, and polygon feature classes using the classified MC-FRM flood probability data.  
The tools fall into two sets:
1. Tools for performing overlay analysis on the classified 2050 MC-FRM flood probabiltiy data
2. Tools for performing overlay analysis on the classified 'current conditions' MC-FRM flood probability data

Set #1 was used for the Needs Assessment for the 2050 Long Range Transportation Plan; overlay analysis is performed on a variety of data.
Set #1 will be used for presenting current conditions; overlay analysis is performed on only one dataset.

## Overview of '2050 Condition Analysis' Tools
The analysis is performed on __point__ feature classes using a simple test for geometric intersection.  

The analysis is performed on the __line__ and __polygon__ features using the ESRI "Identity" tool, 
which reports how much of each feature intersects the "identity" feature,
in this case the 2050 flood risk polygons.
The "Summary Statistics" tool is then run to calculate the sum how much of each "class" of 
input feature \(e.g., roads with a functional classification of _N_\) intersect with the polygon representing each level of flood risk.
Lastly, these sums are converted from meters (or square meters) to miles (or square miles.)

### Input Feature Classes
The analysis is performed on the following feature classes:
* Point
  * Bridge points (MassDOT)
  * Culverts (MassDOT)
  * MBTA rapid transit stations
  * MBTA commuter rail stations
  * MassDOT-owned park-and-ride lots 
  * CTPS-surveyed part-and-ride lots (centroid points derived from polygon features)
  * Freight rail yards (MassDOT)
  * Seaports (MassDOT)
  * Intermodal Freight Facilities Rail TOFC COFC
  * Hospitals (acute care)
  * Hospitals non-acute care
  * Community health centers
  * Long-term care facilities
  * Medical clinics
  * Town halls
  * Police stations
  * Fire stations
  * EV charging stations
  * BlueBikes stations
* Line
  * MBTA rapid transit lines - clipped to TOWNSSURVEY_POLY, selecting records with coastal_poly = 'NO'
  * Commuter rail lines - clipped to TOWNSSURVEY_POLY, selecting records with coastal_poly = 'NO'
  * Road Inventory 2021
  * MassDOT Rail Inventory
  * National highway system freight network - Critical Urban Corridors
  * National highway system freight network - Critical Rural Corridors
  * National highway system freight network - Primary Highway Freight System
  * National highway system freight network - Non-Primary Highway Freight System
* Polygon
  * 2020 Census tracts with EJ attributes, clipped to extent of 2050 MC-FRM probability polygons in order to greatly improve run-time speed
    * minority
    * low income
    * limied English proficiency
    * disability
    * elderly
    * youth

### Outputs
#### Feature Classes
Each tool produces an ESRI FileGeodatabase feature class containing the geometric and tabular results of the overlay analysis for each input feature class.
#### CSV Files
Each tool produces a CSV file containing the tabular results of the overlay analysis for each input feature class.

## Overview of 'Current Condition Analysis' Tools
The analysis is performed only on one __line__ feature class using the ESRI "Identity" tool, which reports how much of each feature intersects the "identity" 
feature, in this case the current flood risk polygons.
The "Summary Statistics" tool is then run to calculate how much of each "class" of input feature \(e.g., roads with a functional classification of X\) intersect
with the polygon representing each level of flood risk.

### Input Feature Classes
* Line
  * Road Inventory 2021

### Outputs
Same as for the 2050 analysis tools.

## Usage
The usage is the same for the two sets of tools.
### Requriements
These tools require the ESRI __arcpy__ library, and are intended to be run under the ESRI ArcGIS environment.
### Parameters
Each of these tools take 2 parameters:
1. file geodatabase, for output feature classes
2. directory (folder), for output CSV files

-- B. Krepp   
23 June 2022, 27 November 2022, 12 April 2023
