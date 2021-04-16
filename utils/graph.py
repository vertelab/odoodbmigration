#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 08:32:32 2021

@author: simon
"""

#%% ---------------------------------------------------------------------------
import networkx as nx
# import odoorpc

import relationtools as rt
#%% ---------------------------------------------------------------------------


def get_graph(conn, models=None, required_only=False, search=[], ignore_default=True):
    '''
    Generate directional graph of the model relations in the target DB
    described by conn.
    
    Dev:
        Default search-criteria is there to match actual models. The model
        field contain pseudo-models and other non model.model or
        transient.model that can't be reached with conn.env["some.model"]
        The model field still always yield the model name which the name field
        not always do (it sometime ¨retrieve the human readable name of a model)
    
    Parameters
    ==========
    conn : ODOO
        Open odoorpc connection
    models : Iterable
        (Optional) Iterable with models as strings. None mean all models in ir.model
    required_only : Boolean
        (Optional) Add required relational fields only
    search : Odoo-search domain
        (Optional) Odoo search domain. Only used if models is None.
    '''
    m = models
    g = nx.DiGraph()
    if models is None:
        model_ids = conn.env["ir.model"].search(search,order="id asc") # Might need some small tweak
        m = conn.env["ir.model"].read(model_ids,["model"])
        g.add_nodes_from({ model["model"] for model in m })
    else:
        g.add_nodes_from(m)
    
    remove_list = [] # Contain models to remove
    for n in g.nodes():
        try: # Some models in ir.model throw errors when put in env[]
            relations = rt.model_primary_dependencies(conn, n,
                                                  required_only=required_only,
                                                  ignore_default=ignore_default)
            # g.add_edges_from( ( (n,r) for r in relations ) ) # Removed: Adds node r if it is not already in g.nodes
            for r in relations:
                 if r in g:
                     g.add_edge(n,r)
                 # else: # Don't add
        except:
            # Most likely conn.env[r] failed to get the model as a usable model
            remove_list.append(n) # We can't remove nodes in the loop
        
    g.remove_nodes_from(remove_list)
    return g


'''
model_list = ['stock.picking',
 'stock.move',
 'res.users',
 'sale.order',
 'sale.order.line',
 'account.account']

g = get_graph(conn,model_list)
nx.draw(g)
print(list(nx.shortest_simple_paths(g,"account.account","stock.move")))
'''