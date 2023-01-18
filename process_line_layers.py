# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# process_line_layers.py
#
# Description: Intersect (using "Identity" tool) line layers of interest with 2050 MC-FRM probability classificaiton polygons
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
# 2. MBTA rapid transit lines - clipped to TOWNSSURVEY_POLY, selecting records with coastal_poly = 'NO'
mbta_rt = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MGIS_MBTA_ARC_clip_dissolve"
# 3. Commuter rail lines - clipped to TOWNSSURVEY_POLY, selecting records with coastal_poly = 'NO'
mbta_cr = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MGIS_TRAINS_RTE_TRAIN_clip"
# 4. Road Inventory 2021
road_inv_2021 = r"\\lindalino2\apollo\mpodata\data\roads_gdb\RoadInv2021_and_pavement.gdb\RoadInventory"

# 5. MassDOT Rail Inventory
rail_inventory = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MASSDOT_RAIL_INVENTORY"
# 6. National highway system freight network - Critical Urban Corridors
nhfn_critical_urban = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\NHFN_MA.gdb\\NHFN_Critical_Urban_Corridors111219"
# 7. National highway system freight network - Critical Rural Corridors
nhfn_critical_rural = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\NHFN_MA.gdb\\NHFN_Critical_Rural_Corridors111219"
# 8. National highway system freight network - Primary Highway Freight System
nhfn_phfs = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\NHFN_MA.gdb\\NHFN_PHFS_111219"
# 9. National highway system freight network - Non-Primary Highway Freight System
nhfn_non_phfs = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\NHFN_MA.gdb\\NHFN_NON_PHFS_111219"

input_fcs = [ mbta_rt, mbta_cr, road_inv_2021, 
              rail_inventory, nhfn_critical_urban, nhfn_critical_rural, nhfn_phfs, nhfn_non_phfs ]
          
aggregation_field_lists = [ "line;score", "comm_line;score", "F_Class;score",
                            "freight_op;ownership;score", "ROUTE_NAME;score", "ROUTE_NAME;score", "ROUTE_ID;ROAD_CLASS;score", "ROUTE_ID;ROAD_CLASS;score" ]
                 
# Output feature classes
temp = [ "mbta_rapid_transit", "commuter_rail", "road_inventory_2021",
         "rail_inventory", "nhfn_critical_urban", "nhfn_critical_rural", "nhfn_phfs", "nhfn_non_phfs" ]
         
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
    arcpy.Identity_analysis(in_fc, probability_score_2050, out_fc, "ALL", "", "NO_RELATIONSHIPS")
    # Aggregate length (in meters) by line and score
    arcpy.Statistics_analysis(out_fc, out_tbl, "shape_Length SUM", aggr_field_list)
    arcpy.AddField_management(out_tbl, "length_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    # Convert length in meters to miles
    arcpy.CalculateField_management(out_tbl, "length_mi", "!SUM_shape_Length! * 0.000621", "PYTHON_9.3", "")
    #
    arcpy.TableToTable_conversion(out_tbl, csv_output_dir, out_csv_fn)
#
