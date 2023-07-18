# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid
from microbial_interactions.Utils.SmetanaUtils import SmetanaUtils
from installed_clients.KBaseReportClient import KBaseReport
from modelseedpy import MSCommScores, commscores_report
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
        # return variables are: output
        #BEGIN run_microbial_interactions

        print (params)



        media_objs = params['media']
        input_kbase_models = params['member_models']
        token = ctx['token']
        kbase_api = cobrakbase.KBaseAPI(token)

        print (kbase_api)


        print (media_objs)
        print (input_kbase_models)

        result_dir = os.path.join(self.shared_folder,  str(uuid.uuid4()))
        print(result_dir)
        self._mkdir_p(result_dir)
        index_html_path = os.path.join(result_dir, "index.html")

        models = [kbase_api.get_from_ws(model) for model in input_kbase_models]
        media = [kbase_api.get_from_ws(medium) for medium in media_objs]

        print ("#############Models########\n")
        print (models)
        print ("##############Media#########\n")
        print (media)

        df, mets = MSCommScores.kbase_output(models, kbase_obj=kbase_api, environments=media)

        print (df)

        reportHTML = commscores_report(df, mets, index_html_path)

        

        SMUtils = SmetanaUtils(self.config, params)
        output = SMUtils.create_html_report(result_dir, params['workspace_name'])

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
