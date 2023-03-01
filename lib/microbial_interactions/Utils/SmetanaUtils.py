
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
        self.ws = Workspace(self.ws_url, token = config['token'])
        self.kbase_api = cobrakbase.KBaseAPI(config['token'])
        self.callback_url =os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)
        self.report = KBaseReport (self.callback_url)

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def delete_zip (self,path):
        dir_list = os.listdir(path)
        for j in dir_list:
            if j.endswith(".zip"):
                zipfilename = os.path.join(path,j)
                os.remove(zipfilename)
    def get_object_name(self, ref):
        x = self.ws.get_object_info3({"objects": [{"ref": ref}]})['infos'][0][1]
        return (x)

    def get_community_members(self, community_model):
        community_members = self.ws.get_object_subset([{
            'included': ['/provenance'],
            'ref': community_model
        }])[0]['provenance'][0]['method_params'][0]['fbamodel_id_list']
        return (community_members)


    def get_biomass(self, models):
        biomass_yields=dict()
        for model in models:
            for ex in model.exchanges:
                ex.bounds = (-100,100)
            model.objective = 'bio1'
            biomass_yields[str(model)] = model.slim_optimize()
        return (biomass_yields)


    def get_models(self, smetana_result):
        mro = smetana_result.get('mro')
        for pair in mro:
            model1, model2 = pair.split("--")
        return [str(model1), str(model2)]

    def generate_html(self, json_object, errors):
        # get the table HTML from the dataframe
        df = pd.json_normalize(json_object)
        table_html = df.to_html(table_id="table", classes="stripe" )

        error_string = "<p>"
        for j in errors:
            error_string += j + "</br>"
        error_string += "</p>"
        # construct the complete HTML with jQuery Data tables
        # You can disable paging or enable y scrolling on lines 20 and 21 respectively
        html = f"""
        <html>
        <header>
            <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
        </header>
        <body>
        {table_html}
        {error_string}
        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"><
/script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready( function () {{
                $('#table').DataTable({{
                    // paging: false,
                    // scrollY: 400,
                }});
            }});
        </script>
        </body>
        </html>
        """
        # return the html
        return html

    def test_pair(self, community_model_ref):
        try:

            community_members = self.get_community_members(community_model_ref)
            model1_ref = community_members[0]
            model2_ref = community_members[1]

            model1 = self.kbase_api.get_from_ws(model1_ref)
            model2 = self.kbase_api.get_from_ws(model2_ref)
            community_model = self.kbase_api.get_from_ws(community_model_ref)

      
            model_names = dict()
            model_names['model1'] = self.get_object_name(model1_ref)
            model_names['model2'] = self.get_object_name(model2_ref)
            model_names['community_model'] = self.get_object_name (community_model_ref)


            comm = MSSmetana([model1, model2], community_model)
            smetana_result=comm.all_scores()

            model1_model2_mro = ""
            model2_model1_mro = ""


            mro = smetana_result.get('mro')
            for pair in mro:
                name1, name2 = pair.split("---")
                val1,val2, val3 = mro[pair]
                if name1==model_names['model1']:
                    model1_model2_mro =  str(round(val1,2)) + " (" + str(val2) + "/" + str(val3) + ")"
                else:
                    model2_model1_mro =  str(round(val1,2)) + " (" + str(val2) + "/" + str(val3) + ")"


            mip = smetana_result.get("mip")

            rs = dict()
            rs['model1'] = str(model_names['model1'])
            rs['model2'] = str(model_names['model2'])
            rs['community_model'] = str(model_names['community_model'])
            rs['model1_model2_mro'] = model1_model2_mro
            rs['model2_model1_mro'] = model2_model1_mro
            rs['mip'] = mip

            biomass_yield = self.get_biomass([model1, model2, community_model]) 
            rs['biomass_yield_model1'] = round(biomass_yield[model_names['model1']],2)
            rs['biomass_yield_model2'] = round (biomass_yield[model_names['model2']], 2)
            rs['biomass_yield_community_model'] = round(biomass_yield[model_names['community_model']] , 2)

            return (rs)
        except Exception as e:
            community_model = self.get_object_name (community_model_ref)
            print(f"\n\nERROR:{e}")
            error = "Error calculating scores for "  + community_model + " (model1: " + self.get_object_name(model2_ref) + " / " + "model2:" + self.get_object_name(model2_ref) +  ")" + ":  " + str(e)
            return (error)
   
    def run_smetana (self, community_model_ref):
        result= self.test_pair(community_model_ref)
        print (result)
        return (result)


    def simplify_smetana_result(self, smetana_result):
        print (smetana_result)
    def write_to_file(self, smetana_batch_result, filex):
        json_object = json.dumps(smetana_batch_result, indent=4)
        with open(filex,  "w") as outfile:
           outfile.write(json_object)

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
