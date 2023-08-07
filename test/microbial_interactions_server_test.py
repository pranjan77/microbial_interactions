# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from microbial_interactions.microbial_interactionsImpl import microbial_interactions
from microbial_interactions.microbial_interactionsServer import MethodContext
from microbial_interactions.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class microbial_interactionsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('microbial_interactions'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'microbial_interactions',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = microbial_interactions(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        params1 = {
            'workspace_name':'pranjan77:narrative_1650064809467',
            "member_models":[ "137367/1887/1", "137367/2417/1", "137367/1925/1" ],
            "media": ["137367/1656/1"]
        }

        params2 = {
            'workspace_name':'pranjan77:narrative_1684888643360',
            "member_models": ["70893/18/1", "70893/16/1"], 
            "media": ["70893/15/1"]
        }
        params = params1

        ret = self.serviceImpl.run_microbial_interactions(self.ctx, params)
