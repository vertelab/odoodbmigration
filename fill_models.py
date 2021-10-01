from configuration import *

models = {
    'project.task.type': {},        # 36,   14-1
    'project.category': {           # 259   1   , 3 duplicates in source
        'model': 'project.tags'},
    'project.project': {},          # 46,   5-2
    'project.task': {},             # 4080, 56-4
    'account.analytic.account': {   # 45
        'domain': [('id', '=', sorted(set([x.get('analytic_account_id')[0] for x in source.env['project.project'].search_read([], ['analytic_account_id'])])))]},  # 59,
    'project.task.work': {          # 6232
        'model': 'account.analytic.line',
        'domain': [('hr_analytic_timesheet_id', '!=', False)]},
    'mail.message': {               # 35627, 9 messages have res_id as 0
        'domain': [('model', '=', 'project.task'), ('res_id', '!=', False)]},
    'project.sprint.type': {},      # 3
    'project.scrum.actors': {},     # 0
    'project.scrum.portfolio': {},  # 18,   6-1
    'project.scrum.sprint': {},     # 138,  3-1
    'project.scrum.us': {},         # 1,    2-1
    'project.scrum.timebox': {},    # 87,   1-1
    'project.scrum.test': {},       # 0
}

for s_model in models:
    try:
        domain = models.get(s_model).get('domain', [])
        s_count = len(source.env[s_model].search(domain))
        print('source model', s_model, s_count)
        t_model = models.get(s_model).get('model', s_model)
        t_count = len(target.env[t_model].search([]))
        print('target model', t_model, t_count)
        m_count = len(target.env['ir.model.data'].find_all_ids_in_target(t_model))
        m_count += len(target.env['ir.model.data'].find_all_ids_in_target(t_model,'__import_bure__'))
        print('migrated', m_count)
        if m_count < s_count:
            print(colored(f"missing {t_model} {s_count-m_count}", 'red'))
        else:
            print(colored('complete', 'green'))
    except:
        input(f'{s_model} or {t_model} is missing probably...Press Enter to continue')


migrate_model('project.task.type')

for _id in sorted(source.env['project.category'].search([])):
    migrate_model('project.category', ids=[_id], model2='project.tags')

# source.env['project.category'].search([('name', '=', 'packning')])      # [76, 77]
# source.env['project.category'].search([('name', '=', 'El')])            # [96, 100]
# source.env['project.category'].search([('name', '=', 'Release 1')])     # [259, 260]
# source.env['project.category'].search([('name', '=', 'Dokumentation')]) # [25, 266]
create_xmlid('project.tags',
             get_target_id_from_source_id('project.tags', 76), 77)
create_xmlid('project.tags',
             get_target_id_from_source_id('project.tags', 96), 100)
create_xmlid('project.tags',
             get_target_id_from_source_id('project.tags', 259), 260)
create_xmlid('project.tags',
             get_target_id_from_source_id('project.tags', 25), 266)


'project.project'
project_calc = {'privacy_visibility': """
vals.update(
    {fields[key]: 'portal' if record[key] in ['public'] else record[key]})"""}
project_domain = [('id', '!=', 55)]
migrate_model('project.project', calc=project_calc, domain=project_domain)
# bure_project_domain = [('id', '=', 42)]
# create_xmlid('project.project', 44, 42)
# migrate_model('project.project', calc=project_calc, domain=bure_project_domain)


'account.analytic.account mapping'
for pid in source.env['project.project'].search([], order='id'):
    source_id = source.env['project.project'].read(
        pid, ['analytic_account_id'])['analytic_account_id'][0]
    pid_target = get_target_id_from_source_id('project.project', pid)
    target_id = target.env['project.project'].read(
        pid_target, ['analytic_account_id'])[0]['analytic_account_id'][0]
    create_xmlid('account.analytic.account', target_id, source_id)


'project.task'
# project_ids = [30, 55] # priority projects
task_calc = {'priority': """if key in fields:
        vals.update({fields[key]: '0' if record[key] in ['0','1'] else '1'})""",
             'categ_ids': """vals.update({'tag_ids':[get_target_id_from_source_id('project.tags',_id) for _id in record[key]]})"""
             }
task_context = {'mail_create_nosubscribe': True,
                'mail_create_nolog': True,
                'mail_notrack': True,
                'tracking_disable': True}
task_diff = {'categ_ids': 'tag_ids',
             'date_start': 'date_assign'}
task_domain = [('project_id', '!=', 55)]
migrate_model('project.task',
              calc=task_calc,
              context=task_context,
              create=1,
              diff=task_diff,
              domain=task_domain,
              exclude=['message_follower_ids'],
              )


migrate_model('project.scrum.actors')   # empty
migrate_model('project.scrum.meeting')  # empty
migrate_model('project.scrum.test')     # empty
migrate_model('project.scrum.us')       # 1 record
migrate_model('project.scrum.portfolio')
migrate_model('project.scrum.sprint')
migrate_model('project.scrum.timebox')


'project.task.work -> account.analytic.line'
create = 1
line_ids = target.env['ir.model.data'].find_all_ids_in_target(
    'account.analytic.line')
task_records = {x.get('id'): x for x in source.env['project.task'].search_read(
    [], ['project_id'])}
timesheet_records = {x.get('id'): x for x in source.env['hr.analytic.timesheet'].search_read(
    [], ['line_id'], order='id')}
user_records = {x.get('id'): x for x in source.env['res.users'].search_read(
    [], ['employee'], order='id')}
work_records = {x.get('id'): x for x in source.env['project.task.work'].search_read(
    [('hr_analytic_timesheet_id', '!=', False)], ['hr_analytic_timesheet_id', 'task_id', 'user_id'], order='id')}
for work_id in work_records:
    work_record = work_records.get(work_id)
    timesheet = work_record.get('hr_analytic_timesheet_id')
    line = timesheet_records.get(timesheet[0]).get('line_id')
    if line:
        line = line[0]

    if line in line_ids and create:
        continue

    vals = {}

    task = work_record.get('task_id')
    if task:
        task = task[0]
        vals.update(
            {'task_id': get_target_id_from_source_id('project.task', task)})

        task_record = task_records.get(task)

        employee = False
        user = work_record.get('user_id')
        if user:
            user_record = user_records.get(user[0])

            employee = user_record.get('employee')
            if employee:
                employee = get_target_id_from_source_id(
                    'hr.employee', employee[0])

        vals.update(
            {'employee_id': employee})

        project = task_record.get('project_id')
        if project:
            vals.update(
                {'project_id': get_target_id_from_source_id('project.project', project[0])})

    print(vals)
    migrate_model('account.analytic.line',
                  context=task_context,
                  create=create,
                  custom=vals,
                  ids=[line])
    line_ids.append(line)


create = 1
migrated_message_ids = target.env['ir.model.data'].find_all_ids_in_target(
    'mail.message')
task_context = {'mail_create_nosubscribe': True,
                'mail_create_nolog': True,
                'mail_notrack': True,
                'tracking_disable': True}
task_domain = [('project_id', '!=', 55)]
task_records = {x.get('id'): x for x in source.env['project.task'].search_read(
    task_domain, ['message_ids'], order='id')}
for task_id in task_records:
    task_record = task_records.get(task_id)
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
                      context=task_context,
                      create=create,
                      custom={'res_id': target_id},
                      exclude=['notified_partner_ids', 'tracking_value_ids'],
                      ids=to_migrate)
    else:
        continue
    print(f"Recordset('project.task', [{task_id}]).message_ids DONE!")
