
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
            'description': 'HTML report for CommScores'
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




