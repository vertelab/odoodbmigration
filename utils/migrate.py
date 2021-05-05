#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 10:23:32 2021

Tools to actually perform the migration.

@author: Simon Rundstedt, Carl-Magnus Arvidsson, Han Wong
"""
#%% 

import odoorpc
import logging

_logger = logging.getLogger(__name__)

#%%

def migrate_data(source, target, model, ids,fields):
    '''
    Migrate selected fields of model from source to target database.
    
    Parameters
    ==========
    source : 
        Open connection to source database
    target : 
        Open connection to target database
    model : str
        Name of model to migrate
    fields : dict str->str
        Fields of the model to migrate on the format {"oldfield":"newfield"}
    '''    
    for source_model in source.env[model].search([]):
        source_fields = source.env[model].read(source_model, fields)
        target_fields = {fields[key]: source_fields[key] for key in fields}
        create_record_and_xml_id(model, target_fields, source_model)

#%%

class FieldToField():
    '''
    Class responsible for translating fields between source and target.
    '''
    pass

class TransferOperation():
    '''
    The class actually doing the transfer.
    '''
    
    def __init__(self, configfile, tr, field2field):
        '''
        Parameters
        =========
        configfile : str
            Configfile to get connections from
        tr : TransferRequest
            TransferRequest to perform.
        field2field : Field2Field
            Map between field names for source and target DB.
        
        '''
        self.config = configfile
    
        self.transfer_requests = tr
        self.field2field = field2field
        
    def run(self):
        '''
        Connect to source and target databases and transfer data.
        '''
        raise NotImplementedError("This class is a skeleton")