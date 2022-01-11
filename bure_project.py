from configuration import *

IMPORT = '__import_bure__'
MA_IMPORT = '__import__'

k = 'allowed_internal_user_ids'
ids = sorted(source.env['project.project'].read(42, [k])[0][k])
model = source.env['project.project'].fields_get(k)[k]['relation']

map_ids_from_module_1to2(model=model, ids=ids,
                         module=MA_IMPORT, module2=IMPORT)

k = 'sprint_ids'
ids = sorted(source.env['project.project'].read(42, [k])[0][k])
model = source.env['project.project'].fields_get(k)[k]['relation']


'project.project'
# create_xmlid('project.project', 44, 42)
bure_project_context = {'mail_create_nolog': True,
                        'mail_create_nosubscribe': True,
                        'mail_notrack': True,
                        'tracking_disable': True}
bure_project_domain = [('id', '=', 42)]
bure_project_include = ['access_token',
                        'allowed_internal_user_ids', 'color',
                        'description', 'planned_hours', 'privacy_visibility', 'rating_active', 'task_no_next', 'use_scrum']
migrate_model('project.project',
              context=bure_project_context,
              create=0,
              domain=bure_project_domain,
              include=bure_project_include,
              )

'project.scrum.sprint'
bure_sprint_calc = {}
bure_sprint_command = {}
bure_sprint_context = {'active_test': False,
                       'mail_create_nolog': True,
                       'mail_create_nosubscribe': True,
                       'mail_notrack': True,
                       'tracking_disable': True}
bure_sprint_domain = [('project_id', '=', 42)]
bure_sprint_exclude = ['message_follower_ids']
bure_sprint_include = []
migrate_model('project.scrum.sprint',
              #   bypass_date=1,
              calc=bure_sprint_calc,
              command=bure_sprint_command,
              context=bure_sprint_context,
              #   create=0,
              domain=bure_sprint_domain,
              exclude=bure_sprint_exclude,
              #   ids=[1226],
              include=bure_sprint_include,
              module='__import_bure__',
              )


'project.task'
bure_task_calc = {}
bure_task_command = {'sprint_ids': 6}
bure_task_context = {'mail_create_nolog': True,
                     'mail_create_nosubscribe': True,
                     'mail_notrack': True,
                     'tracking_disable': True}
bure_task_domain = [('project_id', '=', 42)]
bure_task_exclude = ['message_follower_ids', 'us_ids']
bure_task_include = ['sprint_ids']
migrate_model('project.task',
              bypass_date=1,
              calc=bure_task_calc,
              command=bure_task_command,
              context=bure_task_context,
              #   create=0,
              domain=bure_task_domain,
              exclude=bure_task_exclude,
              ids=[1226],
              include=bure_task_include,
              module='__import_bure__',
              )

'mail.message'
create = 1
migrated_message_ids = target.env['ir.model.data'].find_all_ids_in_target(
    'mail.message','__import_bure__')
bure_mail_context = {'active_test': False,
                'mail_create_nosubscribe': True,
                'mail_create_nolog': True,
                'mail_notrack': True,
                'tracking_disable': True}
bure_mail_domain = [('project_id', '=', 42)]
bure_mail_records = {x.get('id'): x for x in source.env['project.task'].search_read(
    bure_mail_domain, ['message_ids'], order='id')}
for task_id in bure_mail_records:
    task_record = bure_mail_records.get(task_id)
    message_ids = sorted(task_record.get('message_ids'))
    to_migrate = []
    for message_id in message_ids:
        if create:
            if message_id in migrated_message_ids:
                print(message_id, 'is migrated, skipping creation')
                continue
            to_migrate.append(message_id)
        else:
            if message_id not in migrated_message_ids:
                print(message_id, 'is not migrated yet, write failed')
                continue
            to_migrate.append(message_id)

    if to_migrate:
        print(to_migrate)
        target_id = get_target_id_from_source_id('project.task', task_id)
        migrate_model('mail.message',
                        context=bure_mail_context,
                        create=1,
                        custom={'res_id': target_id},
                        exclude=['notified_partner_ids', 'tracking_value_ids'],
                        ids=to_migrate)
    else:
        continue
    print(f"Recordset('project.task', [{task_id}]).message_ids DONE!")
    
    








model = 'project.task'
source_model = source.env[model]
target_model = target.env[model]
source_fields = source_model.fields_get()
target_fields = target_model.fields_get()
exclude = ['message_follower_ids', 'sprint_type', 'us_ids']
fields = sorted(get_common_fields(
    source_fields, target_fields, exclude=exclude))
domain = [('project_id', '=', 42)]
source_ids = source_model.search(domain, order='id')
module = '__import_bure__'
source_ids = find_all_ids_in_target_model(model, source_ids, module)
source_model.read(1226, list(fields))

sprint_ids = sorted(set(
    sprints[i] for sprints in [
        task['sprint_ids'] for task in
        source.env['project.task'].search_read([('project_id', '=', 42)], ['sprint_ids'])]
    for i in range(len(sprints))))
