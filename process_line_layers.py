# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# process_line_layers.py
#
# Description: 
# ---------------------------------------------------------------------------


# Import arcpy module
import arcpy


# Input data "identity features" (for our purposes, "intersection features"
# 1. 2050 MC-FRM inundation classification score polygons
probability_score_2050 = "G:\\Certification_Activities\\Resiliency\\data\\mcfrm\\DERIVED_PRODUCTS\\probability_polygons\\probability_score_2050.shp"

# Input data: "target features"
# 2. Road Inventory - clipped to MPO region
# road_inventory = TBD
# 3. MBTA rapid transit lines - clipped to TOWNSSURVEY_POLY, selecting records with coastal_poly = 'NO'
mbta_rt = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MGIS_MBTA_ARC_clip_dissolve"
# 4. Commuter rail lines - clipped to TOWNSSURVEY_POLY, selecting records with coastal_poly = 'NO'
mbta_cr = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\CTPS_Rail_arc_commuter"
# 5. Road Inventory 2020
road_inv = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\RoadInventory2020.gdb\\RoadInventory2020"

input_fcs = [mbta_rt, mbta_cr, road_inv]

aggregation_field_lists = [ "line;score", "comm_line;score", "F_Class;score" ]


# GDB for intermediate (temp) data
temp_gdb = "C:\\Users\\bkrepp\\Documents\\ArcGIS\\Default.gdb\\"

# Output Geodatabase
output_gdb = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\output_db.gdb\\"

# Output feature classes
temp = [ "mbta_rapid_transit", "commuter_rail", "road_inventory" ]
output_fcs = [ output_gdb + fc + "_fc" for fc in temp ]
# Output tables
output_tbls = [ output_gdb + fc + "_stats" for fc in temp ]

# Output folder for CSV files
output_csv_dir = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\csv_out\\"

# Output CSV files
# Note because of the way the ESRI table-to-table tool works,
# the output folder and file name are specified separately rater than as a single file path.
output_csv_fns = [ name + '_stats.csv' for name in temp ]

# Generate the output feature classes, stats tables, and CSV files
for (in_fc, out_fc, aggr_field_list, out_tbl, out_csv_fn) in zip(input_fcs, output_fcs, aggregation_field_lists, output_tbls, output_csv_fns):
    s = 'Processing ' + in_fc
    arcpy.AddMessage(s)
    #
    arcpy.Identity_analysis(in_fc, probability_score_2050, out_fc, "ALL", "", "NO_RELATIONSHIPS")
    # Aggregate length (in meters) by line and score
    arcpy.Statistics_analysis(out_fc, out_tbl, "shape_Length SUM", aggr_field_list)
    arcpy.AddField_management(out_tbl, "length_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    # Convert length in meters to miles
    arcpy.CalculateField_management(out_tbl, "length_mi", "!SUM_shape_Length! * 0.000621", "PYTHON_9.3", "")
    #
    arcpy.TableToTable_conversion(out_tbl, output_csv_dir, out_csv_fn)
#
