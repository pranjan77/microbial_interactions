# -*- coding: utf-8 -*-
#BEGIN_HEADER
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace
from installed_clients.DataFileUtilClient import DataFileUtil

from commscores import CommScores
from pandas import concat
import cobrakbase
import logging
import uuid
import os


#END_HEADER


class microbial_interactions:
    '''
    Module Name:
    microbial_interactions

    Module Description:
    A KBase module: microbial_interactions
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:pranjan77/microbial_interactions.git"
    GIT_COMMIT_HASH = "94c873b9d99f158c8692a3737cca7a6567eeabd6"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.ws_url = config["workspace-url"]
        self.dfu = DataFileUtil(self.callback_url)
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.config = config

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

        #END_CONSTRUCTOR
        pass

    @staticmethod
    def create_html_report(output_dir, workspace_name):
        callback_url = os.environ['SDK_CALLBACK_URL']
        report_info = KBaseReport(callback_url).create_extended_report({
            'direct_html_link_index': 0,
            'html_links': [{
                'shock_id': DataFileUtil(callback_url).file_to_shock(
                    {'file_path': output_dir, 'pack': 'zip'})['shock_id'],
                'name': 'index.html',
                'label': 'index.html',
                'description': 'HTML report for CommScores'
            }],
            'report_object_name': 'smetana_report_' + str(uuid.uuid4()),
            'workspace_name': workspace_name
        })
        return {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }

    def run_microbial_interactions(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        token = ctx['token']
        kbase_api = cobrakbase.KBaseAPI(token)
        # package the output report
        result_dir = os.path.join(self.shared_folder,  str(uuid.uuid4()))
        print(result_dir)
        self._mkdir_p(result_dir)
        index_html_path = os.path.join(result_dir, "index.html")

        # process the App parameters for CommScores API arguments
        ## models

        ws = Workspace(self.ws_url)

        modelset_refs = params["member_modelsets"]
        model_lists_ids = list ()
        for ref in modelset_refs:
            modellist = list(ws.get_objects2({'objects': [{"ref": ref}]})['data'][0]['data']['instances'].keys())
            model_lists_ids.append(modellist)

        models_lists = [[kbase_api.get_from_ws(model) for model in model_list] for model_list in model_lists_ids]
        if len(models_lists) == 1:  models_lists = models_lists[0]
        ## media
        media = [kbase_api.get_from_ws(medium) for medium in params['media']]
        print("#############Models########\n", models_lists, "##############Media#########\n", media)

        # run the CommScores API
        if len(models_lists) == 1 or params["inter_model_assessment"] == "intra":
            dfs, allmets = [], []
            for model_list in models_lists:
                df, mets = CommScores.report_generation(model_list, kbase_obj=kbase_api, environments=media,
                                                        cip_score=params["cip_score"], costless=params["costless"],
                                                        anme_comm=params["skip_questionable_models"])
                dfs.append(df)  ;  allmets.append(mets)
            combined_df = concat(dfs, axis=0).reset_index(drop=True)
            reportHTML = CommScores.html_report(combined_df, mets, index_html_path)
        else:
            df, mets = CommScores.report_generation(models_lists, kbase_obj=kbase_api, environments=media,
                                                    cip_score=params["cip_score"], costless=params["costless"],
                                                    anme_comm=params["skip_questionable_models"])
            reportHTML = CommScores.html_report(df, mets, index_html_path)
        output = microbial_interactions.create_html_report(result_dir, params['workspace_name'])
        print(output)
        # NOTE: At some point might do deeper type checking...
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
