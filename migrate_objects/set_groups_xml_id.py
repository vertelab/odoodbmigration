
from configuration import *


# ~ fields = {'name': 'Hudterapeut'}


unique = ['name']
id_name = {284: 'Hudterapeut', 
286: 'Slutkonsument', 
283: 'Återförsäljare', 
285: 'SPA-Terapeut', 
242: 'Portal',
243: 'Public',
}
target_model = "res.groups"
for group_id in id_name.keys():
    fields = {'name': id_name[group_id]}
    map_record_to_xml_id(target_model, fields, unique, group_id)
