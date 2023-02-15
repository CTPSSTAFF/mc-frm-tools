# mc-frm-tools
A set of 3 tools for performing overlay analysis on a collection of point, line, and polygon feature classes using the classified 2050 MC-FRM flood probability data.

## Overview
The analysis is performed on __point__ feature classes using a simple test for geometric intersection. The analysis is performed on the __line__ and __polygon__
features using the ESRI "Identity" tool, which reports how much of each feature intersects the "identity" feature,
in this case the flood risk polygons.
The "Summary Statistics" tool is then run to calculate how much of each "class" of input feature \(e.g., roads with a functional classification of X\) intersect
with the polygon representing each level of flood risk.

## Input Feature Classes
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
  * Community health center
  * Long-term care facilitie
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

## Outputs
### Feature Classes
Each tool produces an ESRI FileGeodatabase feature class containing the geometric and tabular results of the overlay analysis for each input feature class.
### CSV Files
Each tool produces a CSV file containing the tabular results of the overlay analysis for each input feature class.

## Usage
### Requriements
These tools require the ESRI __arcpy__ library, and are intended to be run under the ESRI ArcGIS environment.
### Parameters
Each of these tools take 2 parameters:
1. file geodatabase, for output feature classes
2. directory (folder), for output CSV files

-- B. Krepp   
23 June 2022, 27 November 2022
