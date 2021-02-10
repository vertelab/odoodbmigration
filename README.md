## Guide: How to migrate all objects of the following models from source to a target
  * product.attribute
  * product.attribute.value
  * product.attribute.line
  * product.template
  * product.template.attribute.value
  * product.template.attribute.line
  * product.product 
  * product.public.category
  * product.pricelist
  * product.pricelist.item

### Step 1: Configuration
The code to migrate the objects are in the migrate_objects/ directory. \

In `configuration.py` you need to change the IP, database name, and credentials of the source and target. \

### Step 2: Run the scripts in the following order
1. `set_external_id.py`
2. `set_product_category.py`
3. `set_product_pricelist_item.py`
4. `set_category_parent.py`
