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
# Output Geodatabase
output_gdb = arcpy.GetParameterAsText(0)
# Output directory (i.e., folder) for CSV files
csv_output_dir = arcpy.GetParameterAsText(1)

# Sanity check: Echo input parameters
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
#      Note: Be sure to use data projected to "Mass State Plane NAD83 Meters", so linear units will be in _meters_!
tracts = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\TEPops_tracts_2020_MPO.gdb\\TEPops_tracts_2020_MPO_NA_clip_EPSG26986"

# Output feature classes
ej_factors = [ "minority" , "lowinc", "lep", "disability", "elderly", "youth" ]

# Generate the output feature classes, stats tables, and CSV files
for ej_factor in ej_factors:
    s = 'Processing ' + ej_factor
    arcpy.AddMessage(s)
    # Name of FC input to "Identity" operation, containing records seelected from the tracts FC
    input_fc = output_gdb + "\\" + ej_factor + '_tracts'
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
