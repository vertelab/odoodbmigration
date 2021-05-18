#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:56:36 2021

Tools to query an Odoo server of the model relationships.

@author: simon
"""

#%% ---------------------------------------------------------------------------
import logging

import odoorpc

_logger = logging.getLogger(__name__)

#%% ---------------------------------------------------------------------------
DEFAULT_RELATION_FIELDS = ("create_uid","write_uid")
#%% ---------------------------------------------------------------------------
def get_relations(columns,required_only=True, ignore_default=True):
    '''
    Returns a list with keys of columns corresponding to DB relations.
    IE: Many2many, Many2one, One2many

    Parameters
    ==========
    columns : dict
        Dictionary as retrieved by _columns
    ignore_default : Boolean
        Ignore default relation fields (eg: create_/write_uid)
    required_only : Boolean
        Only follow required relations
    '''
    ret = []
    for k in columns.keys():
        if isinstance(columns[k],odoorpc.fields.Many2one) or\
            isinstance(columns[k],odoorpc.fields.Many2many) or\
            isinstance(columns[k],odoorpc.fields.One2many):
            if required_only and not columns[k].required:
                continue
            if ignore_default and k in DEFAULT_RELATION_FIELDS:
                continue
            ret.append(k)
    return ret
def get_required_fields(columns):
    '''
    Returns a list with keys of columns with required data.

    Parameters
    ==========
    columns : dict
        Dictionary as retrieved by _columns
    '''
    ret = []
    for k in columns.keys():
        try:
            if columns[k].required:
                ret.append(k)
        except AttributeError as e:
            _logger.debug(f"Unexpected AttributeError: {e.msg}")
            #pass
    return ret
def _model_dependencies(conn, model, visited, recursive_depth=None, follow_required=True,required_only=True, ignore_default=True):
    '''
    Recursively add a models dependency to the set visited.
    '''
    visited.add(model)  # There is likely a circular dependency back to the
                        # model itself so it makes sense to explicitly add a
                        # as depending on itself.
    if recursive_depth is not None and recursive_depth == 0:
        if follow_required:
            _model_dependencies(conn,model,visited,
                                required_only=True,
                                ignore_default=ignore_default)
        return
    # else:
    columns = conn.env[model]._columns
    relation_cols = get_relations(columns,required_only,ignore_default)

    for r in relation_cols:
        comodel = columns[r].relation
        if comodel not in visited:
            if recursive_depth == None:
                _model_dependencies(conn,comodel,visited,
                                follow_required=follow_required,
                                required_only=required_only,
                                ignore_default=ignore_default)
            else:
                _model_dependencies(conn,comodel,visited,
                                recursive_depth=recursive_depth-1,
                                follow_required=follow_required,
                                required_only=required_only,
                                ignore_default=ignore_default)
def model_dependencies(conn,model,recursive_depth=None, follow_required=True, required_only=True,ignore_default=True):
    '''
    Returns a list of models the input model depend on in the given db.

    Parameters
    ==========
    conn : odoorpc.ODOO
        Open connection to Odoo installation
    model : str
        model name to follow
    recursive_depth : int
        Maximum recursive depth
    follow_required : Boolean
        If the recursive depth should be ignored for required fields
    required_only : Boolean
        Only follow required relations
    ignore_default : Boolean
        Ignore default relation fields (eg: create_/write_uid)
    '''
    _logger.info(f"Getting dependencies for model {model}")
    dependencies = set()
    _model_dependencies(conn,model,dependencies,
                        recursive_depth,follow_required,
                        required_only,ignore_default)
    ret = list(dependencies)
    ret.sort()
    return ret
def model_primary_dependencies(conn,model,required_only=True,ignore_default=True):
    '''
    Calculate model parent dependencies to a depth of 1.

    Parameters
    ==========
    conn : odoorpc.ODOO
        Open connection to Odoo installation
    model : str
        model name to follow
    required_only : Boolean
        Only follow required relations
    ignore_default : Boolean
        Ignore default relation fields (eg: create_/write_uid)
    '''
    columns = conn.env[model]._columns
    relation_cols = get_relations(columns,required_only,ignore_default)
    ret = set()
    for r in relation_cols:
        ret.add(columns[r].relation)
    ret = list(ret)
    ret.sort()
    return ret
