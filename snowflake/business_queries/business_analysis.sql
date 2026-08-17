USE WAREHOUSE RETAILPULSE_WH;

USE DATABASE REATILPULSE_DW;

USE SCHEMA REATILPULSE_SCHEMA;

-- Find the total number of sales records.

select count(*) from fact_sales

-- Calculate the total sales amount.

select sum(total_amount) as total_sales from fact_sales

-- Find the average order value.

select avg(order_total) as avg_order
from fact_sales

-- Count the total number of unique customers.

select distinct(customer_id)
from fact_sales

-- Count the total number of unique products sold.

select distinct(product_id)
from fact_sales

-- Count the total number of products.  

select count(*)
from dim_product

-- List all product categories.

select distinct(category)
from dim_product

-- Find the most expensive product.

select distinct (product_id),brand,category,cost_price
from dim_product
order by cost_price desc
limit 1

-- Find the cheapest product.

select distinct (product_id),brand,category,cost_price
from dim_product
order by cost_price
limit 1

-- Count products in each category.

select count(product_id) as products,category 
from dim_product
group by category

-- Count customers in each state

select count(customer_id) as no_of_cust ,state 
from  dim_customer
group by state
order by no_of_cust desc

-- Count customers in each city

select count(customer_id) as no_of_cust ,city
from  dim_customer
group by city
order by no_of_cust desc

-- Find all active customers.

select *  
from dim_customer
where customer_status = 'Active'

-- Find all active customers.


select *  
from dim_customer
where customer_status = 'Inactive'

-- Count customers by country.

select count(*),country 
from dim_customer
group by country

-- Find the Top 10 selling products by revenue.  

select p.product_id, p.Brand, p.category,sum(s.TOTAL_AMOUNT) as total_revenue
from dim_product p
inner join fact_sales as s on s.product_id = p.product_id
group by p.product_id, p.Brand, p.category
order by total_revenue desc
limit 10

-- Find the Top 10 products by quantity sold.

select p.product_id, p.Brand, p.category,sum(s.quantity) as total_quantity
from dim_product as p
join fact_sales as s on s.PRODUCT_ID = p.PRODUCT_ID
group by p.product_id, p.Brand, p.category
order by total_quantity desc
limit 10

-- 18. Calculate total sales by category.

select p.category,sum(s.total_amount) as total_sales
from fact_sales as s
inner join dim_product as p on p.product_id = s.product_id
group by p.category
order by total_sales desc

-- Calculate average product price by category.

select avg(s.unit_price) as avg_product_price, p.CATEGORY
from fact_sales as s
inner join dim_product as p on p.PRODUCT_ID = s.PRODUCT_ID
group by  p.CATEGORY
order by avg_product_price desc

-- 20. Find the brand generating the highest revenue.

select sum(s.total_amount) as highest_revenue, p.brand
from fact_sales as s
join dim_product as p on p.PRODUCT_ID = s.PRODUCT_ID
group by p.brand
order by highest_revenue desc
limit 1


-- 21. Find the Top 10 customers by total spending.

select sum(total_amount) total_spending, c.customer_id, c.customer_name
from dim_customer c
join fact_sales s on c.CUSTOMER_ID = s.CUSTOMER_ID
group by c.customer_id, c.customer_name
order by total_spending desc
limit 10

-- 22. Find total sales by state.

select sum(s.total_amount) as total_sales,c.state
from dim_customer as c
join fact_sales as s on c.CUSTOMER_ID = s.CUSTOMER_ID
group by c.state
order by total_sales desc

-- 23. Find total sales by city.

select c.city, sum(s.total_amount) as total_sales
from dim_customer as c
join fact_sales as s on c.CUSTOMER_ID = s.CUSTOMER_ID
group by c.city
order by total_sales desc

-- 24. Count total orders per customer.

select c.CUSTOMER_ID,c.customer_name,count(s.order_id) as number_of_orders
from dim_customer c
join fact_sales s on c.customer_id = s.customer_id
group by c.CUSTOMER_ID,c.customer_name
order by number_of_orders desc

