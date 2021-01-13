#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 12:53:58 2021

General purpose file for making small atomic functionalities.

@author: simon
"""

#%% ---------------------------------------------------------------------------
import logging

import odoorpc

import utils.relationtools as rt

_logger = logging.getLogger(__name__)
#%% ---------------------------------------------------------------------------
source_params = {
            "host" : "HOST",
            "port" : 8069,
            "db"   : "DATABASE",
            "user" : "admin",
            "password"  : "PASSWORD" 
        }



#%% ---------------------------------------------------------------------------

conn = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
conn.login(source_params["db"],login=source_params["user"],password=source_params["password"])

## To depth 1
model = "res.partner"
required_only  = False
ignore_default = True
dependencies = rt.model_primary_dependencies(conn,model,required_only=required_only,ignore_default=ignore_default)
print(dependencies)

## Recursive
required_only  = False
ignore_default = True
dependencies = rt.model_dependencies(conn,model,required_only=required_only,ignore_default=ignore_default)

dependencies_count = []
for d in dependencies:
    dependencies_count.append([d, len(rt.model_dependencies(conn,d,required_only=required_only,ignore_default=ignore_default))])
    dependencies_count.sort(key=lambda E: E[1])
print(dependencies)
## Recursive to set depth
rec_depth = 2
required_only  = True
ignore_default = True
dependencies = rt.model_dependencies(conn,model,recursive_depth=rec_depth,required_only=required_only,ignore_default=ignore_default)

dependencies_count = []
for d in dependencies:
    dependencies_count.append([d, len(rt.model_dependencies(conn,model,recursive_depth=rec_depth,required_only=required_only,ignore_default=ignore_default))])
    dependencies_count.sort(key=lambda E: E[1])
print(dependencies)

conn.logout()
