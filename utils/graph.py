#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 08:32:32 2021

Assorted tools to extract and convert Odoo relations to a networkx graph.

networkx supply tools and options to explore and help visualizing the graphs.

@author: Simon Rundstedt
"""

#%% ---------------------------------------------------------------------------
import networkx as nx
# import odoorpc

if __name__ == "__main__":
    import relationtools as rt
else:
    from . import relationtools as rt
#%% ---------------------------------------------------------------------------

# By Model
def _get_default_model_filter(conn):
    '''
    Retrieve default model filter depending on Odoo version.
    '''
    # This filter excludes transient models
    if conn.version[:3] == "8.0":
        return [["osv_memory","=",False]]
    elif conn.version[:4] == "14.0":
        return  [["transient","=",False]]
    else: # Todo add more Odoo-versions as needed
        return  [["transient","=",False]]

def get_graph(conn, models=None, required_only=False,
              search=None,
              ignore_default=True):
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
        if not search:
            search = _get_default_model_filter(conn)
        model_ids = conn.env["ir.model"].search(search) # Might need some small tweak
        m = conn.env["ir.model"].read(model_ids,["model"])
        g.add_nodes_from({ model["model"] for model in m }) # Set force single entry per model but remove any order.
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

def get_ordered_graph(conn, models=None, required_only=False,
                      search=None,
                      order="model asc", ignore_default=True):
    '''
    Generate an orderered directional graph of the model relations in the
    target DB described by conn.
    
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
    order : str
        (Optional) String to pass on to the odoo search. Only used if models is None.
    '''
    m = models
    g = nx.OrderedDiGraph()
    if models is None:
        if not search:
            search = _get_default_model_filter(conn)
        model_ids = conn.env["ir.model"].search(search,order=order) # Might need some small tweak
        m = conn.env["ir.model"].read(model_ids,["model"])
        g.add_nodes_from((model["model"] for model in m ))
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
    # Sample usage
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
# By module
def get_ordered_module_graph(conn, modules=None,installed_only=True,search=[],order="name asc"):
    '''
    Build an ordered nx-graph of the Odoo modules.
    
    Parameters
    ==========
    conn : ODOO
        Open odoorpc connection
    modules : Iterable
        (Optional) Iterable with modules as strings. None mean all modules in
        ir.module.module
    installed_only : boolean
        (Optional) Whether or not to include installed modules only in result.
        Appends to the search domain.
    search : Odoo-search domain
        (Optional) Odoo search domain. Only used if modules is None.
    order : str
        (Optional) Odoo order string. Only used if models is None.
    '''
    m = modules
    g = nx.OrderedDiGraph()
    if modules is None:
        search += [["state",("=" if installed_only else "!="),"installed"]] if installed_only else [];
        modules_ids = conn.env["ir.module.module"].search(search,order=order) # Might need some small tweak
        m = conn.env["ir.module.module"].read(modules_ids,["name"])
        g.add_nodes_from((module["name"] for module in m ))
    else:
        g.add_nodes_from(m)

    remove_list = [] # Contain modules that couldn't be fetched.
    for n in g.nodes():
        try: # <- If some module is not reachable (happens with model)
            self_id = conn.env["ir.module.module"].search([["name","=",n]])
            self_rs = conn.env["ir.module.module"].browse(self_id)
            # g.add_edges_from( ( (n,r) for r in relations ) ) # Removed: Adds node r if it is not already in g.nodes
            for d in self_rs.dependencies_id:
                 print(d.depend_id.name)
                 if d.name in g:
                     g.add_edge(n,d.name)
                 # else: # Don't add
        except:
            # Most likely conn.env[r] failed to get the module as a usable module
            remove_list.append(n) # We can't remove nodes in the loop delay until after loop

    g.remove_nodes_from(remove_list)
    return g
"""
    # Sample usage
    CONNECTION = "barney"
    OUTFILE = "/home/simon/odoo.dot"
    
    #MODULES = ["project","base","project_dermanord","project_scrum","ecommerce","stock"]
    MODULES=None
    
    # conn = odoorpc.ODOO.load(CONNECTION) # Take minutes to complete, haven't optimized.
    conn = odoorpc.ODOO.load(CONNECTION)
    g = get_ordered_module_graph(conn, MODULES) # Can take a long time.
    nx.drawing.nx_agraph.write_dot(g,OUTFILE) # nx can plot by itself too, without export 
    
    conn.logout()
    '''
    From terminal:
        sudo apt install graphviz # IF not installed
        dot -Tsvg odoo.dot -o module.svg
    '''
"""