#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 10:28:54 2021

Tools to compare two different Odoo server installation

@author: simon
"""


#%% ---------------------------------------------------------------------------
import logging

import odoorpc
import pandas

_logger = logging.getLogger(__name__)

#%% ---------------------------------------------------------------------------

def compare_field_names(source,target,model):
    '''
    '''
    src_col   = source.env[model]._columns
    src_col_k = src_col.keys()
    
    trg_col = target.env[model]._columns
    trg_col_k = trg_col.keys()

    src_unique = []
    for k in src_col_k:
        if k not in trg_col_k:
            src_unique.append(k)
    trg_unique = []
    for k in trg_col_k:
        if k not in trg_col_k:
            trg_unique.append(k)
    return src_unique, trg_unique
        

class TableComparisonReport():
    '''
    Rough draft that currently only detect field name mismatches.
    
    Class to help comparing the same model across two different DB's in order
    to help determine if transfer of data can happen automatically and what
    manual steps need to be taken.
    
    General notes
    =============
    A field can be transferred automatically if:
        * field name match in both DB's.
        * field data types match in both DB's.
        * field doesn't exist in target DB
        * a required field in target need to be required in source too
        
    TODO:
        * Put a complete report in a Pandas DataFrame? That way the result is
        fairly easy to slice and dice for information.
            * mismatch count in class is still useful.
    '''
    def __init__(self, source, target, model):
        '''
        source, target open rpc-connections to DB's.
        model - model to compare.
        '''
        self.source = source
        self.target = target
        
        # 
        self.done = False

        self.mismatch_cnt = 0
        self.shared_fields = None
        self.unique_source_fields = None
        self.unique_target_fields = None
        
        # Report
        
    def compare_field_names(self,model):
        '''
        '''
        src_col   = self.source.env[model]._columns
        src_col_k = src_col.keys()
        
        trg_col = self.target.env[model]._columns
        trg_col_k = trg_col.keys()
    
        self.shared_fields = set()
        self.unique_source_fields = set()
        self.unique_target_fields = set()
        
        for k in src_col_k:
            if k not in trg_col_k:
                self.unique_source_fields.add(k)
                self.mismatch_cnt += 1
            else:
                self.shared_fields.add(k)
        for k in trg_col_k:
            if k not in trg_col_k:
                self.unique_target_fields.add(k)
                self.mismatch_cnt += 1
            else:
                self.shared_fields.add(k) 