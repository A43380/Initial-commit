--Find top 10 highest reveue generating products
select top 10 product_id, sum(sales_price) as revenue from df_order
group by product_id
order by revenue desc;

--Find top 5 highest selling products in each region
With cte as(
select product_id, region, sum(sales_price) selling_prod_region from df_order
group by product_id, region
)
select * from (
select *, row_number() over(partition by region order by selling_prod_region desc) as rn from cte) A
where rn <= 5;

--Find month over month growth comparison for 2022 and 2023 sales eg : jan 2022 vs jan 2023
with cte23 as (
	select month(order_date) as mon2023, round(sum(sales_price),2) as ts2023 from df_order where year(order_date) = 2023
	group by month(order_date)
), cte22 as (
	select month(order_date) as mon2022, round(sum(sales_price),2) as ts2022 from df_order where year(order_date) = 2022
	group by month(order_date)
)
select mon2022 as order_month, ts2022 as sales2022, ts2023 as sales2023 from cte23 inner join cte22 
on cte23.mon2023 = cte22.mon2022
order by mon2022;


--For each category which month had highest sales
with cte as(
	select category, format(order_date, 'yyyyMM') as mon, sum(sales_price) as sales from df_order
	group by category, format(order_date, 'yyyyMM')
)
select * from (
	select *, row_number() over(partition by category order by sales desc) as rn
	from cte) a 
where rn = 1;


--Which sub category had highest growth by profit in 2023 compare to 2022
with cte23 as (
	select sub_category, year(order_date) as y2023, sum(sales_price) as sales_2023 from df_order where year(order_date) = 2023
	group by sub_category, year(order_date)
), cte22 as (
	select sub_category, year(order_date) as y2022, sum(sales_price) as sales_2022 from df_order where year(order_date) = 2022
	group by sub_category, year(order_date)
)

select top 1 cte22.sub_category, sales_2022, sales_2023, (sales_2023-sales_2022) as profit from cte23 inner join cte22 on cte22.sub_category = cte23.sub_category
order by profit desc;
