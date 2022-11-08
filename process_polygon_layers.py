# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# process_polygon_layers.py
#
# Description: Intersect (using "Identity" tool) polygon layers of interest with 2050 MC-FRM probability classificaiton polygons
#              Capture output in a feature class , and export each output FC to a CSV file.
# ---------------------------------------------------------------------------
#
# Import arcpy module
import arcpy

# Read input parameters
# GDB for intermediate (temp) data
temp_gdb = arcpy.GetParameterAsText(0)
# Output Geodatabase
output_gdb = arcpy.GetParameterAsText(1)
# Output directory (i.e., folder) for CSV files
csv_output_dir = arcpy.GetParameterAsText(2)

# Sanity check: Echo input parameters
arcpy.AddMessage('Temp GDB: ' + temp_gdb) # Actually, not needed in this script.
arcpy.AddMessage('Output GDB: ' + output_gdb)
arcpy.AddMessage('Output folder for CSVs: ' + csv_output_dir)

# Input data "identity features" (for our purposes, "intersection features")
# 1. 2050 MC-FRM inundation classification score polygons
probability_score_2050 = "G:\\Certification_Activities\\Resiliency\\data\\mcfrm\\DERIVED_PRODUCTS\\CTPS_classification\\CTPS_probability_score_2050.shp"
arcpy.AddMessage('Classification shapefile: ' + probability_score_2050)

# Input data: "target features"
# 2. 2020 Census tracts with EJ attributes
tracts_raw = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\TEPops_tracts_2020_MPO.gdb\\TEPops_tracts_2020_MPO_NA"
# 2.a. 2020 Census tracts with EJ attributes, clipped to extent of 2050 MC-FRM probability polygons
tracts = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\TEPops_tracts_2020_MPO.gdb\\TEPops_tracts_2020_MPO_NA_clip"

# 3. Park-and-Ride Lots polygons
CTPS_PNR_Lots_Polygons = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.CTPS_PNR_Lots_Polygons"

# Output feature classes
ej_factors = [ "minority" , "lowinc", "lep", "disability", "elderly", "youth" ]


# Generate the output feature classes, stats tables, and CSV files
for ej_factor in ej_factors:
    s = 'Processing ' + ej_factor
    arcpy.AddMessage(s)
    # Name of FC input to "Identity" operation, containing records seelected from the tracts FC
    input_fc = output_gdb + "\\" + ej_factor + '_temp'
    # Name of output FC, stats table, and CSV file
    output_fc = output_gdb + "\\" + ej_factor + '_fc'
    output_tbl = output_gdb + "\\" + ej_factor + '_stats'
    output_csv_fn = ej_factor + '_stats.csv'
    # Select records
    query_string = ej_factor.upper() + '_EXCEEDS_QUINT5 = 1'
    arcpy.Select_analysis(tracts, input_fc, query_string)
    # Identity operation
    arcpy.Identity_analysis(input_fc, probability_score_2050, output_fc, "ALL", "", "NO_RELATIONSHIPS")
    # Aggregate area (in square meters) by score
    arcpy.Statistics_analysis(output_fc, output_tbl, "Shape_Area SUM", "score")
    arcpy.AddField_management(output_tbl, "area_sqmi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    # Convert are in square meters to square miles
    arcpy.CalculateField_management(output_tbl, "area_sqmi", "!SUM_Shape_Area! / 2589988.1103", "PYTHON_9.3", "")
    arcpy.TableToTable_conversion(output_tbl, csv_output_dir, output_csv_fn)
#

# Analyze PNR Polygons separately - no selection of features is required
s = 'Processing CTPS PNR polygon layer'
arcpy.AddMessage(s)
# Intermediate (temp) data
ident_output = output_gdb + "\\" + "ctps_pnr_lots_fc"
# Final output table
pnr_output = output_gdb + "\\" + "ctps_pnr_lots_stats"
# Process: Identity
arcpy.Identity_analysis(CTPS_PNR_Lots_Polygons, probability_score_2050, ident_output, "ALL", "", "NO_RELATIONSHIPS")
# Process: Summary Statistics
arcpy.Statistics_analysis(ident_output, pnr_output, "shape_Area SUM", "score")
# Process: Add Field for inundated area, in square miles
arcpy.AddField_management(pnr_output, "area_sqmi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
# Process: Calculate Field - convert area in square meters to square miles
arcpy.CalculateField_management(pnr_output, "area_sqmi", "!SUM_shape_Area! / 2589988.1103", "PYTHON_9.3", "")