-- Find customers who placed more than 10 orders.

select c.customer_id, c.customer_name ,count(s.order_id) as number_of_orders
from dim_customer c
join fact_sales s on c.customer_id = s.customer_id
group by c.customer_id, c.customer_name
order by number_of_orders desc
limit 10

-- 26. Count payments by payment method.

select PAYMENT_method, count(payment_method) as no_of_payments
from fact_payments
group by  PAYMENT_METHOD

-- 27. Count successful and failed payments.

select payment_status, count(*)
from fact_payments
group by payment_status

-- 28. Calculate total payment amount by payment method.

select payment_method , sum(payment_amount)
from fact_payments
group by payment_method

-- 29. Find the highest payment.

select distinct(payment_amount)
from fact_payments
order by payment_amount desc
limit 1

-- 30. Find the average payment amount.

select avg(payment_amount)
from fact_payments


-- 31. Count shipments by courier.

select courier,count(courier)
from fact_shipments
group by courier

-- 32. Count shipments by shipment status.

select shipment_status ,count(shipment_status)
from fact_shipments
group by shipment_status

-- 33. Find warehouses handling the most shipments.

select w.warehouse_name,count(s.shipment_id) as most_shipments
from fact_shipments as s
join dim_warehouse as w on s.warehouse_id = w.warehouse_id
group by  w.warehouse_name
ORDER BY TOTAL_SHIPMENTS DESC;

-- 34. Count delivered shipments.

select shipment_status ,count(shipment_status)
from fact_shipments
where shipment_status = "Delivered"
group by shipment_status

-- 35. Count shipments still in transit.

select shipment_status ,count(shipment_status)
from fact_shipments
where shipment_status = "In Transit"
group by shipment_status

-- 36. Count returns by reason

select count(return_reason)
from fact_returns

-- 37. Count approved returns.

select count(return_reason)
from fact_returns
where return_reason = "Approved"

-- Calculate total refund amount.

select sum(return_reason)
from fact_returns
where return_reason = "Refund"

-- 39. Find the return reason with the highest count.

SELECT
    RETURN_REASON,
    COUNT(*) AS TOTAL_RETURNS
FROM FACT_RETURNS
GROUP BY RETURN_REASON
ORDER BY TOTAL_RETURNS DESC
LIMIT 1;


-- 40. Calculate return percentage.

select
    round
        (count(*) * 100/ (select count(distinct order_id) 
                          from fact_sales),2)  as return_percentage 
from fact_returns


-- 41. Calculate the average product rating.


select avg(rating) as average_rating
from fact_reviews

-- 42. Find products with the highest average rating.

select p.product_id, p.brand ,avg(r.rating) as avg_rating
from dim_product p
join fact_reviews as r on p.product_id = r.product_id
group by p.product_id, p.brand
order by avg_rating desc 

-- 43. Find products with the lowest average rating.

select p.product_id, p.brand ,avg(r.rating) as avg_rating
from dim_product p
join fact_reviews as r on p.product_id = r.product_id
group by p.product_id, p.brand
order by avg_rating

-- 44. Count reviews for each product.

select product_id , count(*) as total_reviews
from fact_reviews
group by product_id
order by total_reviews desc

-- 45. Find products with more than 30 reviews.

select product_id, count(*) total_reviews
from fact_reviews
group by product_id
having count(*) > 30
order by total_reviews desc

-- 46. Monthly sales trend

select 
    date_trunc("Month",order_date) as sales_month,
    sum(total_amount) as monthly_sales
from fact_sales
group by sales_month
order by sales_month desc

-- 47. Yearly sales trend

select
    date_trunc("Year", order_date) as sales_year,
    sum(total_amount) as yearly_sales
from fact_sales
group by sales_year
order by sales_year desc

-- 48. Top 5 categories by revenue

select p.category,sum(s.total_amount) as revenue
from dim_product p
join fact_sales s on p.product_id = s.product_id
group by p.category
order by revenue desc
limit 5

-- 49. Top 10 brands by sales

