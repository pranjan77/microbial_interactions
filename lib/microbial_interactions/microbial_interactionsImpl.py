# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid
from microbial_interactions.Utils.SmetanaUtils import SmetanaUtils
from installed_clients.KBaseReportClient import KBaseReport
from commscores import CommScores
import cobrakbase

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
        models_lists = []
        for model_dic in params["model_list"]:
            models_lists.append([kbase_api.get_from_ws(model) for model in model_dic["member_models"]])
        if len(models_lists) == 1:  models_lists = models_lists[0]
        ## media
        media = [kbase_api.get_from_ws(medium) for medium in params['media']]
        # run the CommScores API
        df, mets = CommScores.kbase_output(models_lists, kbase_obj=kbase_api, environments=media)
        reportHTML = CommScores.html_report(df, mets, index_html_path)

        reportUtils = ReportUtils(self.config, params)
        output = reportUtils.create_html_report(result_dir, params['workspace_name'])

        print(output)
        #END run_microbial_interactions

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_microbial_interactions return value ' +
                             'output is not type dict as required.')
        # return the results
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
