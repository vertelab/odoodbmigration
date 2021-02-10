## Guide: How to migrate all obejcts of the following models from source to a target
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
In each script file you need to change the IP, database name, and credentials of the source and target. \

TODO: create centralized configuration file

### Step 2: Run the scripts in the following order
1. `set_external_id.py`
2. `set_product_category.py`
3. `set_product_pricelist_item.py`
4. `set_product_attribute_line.py`
5. `set_category_parent.py`
