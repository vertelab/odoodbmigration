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
The code to migrate the objects are in the migrate_objects/ directory.

* Generate/copy .odoorpcrc in your home directory with source and target configuration.


### Step 3: Run the scripts in the right order
`set_external_id.py` needs to be run first, but the order of the other scripts are irrelevant.
Is this step still relevant?
