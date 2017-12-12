#!/usr/bin/env python

import subprocess
import argparse

import dxpy

###
#Nathaniel Watson
#2016-12-11
#nathankw@stanford.edu
###

RAW_DATA_FOLDER = "/raw_data" #The raw_data folder location in a SCGPM DNAnexus project.
APP_NAME = "scgpm_clean_raw_data" #App's name on DNAnexus
APP = dxpy.DXApp(name="scgpm_clean_raw_data")

description = """This script calls the DNAnexus app I built called SCGPM Clean Raw Data at https://platform.dnanexus.com/app/scgpm_clean_raw_dataRemoves to unwanted files (that drive up the storage costs) from the raw_data folder of a DNAnexus project containing sequencing results from the SCGPM sequencing workflow. Most of the files in the raw_data folder are removed. Moreover, the lane tarball is removed; the XML files RunInfo.xml and runParameters.xml are extracted from *Interop.tar and then the tarball is removed; finally, *metadata.tar is removed. The extracted XML files are uploaded back to the raw_data folder. 

Queryies DNAnexus for all projects billed to the specified org and that were created within the last -d days.
"""

parser = argparse.ArgumentParser(description=description,formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-d',"--days-ago",type=int,default=30, help="The number of days ago to query for new projects that are billed to the org specified by --org.")
parser.add_argument('-o',"--org",required=True,help="Limits the project search to only those that belong to the specified DNAnexus org. Should begin with 'org-'.")

args = parser.parse_args()
days_ago = args.days_ago
days_ago = "-" + str(days_ago) + "d"
org = args.org

if not org.startswith("org-"):
	parser.error("Argument --org must be passed a value prefixed with 'org-'.")

dx_projects = dxpy.find_projects(created_after=days_ago,billed_to=org)
#dx_projects is a generater of dicts of the form {u'permissionSources': [u'user-nathankw'], u'public': False, u'id': u'project-BzzP0j0070XJ8vkJpk0Vgkb7', u'level': u'ADMINISTER'}
for i in dx_projects:
	proj_id = i["id"]
	proj = dxpy.DXProject(proj_id)
	APP.run(app_input={},project=proj_id,folder=RAW_DATA_FOLDER)
	print(proj.name + " (" + proj_id + ")")
