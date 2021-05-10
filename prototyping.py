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

#%% ---------------------------------------------------------------------------
# Modified demo from bokeh.io about networkx
import networkx as nx

from bokeh.io import output_file, show
from bokeh.models import (BoxSelectTool,WheelZoomTool, Circle, EdgesAndLinkedNodes, HoverTool,
                          MultiLine,NodesOnly, NodesAndLinkedEdges, Plot, Range1d, TapTool,)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

import utils.graph as graph


plot = Plot(plot_width=2560, plot_height=1440,
            x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
plot.title.text = "Graph Interaction Demonstration"

tooltips = [("Index", "@index")]
my_hover = HoverTool(tooltips=tooltips)
plot.add_tools(my_hover, TapTool(), BoxSelectTool(),WheelZoomTool())

#G = graph.get_ordered_graph(conn,required_only=False)
graph_renderer = from_networkx(G, nx.nx_pydot.graphviz_layout(G, prog="dot"), scale=1, center=(0,0))

graph_renderer.node_renderer.glyph = Circle(size=5, fill_color=Spectral4[0])
graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

graph_renderer.selection_policy = NodesAndLinkedEdges()
graph_renderer.inspection_policy = NodesAndLinkedEdges()

plot.renderers.append(graph_renderer)

output_file("interactive_graphs.html")
show(plot)
#%% ---------------------------------------------------------------------------
# Cleanup
conn.logout()