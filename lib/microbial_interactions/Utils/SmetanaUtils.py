
#  define the environment path
import sys
#sys.path.append("/kb/module/lib")
import pandas as pd

import time
import os
import errno
import uuid
import shutil
import stat
import gzip
from zipfile import ZipFile, ZIP_DEFLATED

import json
import os
from matplotlib import pyplot
from numpy import array
# import the KBase
import cobrakbase
# prevent excessive warnings
from time import process_time
from modelseedpy.community.mssmetana import MSSmetana
from modelseedpy.core.exceptions import ModelError

from installed_clients.WorkspaceClient import Workspace
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport


class SmetanaUtils:


    def __init__(self, config, params):
        self.ws_url = config["workspace-url"]
        self.workspace_name = params['workspace_name']
        self.ws = Workspace(self.ws_url)
        self.callback_url =os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)
        self.report = KBaseReport (self.callback_url)


    def create_html_report(self, output_dir, workspace_name):
        '''
        function for creating html report
        :param callback_url:
        :param output_dir:
        :param workspace_name:
        :return:
        '''

        report_name = 'smetana_report_' + str(uuid.uuid4())

        report_shock_id = self.dfu.file_to_shock({'file_path': output_dir,
                                            'pack': 'zip'})['shock_id']

        html_file = {
            'shock_id': report_shock_id,
            'name': 'index.html',
            'label': 'index.html',
            'description': 'HTML report for Antismash'
            }

        report_info = self.report.create_extended_report({
                        'direct_html_link_index': 0,
                        'html_links': [html_file],
                        'report_object_name': report_name,
                        'workspace_name': workspace_name
                    })
        return {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }

    def run_smetana_batch (self, community_models, json_output_path, html_output_path):
        smetana_batch_result = list()
        errors = list()
        for j in community_models:
           rs = self.run_smetana(j)
           if "Error" in rs:
             errors.append(rs)
           else:
               smetana_batch_result.append(rs)
        self.write_to_file(smetana_batch_result, json_output_path) 
        html = self.generate_html(smetana_batch_result, errors)
        with open(html_output_path,  "w") as outfile:
           outfile.write(html)
    




if __name__=="__main__":
    params = dict()
    params['workspace_name'] = 'pranjan77:narrative_1650064809467'

    config = dict()
    config['workspace-url']="https://kbase.us/services/ws"
    token="CP27V4DOUKJMJFDOOATYYMPWNISD266S"

    config['token'] = token
    SMUtils = SmetanaUtils(config, params)
    community_models=[ "114731/94/1", "114731/92/1" ]
    j1 = SMUtils.run_smetana_batch(community_models, "/kb/module/work/output.json", "/kb/module/work/output.html")











"""

# load the pair
#YR343 = kbase_api.get_from_ws("Pantoea_YR343_pacbio_v2.RAST.fbamodel", 114731)
#CF313 = kbase_api.get_from_ws("Variovorax_CF313_pacbio_v2.RAST.fbamodel",114731)
#YR343_CF313_model = kbase_api.get_from_ws("YR343-CF313",114731)
#d = test_pair(YR343, CF313, YR343_CF313_model)
#print (d)
#models = [YR343, CF313, YR343_CF313_model]
#biomass_yields=dict()
#for model in models:
  biomass_yields[model] = model.slim_optimize()

print (biomass_yields)





CF142 = kbase_api.get_from_ws("Rhizobium_CF142_pacbio_v2.RAST.fbamodel", 114731)
BC15 = kbase_api.get_from_ws("Bacillus_sp._bc15.RAST.fbamodel", 114731)
CF142_BC15_model = kbase_api.get_from_ws("CF142-BC15", 114731)
models = [CF142, BC15, CF142_BC15_model]
biomass_yields=dict()
for model in models:
  biomass_yields[model] = model.slim_optimize()

print (biomass_yields)


CF402 = kbase_api.get_from_ws("Duagnella_sp_CF402.RAST.fbamodel", 114731)
CF313 = kbase_api.get_from_ws("Variovorax_CF313_pacbio_v2.RAST.fbamodel",114731)
CF402_CF313_model = kbase_api.get_from_ws("CF402-CF313", 114731)


models = [CF402, CF313, CF402_CF313_model]
biomass_yields=dict()
for model in models:
  biomass_yields[model] = model.slim_optimize()

print (biomass_yields)



GM17 = kbase_api.get_from_ws("Pseudomonas_GM17_pacbio_v2.RAST.fbamodel", 114731)
CF142 = kbase_api.get_from_ws("Rhizobium_CF142_pacbio_v2.RAST.fbamodel", 114731)
GM17_CF142_model = kbase_api.get_from_ws("GM17-CF142", 114731)

models = [GM17, CF142, GM17_CF142_model]
biomass_yields=dict()
for model in models:
  biomass_yields[model] = model.slim_optimize()

print (biomass_yields)



GM17 = kbase_api.get_from_ws("Pseudomonas_GM17_pacbio_v2.RAST.fbamodel", 114731)
YR343 = kbase_api.get_from_ws("Pantoea_YR343_pacbio_v2.RAST.fbamodel", 114731)
GM17_YR343_model = kbase_api.get_from_ws("YR343-GM17", 114731)

models = [GM17, YR343, GM17_YR343_model]
biomass_yields=dict()
for model in models:
  biomass_yields[model] = model.slim_optimize()

print (biomass_yields)

"""
