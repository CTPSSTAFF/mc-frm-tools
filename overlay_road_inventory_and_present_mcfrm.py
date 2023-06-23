# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# overlay_road_inventory_and present_mcfrm.py
#
# Description: Intersect (using "Identity" tool) 2021 Road Inventory with present-day MC-FRM probability classificaiton polygons
#              Capture output in a feature class, and export the output FC to a CSV file.
#
# Note: This is implemented in a general way, such that additional line feature datasets can be added to
#       those included in the overlay analysis. 
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
# 1. Present-day MC-FRM inundation classification score polygons
probability_score_present = "G:\\Certification_Activities\\Resiliency\\data\\mcfrm\\DERIVED_PRODUCTS\\CTPS_classification_mpo_h2o_clip\\CTPS_probability_score_present_mpo_h2o_clip.shp"
arcpy.AddMessage('Classification shapefile: ' + probability_score_present)

# Input data: "target features"
# 2. Road Inventory 2021
road_inv_2021 = r"\\lindalino2\apollo\mpodata\data\roads_gdb\RoadInv2021_and_pavement.gdb\RoadInventory"

# Line FCs to include in analysis
input_fcs = [ road_inv_2021 ]

# List of fields to aggregate           
aggregation_field_lists = [ "F_Class;score" ]
                 
# Output feature classes
temp = [ "road_inventory_2021" ]
         
output_fcs = [ output_gdb + "\\" + fc + "_fc" for fc in temp ]
# Output tables
output_tbls = [ output_gdb + "\\" + fc + "_stats" for fc in temp ]

# Output CSV files
# Note because of the way the ESRI table-to-table tool works,
# the output folder and file name are specified _separately_ rater than as a single file path.
output_csv_fns = [ name + '_stats.csv' for name in temp ]

# Generate the output feature classes, stats tables, and CSV files
for (in_fc, out_fc, aggr_field_list, out_tbl, out_csv_fn) in zip(input_fcs, output_fcs, aggregation_field_lists, output_tbls, output_csv_fns):
    s = 'Processing ' + in_fc
    arcpy.AddMessage(s)
    #
    arcpy.Identity_analysis(in_fc, probability_score_present, out_fc, "ALL", "", "NO_RELATIONSHIPS")
    # Aggregate length (in meters) by line and score
    arcpy.Statistics_analysis(out_fc, out_tbl, "shape_Length SUM", aggr_field_list)
    arcpy.AddField_management(out_tbl, "length_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    # Convert length in meters to miles
    arcpy.CalculateField_management(out_tbl, "length_mi", "!SUM_shape_Length! * 0.000621", "PYTHON_9.3", "")
    #
    arcpy.TableToTable_conversion(out_tbl, csv_output_dir, out_csv_fn)
#
