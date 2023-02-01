# mc-frm-tools
A set of 3 tools for performing overlay analysis on a collection of point, line, and polygon feature classes using the classified 2050 MC-FRM flood probability data.

The analysis is performed on point feature classes using a simple test for geometric intersection. The analysis is performed on the line and polygon features
using the ESRI "Identity" tool, which reports how much of each feature intersects the "identity" feature, in this case the flood risk polygons. The "Summary
Statistics" tool is then run to calculate how much of each "class" of input feature (e.g., roads with a functional classification of X) intersect with the polygon
representing each level of flood risk.

The analysis is performed on the following feature classes:
* Point
  * bridge points
  * culverts
  * MBTA rapid transit stations
  * MBTA commuter rail stations
  * MassDOT-owned park-and-ride lots 
  * CTPS-surveyed part-and-ride lots (centroid points from polygon features
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
  * MassDOT Rail Inventor
  * National highway system freight network - Critical Urban Corridors
  * National highway system freight network - Critical Rural Corridors
  * National highway system freight network - Primary Highway Freight System
  * National highway system freight network - Non-Primary Highway Freight System
* Polygon
  * 2020 Census tracts with EJ attributes, clipped to extent of 2050 MC-FRM probability polygons
    * minority
    * low income
    * limied English proficiency
    * disability
    * elderly
    * youth

Parameters:
1. file geodatabase for output feature classes
2. directory (folder) for output CSV files

Requriements:
* These tools require the ESRI __arcpy__ library.

-- B. Krepp 
23 June 2022, 27 November 2022
