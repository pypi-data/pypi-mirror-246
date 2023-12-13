import mateo_pip.example as pp
import os

os.environ["DATABASE_URL"] = 1

BINS_WHERE_PRODUCT_IS_QUERY = """
SELECT
    wb.id,
    wb.warehouse_bin_type_id,
    wa.id warehouse_area_id,
    wb.name,
    wb.code,
    wb.parent_warehouse_bin_id,
    wb.composite,
    wb.ephemeral,
    COUNT(it.id) AS product_items_quantity
FROM warehouse_area AS wa
    INNER JOIN warehouse_bin AS wb
                ON wa.id = wb.warehouse_area_id
    INNER JOIN item AS it
                ON wb.id = it.current_location_warehouse_bin_id
WHERE it.item_state_id IN (3, 4)
    AND wa.warehouse_id = 2
    AND it.warehouse_id = 2
    AND it.product_id = 70632
    AND wb.warehouse_bin_type_id = 102
GROUP BY
    wb.id
ORDER BY
    product_items_quantity DESC;
"""

