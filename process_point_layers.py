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
# 2. Bridge points - 2022 bridge points as of 11/23/2022 
bridges = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\MassDOT_bridges_2022.gdb\\MassDOT_bridge_points_2022"
# 3. Culverts
culverts = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MASSDOT_Culverts"
# 4. MBTA rapid transit stations
mbta_rt_stations = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_MBTA_NODE"
# 5. Commuter rail stations
#    This FC contains feature extracted from MGIS_TRAINS_NODE where C_RAILSTAT = 'Y' and MAP_STA = 'Y'
cr_stations = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MGIS_TRAINS_NODE_active_mapsta"
# 6. MassDOT-owned park-and-ride lots (points)
massdot_pnr = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\Park_and_Ride_Lots_2022.gdb\\ParkandRideLots_1"
# 7. CTPS-surveyed part-and-ride lots (centroid points from polygon features)
ctps_pnr = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\CTPS_PNR_Lots_Centroid_points"

# 8. Hospitals (acute care)
hospitals = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_HOSPITALS_PT"
# 9. Hospitals non-acute care
hospitals_nonacute = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_HOSPITALS_NONACUTE_PT"
# 10. Community health centers
chcs = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_CHCS_PT"
# 11. Long-term care facilities
ltc = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_LONGTERMCARE_PT"
# 12. Medical clinics
clinics = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\medical_clinics"
# 13. Town halls
townhalls = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_TOWNHALLS_PT_MEMA"
# 14. Police stations
police = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_POLICESTATIONS_PT_MEMA"
# 15. Fire stations
fire = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.MGIS_FIRESTATIONS_PT_MEMA"
# 16. EV charging stations
ev_stations = "\\\\lindalino2\users\Public\Documents\Public ArcGIS\Database Connections\CTPS 10.6.sde\mpodata.mpodata.DOE_CHARGEHUB_LOCS_BRMPO_20221012"
# 17. BlueBikes stations
blue_bikes = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\Bikeshare\\current_bluebikes_stations_090822.gdb\\current_bluebikes_stations_090822"

input_fcs = [bridges, culverts, mbta_rt_stations, cr_stations, massdot_pnr, ctps_pnr, hospitals,
             hospitals_nonacute, chcs, ltc, clinics, townhalls, police, fire, ev_stations, blue_bikes]

# Output feature classes
temp = [ "bridges", "culverts", "mbta_rt_stations", "cr_stations", "massdot_pnr_lots_2022",
         "ctps_pnr_lots",  "hospitals", "hospitals_nonacute", "community_health_centers", 
         "lonterm_care_facilities", "clinics", "townhalls", "police", "fire", "ev_stations", "blue_bikes" ]      
 
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

