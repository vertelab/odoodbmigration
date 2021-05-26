import odoorpc
import datetime

source = odoorpc.ODOO.load('source_kastrup')
target = odoorpc.ODOO.load('target_kastrup')

del source.env.context['lang']
target.env.context['lang'] = 'en_US'

# HELPER FUNCTIONS
IMPORT_MODULE_STRING = '__import__'
''' Glossary
       domain = list of search criterias
           id = number
        model = ex. 'res.partner'
record_fields = what you get from source.env[model].read(record.id, fields)
  record_list = what you get from source.env[model].search([])
      records = what you get from source.env[model].browse(record_list)
       record = what you get from source.env[model].browse(record_list[index])
       source = source database
       target = target database
'''


def unlink(model, only_migrated=True):
    ''' unlinks all records of a model in target database
    example: unlink('res.partner')
    '''
    record_list = []
    if only_migrated:
        domain = [('module', '=', IMPORT_MODULE_STRING), ('model', '=', model)]
        model_data_record_list = target.env['ir.model.data'].search(domain)
        model_data_records = target.env['ir.model.data'].browse(
            model_data_record_list)
        for record in model_data_records:
            record_list.append(record.res_id)
    else:
        record_list = target.env[model].search([])

    try:
        target.env[model].browse(record_list).unlink()
        print(f"Recordset('{model}', {record_list}) unlinked")
    except Exception as e:
        print(e)


def create_xml_id(model, target_record_id, source_record_id):
    ''' Creates an external id for a model
    example: create_xml_id('product.template', 89122, 5021)
    '''
    xml_id = f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}"
    values = {
        'module': xml_id.split('.')[0],
        'name': xml_id.split('.')[1],
        'model': model,
        'res_id': target_record_id,
    }
    try:
        target.env['ir.model.data'].create(values)
        return f"xml_id = {xml_id} created"
    except:
        return f"ERROR: create_xml_id('{model}', {target_record_id}, {source_record_id}) failed. Does the id already exist?"


def get_target_record_from_id(model, source_record_id):
    ''' gets record from target database using record.id from source database
    example: get_target_record_from_id('product.attribute', 3422)
    returns: 0 if record cannot be found
    '''
    try:
        return target.env.ref(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
    except:
        return 0


def create_record_and_xml_id(model, fields, source_record_id):
    ''' Creates record on target if it doesn't exist, using fields as values,
    and creates an external id so that the record will not be duplicated
    example: create_record_and_xml_id('res.partner', {'name':'MyPartner'}, 2)
    '''
    if get_target_record_from_id(model, source_record_id):
        print(
            f"INFO: skipping creation, an external id already exist for [{model}] [{source_record_id}]")
    else:
        try:
            target_record_id = target.env[model].create(fields)
            print(f"Recordset('{model}', [{target_record_id}]) created")
        except Exception as e:
            print(
                f"ERROR: target.env['{model}'].create ({source_record_id}) failed")
            return e
        print(create_xml_id(model, target_record_id, source_record_id))


def migrate_model(model, exclude=[], diff={}, custom={}, debug=False, create=True):
    '''
    use this method for migrating a model with return dict from get_all_fields()
    example:
        product_template = get_all_fields(
            'product.template', exclude=['message_follower_ids'])
        simple_migrate_model('product.template', product_template)
    '''
    s = source.env[model]
    fields = get_all_fields(model, exclude, diff)
    errors = {'ERRORS:'}

    for source_record_id in s.search([]):
        target_record = get_target_record_from_id(model, source_record_id)
        if create and target_record:
            print(
                f"INFO: skipping creation, an external id already exist for [{model}] [{source_record_id}]")
            continue
        vals = {}
        source_record = s.browse(source_record_id)
        source_record_values = s.read(source_record_id, fields)
        if type(source_record_values) is list:
            source_record_values = source_record_values[0]

        # Customize certain fields before creating records
        for key in fields:

            # Remove /page if it exists in url (odoo v8 -> odoo 14)
            if key == 'url' and type(source_record_values[key]) is str:
                url = source_record[key]
                if url.startswith('/page'):
                    url = url.replace('/page', '')
                vals.update({fields[key]: url})

            # Stringify datetime objects
            # TypeError('Object of type datetime is not JSON serializable')
            elif type(source_record[key]) is datetime.datetime:
                vals.update({fields[key]: str(source_record[key])})

            # If the value of the key is a list, look for the corresponding record on target instead of copying the value directly
            # example: country_id 198, on source is 'Sweden' while
            #          country_id 198, on target is 'Saint Helena, Ascension and Tristan da Cunha'
            elif type(source_record_values[key]) is list:
                try:
                    vals.update(
                        {fields[key]: get_id_from_xml_id(source_record[key])})
                    continue
                except:
                    x = get_target_record_from_id(
                        source_record[key]._name, source_record[key].id)
                    if x:
                        vals.update({fields[key]: x.id})
                        continue
                    error = f"Target '{key}': {source_record[key]} does not exist"
                    if error not in errors:
                        errors.add(error)
                        if debug:
                            print(error)

            # Just copy the value it it is not False
            elif source_record[key]:
                vals.update({fields[key]: source_record[key]})

        vals.update(custom)
        # Break operation and return last dict used for creating record if something is wrong and debug is True
        if create and create_record_and_xml_id(model, vals, source_record.id) and debug:
            return vals
        elif not create:
            try:
                target_record.write(vals)
                print(f"Writing to existing {source_record}")
            except:
                return vals

    return errors


def get_id_from_xml_id(record):
    '''
    Returns a dict with { key: id } of target record
    example:
    source_record = source.env['res.company'].browse(1)
    get_target_id_from_source(source_record, 'country_id')
    '''
    s = source.env['ir.model.data']
    d = [('model', '=', record._name),
         ('res_id', '=', record.id)]
    return target.env.ref(s.browse(s.search(d)).complete_name).id


def get_all_fields(model, exclude=[], diff={}):
    '''
    Returns dict with key as source model keys and value as target model keys
    Use exclude = ['this_field', 'that_field'] to exclude keys on source model
    Use diff = {'image':'image_1920'} to update key-value pairs manually
    '''
    fields = {}
    target_field_keys = target.env[model]._columns

    # for key, value in target.env[model].fields_get().items():
    #     if not value['readonly']:
    #         target_field_keys.append(key)

    for key in source.env[model]._columns:
        if key in exclude:
            continue
        elif key in target_field_keys:
            fields.update({key: key})

    fields.update(diff)

    return fields


def get_fields_difference(model):
    '''
    Returns list with fields difference
    example: get_fields_difference('res.company')
    '''
    source_set = set(source.env[model]._columns)
    target_set = set(target.env[model]._columns)

    return {'source': source_set - target_set, 'target': target_set - source_set}


def get_required_fields(model):
    '''
    Returns list with required fields
    example: get_required_fields('res.company')
    '''
    source_dict = source.env[model].fields_get()
    target_dict = target.env[model].fields_get()
    source_keys = []
    target_keys = []
    for key in source_dict:
        if source_dict[key]['required']:
            source_keys.append(key)
    for key in target_dict:
        if target_dict[key]['required']:
            target_keys.append(key)
    return {'source': source_keys, 'target': target_keys}
