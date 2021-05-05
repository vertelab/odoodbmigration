#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 08:58:25 2021

Classes and methods to help build and perform transactions between two Odoo
installations.

Work in progress:
    * It will likely become slow for large transfers. Maybe use an INDEXed DB
    or something to store the id's in?

@author: Simon Rundstedt
"""

import odoorpc
from ..utils import relationtools as rt

import logging
_logger = logging.getLogger(__name__)

#%% Helper functions

#%% Basic transfers requests (target agnostic)
class TransferModelRequest():
    '''
    Representation of the fields and specific ID's to transfer for a given
    model.
    '''
    def __init__(self, model, ids=set(), fields=None):
        '''
        
        Parameters
        ==========
        model : str
            Model to transfer as identified by _name
        ids : Iterable
            ID's of the rows to transfer. None mean no ID's. 
        fields : Iterable
            Iterable of fields's to transfer. If set to None all fields will be
            transferred.
        '''
        self.model = model
        if fields:
            self.fields = set(fields)
        else:
            self.fields = None # None mean all fields
        self.ids = set(ids) # Empty set mean no ID's
        
    def append(self, tmr):
        '''
        Append another TransferModelRequest of the same model to self
        '''
        if tmr.model != self.model:
            raise ValueError("Input TransferModelRequest of wrong model: {} Expected: {}".format( tmr.model, self.model))
        # else:
        self.append_fields(tmr.fields)
        self.append_ids(tmr.ids)
         
    def append_fields(self, fields):
        '''
        Parameters
        ==========
        fields : Iterable
            Iterable of fields's to transfer. If set to None all fields will be
            transferred.
        '''
        if not fields:
            self.fields = None # Set
        else:
            self.fields = self.fields.union(set(fields))
            
    def append_ids(self, ids):
        '''
        Parameters
        ==========
        ids : Iterable
            Iterable of ID's to transfer
        '''
        print(self.ids.union(set(ids)))
        self.ids = self.ids.union(set(ids))


class TransferRequest():
    '''
    Representation of the models, fields and specific ID's to transfer.
    '''
    
    def __init__(self, tmrs=None):
        '''
        Parameters
        ==========
        tmr: Iterable
            (Optional) List of TransferModelRequest's
        '''
        self.tmr = dict() # Model specific TransferModelRequest
        if tmrs:
            for t in tmrs:
                self.tmr[t.model] = t

    def __getitem__(self, model):
        '''
        Shorthand to retrieve the TransferModelRequest for model model or None. 
        '''
        return self.tmr.get(model,None)

    def append(self, tr):
        '''
        Append TransferRequest to self
        '''
        for t in tr.tmr:
            self.append_tmr(tr.tmr[t])

    def append_tmr(self,tmr):
        '''
        Parameters
        ==========
        tmr: TransferModelRequest
            Model specific request to append to self
        '''
        t = self.tmr.get(tmr.model, None)
        if t:
            self.tmr[tmr.model].append(tmr)
        else:
            self.tmr[tmr.model] = t
#%% Target specific stuff
#            
## Default rules for fields to include
#RR_DEFAULTRULE = {
#    "nonrelational": "all",
#    "relational": "required",
#    "depth": None ,         # How deep relational fields should be followed.
#    "followrequired": True, # Whether or not to follow required relations, overriding depth for required relations.
#    "list" : [], # If either nonrelational or relational are not defined or defined as list.
#    "blacklist" : ["create_date","create_uid","write_date","write_uid"] # Blacklist optional  
#}
## Default rules for fields to include
#RR_DEFAULTFOLLOWREQUIRED = {
#    "nonrelational": "required",
#    "relational": "required",
#    "depth": None ,         # How deep relational fields should be followed.
#    "followrequired": True, # Whether or not to follow required relations, overriding depth for required relations.
#    "list" : [], # If either nonrelational or relational are not defined or defined as list.
#    "blacklist" : ["create_date","create_uid","write_date","write_uid"] # Blacklist optional  
#}
#class ModelRequestRules():
#    '''
#    Basically a namespace to hold rules on a model level.
#    '''
#    def __init__(self, model, rules, defaultrule=RR_DEFAULTRULE, default_followrequired=RR_DEFAULTFOLLOWREQUIRED):
#        '''    
#        {
#             *nonrelational: "list|required|all"
#             *relational: "list|required|all",
#             *depth: 0 ,
#             *followrequired: 0
#             *list : [] # If either nonrelational or relational are not defined or defined as list.
#             *blacklist : ["",""] # Blacklist optional
#        }
#        '''
#        self.model = model
#        
#        self.followrequire_rules = default_followrequired
#        # Field rules:
#        # Defining defaults
#        # By list
#        self.list = defaultrule["list"]
#        self.blacklist = defaultrule["blacklist"]
#
#        # By normal fields
#        self.nonrelational = defaultrule["nonrelational"]
#
#        # By relational
#        self.relational = defaultrule["relational"]
#        self.depth = defaultrule["depth"] # None - no limit  
#        self.followrequired = defaultrule["followrequired"] #
#        
#        
#        # Overriding defaults:
#        keys = rules.keys()
#        # Trusting the format is right
#        if "nonrelational" in keys:
#            self.nonrelational = rules["nonrelational"]
#        if "relational" in keys:
#            self.relational = rules["relational"]
#        if "depth" in keys:
#            self.relational = rules["depth"]
#        if "followrequired" in keys:
#            self.relational = rules["followrequired"]
#        if "list" in keys:
#            self.relational = rules["list"]
#        if "blacklist" in keys:
#            self.relational = rules["blacklist"]
#
#    def get_fields(self,conn,curr_depth=None):
#        '''
#        Get the fields for the current model as described by the rules in self.
#        
#        Parameters
#        ==========
#        conn : 
#            Open odoorpc connection to source database
#        '''
#        # Depth check
#        tmprulestorage = {}
#        if curr_depth > self.depth:
#            if self.followrequired:
#                # Temporarily change rule fetch required data
#                # TODO: Continue from here
#                pass
#            else:
#                return []
#        # 
#        dbfields = conn.env[self.model]._columns.keys()
#        ret = []
#        for f in dbfields:
#            if self.field_in_rule(conn,f):
#                ret.append(f)
#    def field_in_rule(self,conn,field):
#        '''
#        Checks the field is valid according the rules in self.
#        
#        Parameters
#        ==========
#        conn : 
#            Open odoorpc connection to source database
#        '''
#        columns = conn.env[self.model]._columns
#        # Sanity check - Case 0
#        if field not in columns.keys():
#            raise ValueError(f"Field {field} not present among model {self.model} columns.")
#
#        # Normal checks
#        if field in self.list:
#            return True # Case 1: In whitelist
#        if field in self.blacklist:
#            return False # Case 2: In blacklist
#
#        relational_fields = rt.get_relations(columns,
#                             required_only=(self.relational == "required"),
#                             ignore_default=False) # Covered by blacklist
#        if self.relational != 'list' and field in relational_fields: # Cover both "all" and "required" together with row above.
#            return True # Case 3,4: Relational + Required (depending on relational search options) 
#        all_relational_fields = rt.get_relations(columns,
#                             required_only=False,
#                             ignore_default=False) # Covered by blacklist
#        if field not in all_relational_fields:
#            # With sanity check -> field is not relational.
#            if self.nonrelational == "all":
#                return True # Case 5: field is not relational or in blacklist (or explicitely in whitelist)   
#            elif self.nonrelational == "required" and field in rt.get_required_fields(c):
#                return True # Case 6: Like 5 but restricted to required fields.
#            else: # list only:
#                return False # Case 7: We only want fields in whitelist.
#        
#        _logger.debug("MRR: Didn't know we could end up here.")
#        return False
#            
#
#class RequestRules():
#    '''
#    Basically a namespace to hold rules on what fields to transfer and how to
#    traverse relations.
#    '''
#    def __init__(self, rulesdict, default=RR_DEFAULTRULE):
#        '''
#        Parameter
#        =========
#        rulesdict : dict
#            Dictionary with models as keys and values rules according to
#            ModelRequestRules() . A rule with key 'default' overrides the
#            other settings of the
#        '''
#        self.defaultrule = default
#        self.mrr = dict()
#        for model in rulesdict.keys():
#            if model != "default":
#                self.mrr["model"] = rulesdict[model]
#            else:
#                self.defaultrule = rulesdict[model]
#    def __getitem__(self, model):
#        '''
#        Get rules for model model.
#        '''          
#        self.mrr[model]
#    def validate_rules_dict(rulesdict):
#        '''
#        '''
#        _logger.warn("validate_rules_dict is not implemented yet")
#        return True
#class TransferRequestFactory():
#    '''
#    Factory for auto-magically building transfer orders
#    '''
#    def __init__(self, configfile):
#        '''
#        '''
#        self.config = configfile
#        self.source = odoorpc.ODOO.load("source", rc_file=self.config)
#    
#    def login(self):
#        '''
#        Mostly for completeness.
#        '''
#        self.source = odoorpc.ODOO.load("source", rc_file=self.config)
#    def logout(self):
#        '''
#        '''
#        self.source.logout()
#     
#    def _recursive_btr(self, model,ids,rules,curr_depth=None):
#        '''
#        Assumes self.source is logged in.
#        '''
#        # Build requst for this model
#        fields = rules[model].get_fields(self.source)    
#        tmr = TransferModelRequest(model, ids, fields)
#
#        # Append requests for children according to rules:
#        columns = self.source.env[model]._columns
#        relational_fields = rt.get_relations(columns,False,False) # False,False since rules take care of filtering
#        
#
#
#    def recursive_build_transfer_request(self, model, ids,rulesdict):
#        '''
#        Build a transfer request recursively according to the given rules.
#        '''
#        rules = RequestRules(rulesdict)
#        tr = self._recursive_btr(model,ids,rules,curr_depth = 0)