from data.processed.extract_static_csv import main
import logging as log

inventory_df, sales_df = main()

log.info('Initializing CSV cleanup')

print(sales_df['sale_id'].duplicated())
print('**********************************')

# Check for duplicates in inventory_df
if "inventory_id" in inventory_df.columns:

    if inventory_df['inventory_id'].duplicated().sum() != 0:

        log.info("Checking for ID duplicity: Inventory DF")
        log.warning(f"Duplicate IDs found: {inventory_df['inventory_id'].duplicated().sum()}")
        
        duplicates = inventory_df[inventory_df['inventory_id'].duplicated(keep=False)]
        log.warning(duplicates)

        # Inspect duplicate counts
        duplicate_counts = duplicates['inventory_id'].value_counts()
        log.warning(f"Duplicate counts for Inventory IDs:\n{duplicate_counts}")

        # Drop duplicates (optional)
        inventory_df = inventory_df.drop_duplicates(subset='inventory_id', keep='first')
        log.info("Duplicates removed from Inventory DF.")
    else:
        log.info("No duplicate IDs found in Inventory DF.")
else:
    log.error("Critical error: Column 'inventory_id' not found in inventory_df")
    raise LookupError("Column 'inventory_id' not found in inventory_df")

if "sale_id" in sales_df.columns:

    if sales_df['sale_id'].duplicated().sum() != 0:
        print("Total rows:", len(sales_df))
        print("Unique sale_ids:", sales_df['sale_id'].nunique())
        print('**************************')
        print(f'value is not zero: {sales_df['sale_id'].duplicated().sum()}')
        print('**************************')
        log.info("Checking for ID duplicity: Sale DF")
        log.warning(f"Duplicate IDs found: {sales_df['sale_id'].duplicated().sum()}")
        
        duplicates = sales_df[sales_df['sale_id'].duplicated(keep=False)]
        log.warning(duplicates)

        # Inspect duplicate counts
        duplicate_counts = duplicates['sale_id'].value_counts()
        log.warning(f"Duplicate counts for Sale IDs:\n{duplicate_counts}")

        # Drop duplicates (optional)
        sales_df = sales_df.drop_duplicates(subset='sale_id', keep='first')
        log.info("Duplicates removed from Sales DF.")
    else:
        print('Value is zero')
        log.info("No duplicate IDs found in Sales DF.")
else:
    log.error("Critical error: Column 'sale_id' not found in sales_df")
    raise LookupError("Column 'sale_id' not found in sales_df")
