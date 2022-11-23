# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# process_point_layers.py
#
# Description: Intersect point layers of interest with 2050 MC-FRM probability classificaiton polygons
#              Capture output in a feature class , and export each output FC to a CSV file.
# ---------------------------------------------------------------------------

import arcpy

# Read input parameters
# Output Geodatabase
output_gdb = arcpy.GetParameterAsText(0)
# Output directory (i.e., folder) for CSV files
csv_output_dir = arcpy.GetParameterAsText(1)

# Input data "identity features" (for our purposes, "intersection features")
# 1. 2050 MC-FRM inundation classification score polygons
probability_score_2050 = "G:\\Certification_Activities\\Resiliency\\data\\mcfrm\\DERIVED_PRODUCTS\\CTPS_classification\\CTPS_probability_score_2050.shp"
arcpy.AddMessage('Classification shapefile: ' + probability_score_2050)

# Input data: "target features"
# 2. Bridge points
# Pre-2022 bridge points (commented out as of 11/23/2022)
#    bridges = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MASSDOT_Bridge_Points"
# 2020 bridge points
bridges = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\MassDOT_bridges_2022.gdb\\MassDOT_bridge_points_2022"
# 3. Culverts
culverts = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MASSDOT_Culverts"
# 4. MBTA rapid transit stations
mbta_rt_stations = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_MBTA_NODE"
# 5. Commuter rail stations
cr_stations = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_TRAINS_NODE"
# 6. MassDOT-owned park-and-ride lots (points)
#    Using 2022 bridge points as of 11/23/2022
massdot_pnr = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\Park_and_Ride_Lots_2022.gdb\\ParkandRideLots_1"
# 7. Hospitals (acute care)
hospitals = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_HOSPITALS_PT"
# 8. Hospitals non-acute care
hospitals_nonacute = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_HOSPITALS_NONACUTE_PT"
# 9. Community health centers
chcs = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_CHCS_PT"
# 10. Long-term care facilities
ltc = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_LONGTERMCARE_PT"
# 11. Medical clinics
clinics = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\medical_clinics"
# 12. Town halls
townhalls = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_TOWNHALLS_PT_MEMA"
# 13. Police stations
police = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_POLICESTATIONS_PT_MEMA"
# 14. Fire stations
fire = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_FIRESTATIONS_PT_MEMA"
# 15. EV charging stations
ev_stations = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.DOE_CHARGEHUB_LOCS_BRMPO_20221012"
# 16. BlueBikes stations
blue_bikes = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\Bikeshare\\current_bluebikes_stations_090822.gdb\\current_bluebikes_stations_090822"

input_fcs = [bridges, culverts, mbta_rt_stations, cr_stations, massdot_pnr, hospitals,
             hospitals_nonacute, chcs, ltc, clinics, townhalls, police, fire, ev_stations, blue_bikes]

# Output feature classes
temp = [ "bridges", "culverts", "mbta_rt_stations", "cr_stations", "massdot_pnr_lots_2022", "hospitals",
         "hospitals_nonacute", "community_health_centers", "lonterm_care_facilities", "clinics", "townhalls", "police", "fire",
         "ev_stations", "blue_bikes" ]         
output_fcs = [ output_gdb + "\\" + fc for fc in temp ]

# Output CSV files
# Note because of the way the ESRI table-to-table tool works,
# the output folder and file name are specified separately rater than as a single file path.
output_csv_fns = [ name + '.csv' for name in temp]

# Generate the output feature classes and CSV files
for (in_fc, out_fc, out_csv_fn) in zip(input_fcs, output_fcs, output_csv_fns):
    s = 'Processing ' + in_fc
    arcpy.AddMessage(s)
    arcpy.Intersect_analysis([probability_score_2050, in_fc], out_fc, "ALL", "", "INPUT")
    arcpy.TableToTable_conversion(out_fc, csv_output_dir, out_csv_fn)
#

