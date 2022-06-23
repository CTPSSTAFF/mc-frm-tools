# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# process_point_layers.py
#
# Description: Intersect point layers of interest with 2050 MC-FRM probability classificaiton polygons
#              Capture output in a feature class 
#              TBD: and export each output FC to a CSV file
# ---------------------------------------------------------------------------

import arcpy

# Input data "identity features" (for our purposes, "intersection features"
# 1. 2050 MC-FRM inundation classification score polygons
probability_score_2050 = "G:\\Certification_Activities\\Resiliency\\data\\mcfrm\\DERIVED_PRODUCTS\\probability_polygons\\probability_score_2050.shp"

# Input data: "target features"
# 2. Bridge points
bridges = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MASSDOT_Bridge_Points"
# 3. Culverts
culverts = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\MASSDOT_Culverts"
# 4. MBTA rapid transit stations
mbta_rt_stations = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_MBTA_NODE"
# 5. Commuter rail stations
cr_stations = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_TRAINS_NODE"
# 6. MassDOT-owned park-and-ride lots (points)
massdot_pnr = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\Park_and_Ride_Lots.gdb\\ParkandRideLots_1"
# 7. Hospitals (acute care)
hospitals = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_HOSPITALS_PT"
# 8. Hospitals non-acute care
hospitals_nonacute = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_HOSPITALS_NONACUTE_PT"
# 9. Community health centers
chcs = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_CHCS_PT"
# 10. Long-term care facilities
ltc = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_LONGTERMCARE_PT"
# 11. Medical clinics
clinics = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\reference_data.gdb\\medical_clinics"
# 12. Town halls
townhalls = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_TOWNHALLS_PT_MEMA"
# 13. Police stations
police = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_POLICESTATIONS_PT_MEMA"
# 14. Fire stations
fire = "Database Connections\\CTPS 10.6.sde\\mpodata.mpodata.MGIS_FIRESTATIONS_PT_MEMA"

input_fcs = [bridges, culverts, mbta_rt_stations, cr_stations, massdot_pnr, hospitals,
             hospitals_nonacute, chcs, ltc, clinics, townhalls, police, fire ]

# Output Geodatabase
output_gdb = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\output_db.gdb\\"

# Output feature classes
temp = [ "bridges", "culverts", "mbta_rt_stations", "cr_stations", "massdot_pnr_lots", "hospitals",
         "hospitals_nonacute", "community_health_centers", "lonterm_care_facilities", "clinics", "townhalls", "police", "fire" ]              
output_fcs = [ output_gdb + fc for fc in temp ]

# Output folder for CSV files
output_csv_dir = "G:\\Certification_Activities\\2023 LRTP Destination 2050\\GIS_Data\\MC_FRM_Analysis\\csv_out\\"

# Output CSV files
# Note because of the way the ESRI table-to-table tool works,
# the output folder and file name are specified separately rater than as a single file path.
output_csv_fns = [ name + '.csv' for name in temp]

# Generate the output feature classes and CSV files
for (in_fc, out_fc, out_csv_fn) in zip(input_fcs, output_fcs, output_csv_fns):
    s = 'Processing ' + in_fc
    arcpy.AddMessage(s)
    arcpy.Intersect_analysis([probability_score_2050, in_fc], out_fc, "ALL", "", "INPUT")
    arcpy.TableToTable_conversion(out_fc, output_csv_dir, out_csv_fn)
#

