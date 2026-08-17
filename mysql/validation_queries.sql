

USE RETAIL_SOURCE_DB;


SELECT 'customers' AS table_name, COUNT(*) AS record_count
FROM customers

UNION ALL

SELECT 'products', COUNT(*)
FROM products

UNION ALL

SELECT 'sellers', COUNT(*)
FROM sellers

UNION ALL

SELECT 'warehouses', COUNT(*)
FROM warehouses

UNION ALL

SELECT 'orders', COUNT(*)
FROM orders

UNION ALL

SELECT 'order_items', COUNT(*)
FROM order_items

UNION ALL

SELECT 'payments', COUNT(*)
FROM payments

UNION ALL

SELECT 'shipments', COUNT(*)
FROM shipments

UNION ALL

SELECT 'returns', COUNT(*)
FROM returns

UNION ALL

SELECT 'reviews', COUNT(*)
FROM reviews;


SELECT Customer_ID, COUNT(*) AS duplicate_count
FROM customers
GROUP BY Customer_ID
HAVING COUNT(*) > 1;

SELECT Product_ID, COUNT(*) AS duplicate_count
FROM products
GROUP BY Product_ID
HAVING COUNT(*) > 1;

SELECT Seller_ID, COUNT(*) AS duplicate_count
FROM sellers
GROUP BY Seller_ID
HAVING COUNT(*) > 1;

SELECT Warehouse_ID, COUNT(*) AS duplicate_count
FROM warehouses
GROUP BY Warehouse_ID
HAVING COUNT(*) > 1;

SELECT Order_ID, COUNT(*) AS duplicate_count
FROM orders
GROUP BY Order_ID
HAVING COUNT(*) > 1;

SELECT Order_Item_ID, COUNT(*) AS duplicate_count
FROM order_items
GROUP BY Order_Item_ID
HAVING COUNT(*) > 1;

SELECT Payment_ID, COUNT(*) AS duplicate_count
FROM payments
GROUP BY Payment_ID
HAVING COUNT(*) > 1;

SELECT Shipment_ID, COUNT(*) AS duplicate_count
FROM shipments
GROUP BY Shipment_ID
HAVING COUNT(*) > 1;

SELECT Return_ID, COUNT(*) AS duplicate_count
FROM returns
GROUP BY Return_ID
HAVING COUNT(*) > 1;

SELECT Review_ID, COUNT(*) AS duplicate_count
FROM reviews
GROUP BY Review_ID
HAVING COUNT(*) > 1;



SELECT COUNT(*) AS null_customer_ids
FROM customers
WHERE Customer_ID IS NULL;

SELECT COUNT(*) AS null_product_ids
FROM products
WHERE Product_ID IS NULL;

SELECT COUNT(*) AS null_seller_ids
FROM sellers
WHERE Seller_ID IS NULL;

SELECT COUNT(*) AS null_warehouse_ids
FROM warehouses
WHERE Warehouse_ID IS NULL;

SELECT COUNT(*) AS null_order_ids
FROM orders
WHERE Order_ID IS NULL;

SELECT COUNT(*) AS null_order_item_ids
FROM order_items
WHERE Order_Item_ID IS NULL;

SELECT COUNT(*) AS null_payment_ids
FROM payments
WHERE Payment_ID IS NULL;

SELECT COUNT(*) AS null_shipment_ids
FROM shipments
WHERE Shipment_ID IS NULL;

SELECT COUNT(*) AS null_return_ids
FROM returns
WHERE Return_ID IS NULL;

SELECT COUNT(*) AS null_review_ids
FROM reviews
WHERE Review_ID IS NULL;



-- Orders with invalid customers
SELECT COUNT(*) AS invalid_order_customers
FROM orders o
LEFT JOIN customers c
    ON o.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL;


-- Order items with invalid orders
SELECT COUNT(*) AS invalid_order_item_orders
FROM order_items oi
LEFT JOIN orders o
    ON oi.Order_ID = o.Order_ID
WHERE o.Order_ID IS NULL;


-- Order items with invalid products
SELECT COUNT(*) AS invalid_order_item_products
FROM order_items oi
LEFT JOIN products p
    ON oi.Product_ID = p.Product_ID
WHERE p.Product_ID IS NULL;


-- Products with invalid sellers
SELECT COUNT(*) AS invalid_product_sellers
FROM products p
LEFT JOIN sellers s
    ON p.Seller_ID = s.Seller_ID
WHERE s.Seller_ID IS NULL;


-- Payments with invalid orders
SELECT COUNT(*) AS invalid_payment_orders
FROM payments p
LEFT JOIN orders o
    ON p.Order_ID = o.Order_ID
WHERE o.Order_ID IS NULL;


-- Shipments with invalid orders
SELECT COUNT(*) AS invalid_shipment_orders
FROM shipments s
LEFT JOIN orders o
    ON s.Order_ID = o.Order_ID
WHERE o.Order_ID IS NULL;


-- Shipments with invalid warehouses
SELECT COUNT(*) AS invalid_shipment_warehouses
FROM shipments s
LEFT JOIN warehouses w
    ON s.Warehouse_ID = w.Warehouse_ID
WHERE w.Warehouse_ID IS NULL;


-- Returns with invalid orders
SELECT COUNT(*) AS invalid_return_orders
FROM returns r
LEFT JOIN orders o
    ON r.Order_ID = o.Order_ID
WHERE o.Order_ID IS NULL;


-- Reviews with invalid customers
SELECT COUNT(*) AS invalid_review_customers
FROM reviews r
LEFT JOIN customers c
    ON r.Customer_ID = c.Customer_ID
WHERE c.Customer_ID IS NULL;



SELECT COUNT(*) AS invalid_review_products
FROM reviews r
LEFT JOIN products p
    ON r.Product_ID = p.Product_ID
WHERE p.Product_ID IS NULL;

=

-- Invalid product prices
SELECT COUNT(*) AS invalid_product_prices
FROM products
WHERE Price < 0
   OR Cost_Price < 0;


-- Invalid stock
SELECT COUNT(*) AS invalid_product_stock
FROM products
WHERE Stock < 0;


-- Invalid order item quantity
SELECT COUNT(*) AS invalid_quantities
FROM order_items
WHERE Quantity <= 0;


-- Invalid order item amounts
SELECT COUNT(*) AS invalid_order_item_amounts
FROM order_items
WHERE Unit_Price < 0
   OR Discount < 0
   OR Tax < 0
   OR Total_Amount < 0;


-- Invalid order totals
SELECT COUNT(*) AS invalid_order_totals
FROM orders
WHERE Order_Total < 0;


-- Invalid payment amounts
SELECT COUNT(*) AS invalid_payment_amounts
FROM payments
WHERE Payment_Amount < 0;


-- Invalid refund amounts
SELECT COUNT(*) AS invalid_refund_amounts
FROM returns
WHERE Refund_Amount < 0;


-- Invalid review ratings
SELECT COUNT(*) AS invalid_ratings
FROM reviews
WHERE Rating < 1
   OR Rating > 5;


-- Return date earlier than delivery date
SELECT COUNT(*) AS invalid_return_dates
FROM returns
WHERE Return_Date < Delivery_Date;


-- Delivery date earlier than shipment date
SELECT COUNT(*) AS invalid_delivery_dates
FROM shipments
WHERE Delivery_Date < Shipment_Date;


