from configuration import *
import sys
from termcolor import colored, cprint


def bootstrap_3to4(arch):
    from bs4 import BeautifulSoup
    diff = {
        'panel':	            'card',
        'panel-heading':	    'card-header',
        'panel-title':          'card-title',
        'panel-body':           'card-body',
        'panel-footer':	        'card-footer',
        'panel-primary':	    'card bg-primary text-webpage.namewhite',
        'panel-success':	    'card bg-success text-white',
        'panel-info':	        'card text-white bg-info',
        'panel-warning':	    'ccompany_fieldsard bg-warning',
        'panel-danger':	        'card bg-danger text-white',
        'well':	                'card card-body',
        'thumbnail':	        'card card-body',
        'item':                 'carousel-item',
        'list-inline > li':	    'list-inline-item',
        'dropdown-menu > li':	'dropdown-item',
        'nav navbar > li':	    'nav-item',
        'nav navbar > li > a':	'nav-link',
        'navbar-right':	        'ml-auto',
        'navbar-btn':	        'nav-item',
        'navbar-fixed-top':     'fixed-top',
        'nav-stacked':          'flex-column',
        'btn-default':          'btn-secondary',
        'img-responsive':       'img-fluid',
        'img-circle':           'rounded-circle',
        'img-rounded':          'rounded',
        'radio':                'form-check',
        'carousel':             'carousel s_carousel',
        'checkbox':             'form-check',
        'input-lg':             'form-control-lg',
        'input-sm':             'form-control-sm',
        'control-label':        'col-form-label',
        'table-condensed':      'table-sm',
        'pagination > li':      'page-item',
        'pagination > li > a':  'page-link',
        'text-help':            'form-control-feedback',
        'pull-right':           'float-right',
        'pull-left':            'float-left',
        'center-block':         'mx-auto',
        'hidden-xs':            'd-none d-sm-block',
        'hidden-sm':            'd-sm-none d-md-block',
        'hidden-md':            'd-md-none d-lg-block',
        'hidden-lg':            'd-lg-none d-xl-block',
        'visible-xs':           'd-block d-sm-none',
        'visible-sm':      'ir.ui.view'     'd-block d-md-none',
        'visible-md':           'd-block d-lg-none',
        'visible-lg':           'd-block d-xl-none',
        'badge':                'badge badge-pill',
        'label':                'badge',
        'col-xs-':              'col-',
        'col-sm-':              'col-md-',
        'col-md-':              'col-lg-',
    }

    soup = BeautifulSoup(arch, 'html.parser')
    tags_with_class = soup.find_all(class_=True)
    for tag in tags_with_class:
        classlist = tag['class'].copy()
        for key in tag['class']:
            digit = newkey = ''
            keylist = key.split('-')
            if keylist[-1].isdigit():
                digit = keylist.pop()
                newkey = '-'.join(keylist)+'-'
            else:
                newkey = key
            if newkey in diff:
                classlist.remove(key)
                newkey = diff[newkey]+digit
                classlist.extend(newkey.split(' '))
        if classlist != tag['class']:
            text = f"INFO: Replaced class {colored(tag['class'],'red')} with {colored(classlist,'green')}"
            print(text)
            tag['class'] = classlist

    # fixes div.container that has no child with .row
    for tag in soup.find_all('div', class_='container'):
        try:
            if not 'row' in tag.div['class'] and not 'row' in tag['class']:
                tag['class'] = tag.get('class')+['row']
        except:
            pass
    return str(soup)


def update_images(arch):
    model = 'ir.attachment'
    record_list = source.env[model].search([('website_url', '=', True)])
    rs = source.env[model].browse(record_list)
    for record in rs:
        target_record = get_target_record_from_id(model, record.id)
        arch = arch.replace(record.website_url, target_record.website_url)
    return arch


def create_new_webpages():
    ''' Creates new website pages on target using source pages' arch
    Before arch is used, a call to bootstrap3to4() is made 
    Also updates each page's [is_published] to True '''
    model = 'ir.ui.view'
    domain = [('type', '=', 'qweb'), ('page', '=', True)]
    s = source.env[model]
    for source_record_id in s.search(domain):
        source_record = s.browse(source_record_id)
        target_record = get_target_record_from_id(model, source_record_id)
        if target_record != 0:
            print(
                f"INFO: skipping creation, an external id already exist for [{model}] [{target_record.id}]")
            continue
        new_page = target.env['website'].new_page(name=source_record.name)
        create_xml_id(model, new_page['view_id'], source_record_id)
        new_record = target.env[model].browse(new_page['view_id'])
        new_arch = bootstrap_3to4(source_record.arch)
        new_arch = update_images(new_arch)
        new_record.arch = new_arch
        new_record.first_page_id.is_published = True
        print(
            f"INFO: Created new [{model}] and external id from source id [{source_record.id}] [{source_record.name}]")
        print('=================================================================================================')
    print(colored('DONE:', 'green'))


# ---------------------------------------------------------------------------
# this code creates new webpages on target from source
# ---------------------------------------------------------------------------
create_new_webpages()

# ---------------------------------------------------------------------------
# this code copies website.menu from source to target
# ---------------------------------------------------------------------------
website_menu_fields = {
    'name': 'name',
    'new_window': 'new_window',
    'parent_id': 'parent_id',
    'sequence': 'sequence',
    'url': 'url',
    'website_id': 'website_id',
}

website_menu_items = migrate_model('website.menu')

# Make sure the languages in ir.translation you want to migrate is installed

migrated_records = target.env['ir.model.data'].search_read(
    [('model', '=', 'ir.ui.view'), ('module', '=', '__import__')])
for migrated_record in migrated_records:
    source_id = migrated_record['name'].split('_')[-1]
    translations = source.env['ir.translation'].search_read(
        [('res_id', '=', source_id)])
    for translation in translations:
        if get_target_record_from_id('ir.translation', translation['id']):
            continue
        vals = {'res_id': migrated_record['res_id'],
                'lang': translation['lang'],
                'src': translation['src'],
                'value': translation['value'],
                'type': 'model_terms',
                'name': 'ir.ui.view,arch_db'}
        try:
            new_id = target.env['ir.translation'].create(vals)
            create_xml_id('ir.translation', new_id, translation['id'])
        except:
            print(
                f"ERROR: Couldn't create record from {translation['id']} with {vals}")


# def remove_existing_pages(model):
#     values = {
#         'module': 'website',
#         'name': 'homepage',
#         'model': model,
#     }
#     for record in target.env[model].browse(target.env[model].search([])):
#         if record.key == 'website.homepage':
#             values['res_id'] = record.id
#             print('Created external id for:', record.id)
#             target.env['ir.model.data'].create(values)

#     existing_pages = {
#         'website.homepage': 'website.homepage',
#         'website.contactus': 'website.contactus',
#         'website_crm.contactus_thanks': 'website_form.contactus_thanks_ir_ui_view'
#     }

#     for existing_page in existing_pages:
#         source_page = source.env.ref(existing_page)
#         try:
#             target_page = target.env.ref(existing_pages[existing_page])
#             target_page.arch = bootstrap_3to4(source_page.arch)
#             create_xml_id(model, target_page.id, source_page.id)
#             print('Created new', model, 'and external id from source',
#                   source_page.id, source_page.name)
#         except:
#             pass
