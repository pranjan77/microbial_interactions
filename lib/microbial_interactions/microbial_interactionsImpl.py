# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid
from microbial_interactions.Utils.SmetanaUtils import SmetanaUtils
from installed_clients.KBaseReportClient import KBaseReport
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
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
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
        # return variables are: output
        #BEGIN run_microbial_interactions

        result_dir = os.path.join(self.shared_folder,  str(uuid.uuid4()))
        print (result_dir)
        self._mkdir_p(result_dir)
        smetana_json_path = os.path.join(result_dir, "smetana_output.json")
        index_html_path = os.path.join(result_dir, "index.html")

        config = dict()
        config['workspace-url']="https://kbase.us/services/ws"
#        token="CP27V4DOUKJMJFDOOATYYMPWNISD266S"

        config['token'] = ctx['token']
        SMUtils = SmetanaUtils(config, params)
        j1 = SMUtils.run_smetana_batch(params['community_models'], smetana_json_path, index_html_path)
        output = SMUtils.create_html_report(result_dir, params['workspace_name'])

        print (output)
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
