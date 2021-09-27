#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = True

if debug:
    input("press enter to continue")

# ~ # product.product fields to copy from source to target WORKS
pp_domain = [('access_group_ids', '=', 286), ('sale_ok', '=', True), ('website_published', '=', True)]
#pp_domain = [('id', 'in', [11062,11092,11093,11219,11221,11222,11291,11293,11495,11496,11497,11498,11499,11500,11572,11612,11623,11624,11625,11640,11641,11642,11643,11644,11645,11719,11720,11721,11828,11829,11844,11845,11846,11847,11848,11849,2489,2603,2729,2854,2870,3049,3050,3051,4242,4493,4494,4693,5071,5386,5652,5933,5935,5938,7392,7638,8340,8355,8466,8467,8625,9564,9568,9572,9626,9627,9628,9632,9633,9634,9635,9636,9637,9638,9639,9640,9641,9642,9643,9644,9645,9646,9651,9652,9653,9654,9655,9656,9662,9663,9664,9665,9666,9667,9668,9669,9670,9674,9675,9676,9683,9684,9685,9686,9687,9688,9689,9690,9691,9692,9693,9694,9695,9696,9697,9698,9699,9700,9701,9702,9703,9704,9705,9706,9707,9708,9709,9710,9711,9712,9713,9714,9715,9716,9717,9718,9719,9720,9721])]
#product_product_include = ['image', 'lst_price', 'list_price']
product_product_include = ['default_code']
#product_product_custom = {
#    'image': 'image_1920'
#}


migrate_model('product.product', include=True, migrate_fields=product_product_include, create=False, domain=pp_domain)
#migrate_model('product.product', include=True, migrate_fields=product_product_include, custom=product_product_custom, domain=pp_domain, create=False)
if debug:
    input("press enter to continue")




