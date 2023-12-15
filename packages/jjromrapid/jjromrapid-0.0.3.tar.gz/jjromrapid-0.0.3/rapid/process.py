"""
rapid - process.py
Copyright 2023 Jerome Gasperi
@author: jerome.gasperi@gmail.com
"""
import requests
import json
import os
import rapid.settings as settings

class ProcessAPI():
    
    def __init__(self, config=None):
        """
        Initialize Process class - access to resto OGC API Processes

        @params
            config          --  Superseed settings.config / environnment variables
                                Allowed variables are :
                                    RESTO_API_ENDPOINT
                                    RESTO_PROCESS_API_AUTH_TOKEN
                                    RESTO_PROCESS_API_S3_HOST
                                    RESTO_PROCESS_API_S3_BUCKET
                                    RESTO_PROCESS_API_S3_KEY
                                    RESTO_PROCESS_API_S3_SECRET
                                    RESTO_PROCESS_API_S3_REGION
        """
        
        self.config = {}
        
        configKeys = [
            'RESTO_API_ENDPOINT',
            'RESTO_PROCESS_API_AUTH_TOKEN',
            'RESTO_PROCESS_API_S3_HOST',
            'RESTO_PROCESS_API_S3_BUCKET',
            'RESTO_PROCESS_API_S3_KEY',
            'RESTO_PROCESS_API_S3_SECRET',
            'RESTO_PROCESS_API_S3_REGION'
        ]
        for key in configKeys:
            self.config[key] = os.environ.get(key) if os.environ.get(key) else settings.config[key]
            if config and key in config:
                self.config[key] = config[key]
        
        self.processAPIUrl = self.config['RESTO_API_ENDPOINT'] + '/oapi-p'
        
        
    def deploy(self, application_package):
        """
        Deploy input process as an Application Package to resto endpoint

        @params
            application_package     -- Application package
        """
        return requests.post(self.processAPIUrl + '/processes',
        	data=json.dumps(application_package),
        	headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + (self.config['RESTO_PROCESS_API_AUTH_TOKEN'] if self.config['RESTO_PROCESS_API_AUTH_TOKEN'] != None else 'none')
            }
        )

    def replace(self, process_id, application_package):
        """
        Replace process 

        @params
            process_id              -- Process identifier
            application_package     -- Application package
            
        """
        return requests.put(self.processAPIUrl + '/processes/' + process_id,
        	data=json.dumps(application_package),
        	headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + (self.config['RESTO_PROCESS_API_AUTH_TOKEN'] if self.config['RESTO_PROCESS_API_AUTH_TOKEN'] != None else 'none')
            }
        )
        
    def undeploy(self, process_id):
        """
        Undeploy process

        @params
            process_id              -- Process identifier
        """
        
        return requests.delete(self.processAPIUrl + '/processes/' + process_id,
        	headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + (self.config['RESTO_PROCESS_API_AUTH_TOKEN'] if self.config['RESTO_PROCESS_API_AUTH_TOKEN'] != None else 'none')
            }
        )
        
    def setJobStatus(self, process_id, status, progress=None):
        """
        Update the status of a process

        @params
            process_id              -- Process identifier
            status                  -- Status - one of "accepted", "running", "successful", "failed", "dismissed"
            progress                -- Progress of the running job (in %)
        """
        
        body = {
            'status': status
        }
        
        if progress:
            body['progress'] = progress
            
        return requests.put(self.processAPIUrl + '/processes/' + process_id,
            data=json.dumps(body),
        	headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + (self.config['RESTO_PROCESS_API_AUTH_TOKEN'] if self.config['RESTO_PROCESS_API_AUTH_TOKEN'] != None else 'none')
            }
        )