select p.brand, sum(total_amount) as sales
from dim_product p
join fact_sales f on p.product_id = f.PRODUCT_ID
group by p.BRAND
order by sales desc
limit 10

-- 50. Customer lifetime value

select
    c.customer_id,
    c.customer_name,
    sum(s.total_amount) as lifetime_value
from dim_customer c
join fact_sales s on c.customer_id = s.customer_id
group by c.customer_id,c.customer_name
order by lifetime_value desc

-- 51. Running total of monthly sales

select 
    sales_month,
    monthly_sales,
    sum(monthly_sales) over(order by sales_month) as running_total
from (
select
    date_trunc("Month",order_date) sales_month,
    sum(total_amount) as monthly_sales
from fact_sales
group by sales_month
)
order by sales_month desc


-- 52. Rank products by revenue

select 
    p.product_id,
    p.Brand,
    sum(total_amount) total_revenue,
    rank() over(order by sum(s.total_amount) desc ) as product_rank
from dim_product p
inner join fact_sales s on p.product_id = s.product_id
group by p.product_id,p.Brand
order by product_rank


-- 53. Dense rank customers by spending

select
    c.customer_id,
    c.customer_name,
    sum(s.total_amount) as total_spent,
    dense_rank() over (order by sum(s.total_amount) desc ) rank_spending
from fact_sales s 
join dim_customer as c on s.CUSTOMER_ID = c.CUSTOMER_ID
group by c.customer_id, c.customer_name
order by rank_spending

-- 54. Percentage contribution of each category to total sales

SELECT
    P.CATEGORY,
    SUM(F.TOTAL_AMOUNT) AS CATEGORY_SALES,
    ROUND(
        SUM(F.TOTAL_AMOUNT) * 100.0 /
        SUM(SUM(F.TOTAL_AMOUNT)) OVER (),
        2
    ) AS SALES_PERCENTAGE
FROM FACT_SALES F
JOIN DIM_PRODUCT P
    ON F.PRODUCT_ID = P.PRODUCT_ID
GROUP BY P.CATEGORY
ORDER BY CATEGORY_SALES DESC;

-- 55. Top-selling product in each category

WITH PRODUCT_SALES AS (
    SELECT
        P.CATEGORY,
        P.PRODUCT_ID,
        P.Brand,
        SUM(F.TOTAL_AMOUNT) AS TOTAL_SALES
    FROM FACT_SALES F
    JOIN DIM_PRODUCT P
        ON F.PRODUCT_ID = P.PRODUCT_ID
    GROUP BY
        P.CATEGORY,
        P.PRODUCT_ID,
        P.BRAND
),
RANKED_PRODUCTS AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY CATEGORY
            ORDER BY TOTAL_SALES DESC
        ) AS RN
    FROM PRODUCT_SALES
)
SELECT
    CATEGORY,
    PRODUCT_ID,
    Brand,
    TOTAL_SALES
FROM RANKED_PRODUCTS
WHERE RN = 1
ORDER BY CATEGORY;


-- 56. Use ROW_NUMBER() to rank products by sales

select 
    p.product_id,
    p.brand,
    sum(s.total_amount) as total_sales,
    row_number()over(order by sum(s.total_amount) desc ) rank_by_product
from fact_sales s
join dim_product p on p.PRODUCT_ID = s.PRODUCT_ID
group by p.product_id, p.brand
order by rank_by_product 

-- 57. Use RANK() to rank customers by total spending

select
    c.customer_id,
    c.customer_name,
    sum(s.total_amount) as total_spending,
    rank() over(order by sum(s.total_amount) desc ) as customer_rank
from fact_sales s
join dim_customer c on s.customer_id = c.customer_id
group by c.customer_id, c.customer_name
order by customer_rank


--  58. Use DENSE_RANK() to rank brands

select 
    p.product_id,
    p.brand,
    sum(s.total_amount),
    dense_rank() over (order by sum(s.total_amount) desc ) rank_by_brands
from fact_sales s
join dim_product p  on s.product_id = p.product_id
group by  p.product_id, p.brand
order by  rank_by_brands 

