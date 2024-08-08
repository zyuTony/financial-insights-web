-- create or replace temporary view ta_indicators as  
with btc_prices as (
    select symbol, date, close 
    from coin_historical_price
    where symbol = 'BTCUSDT'
),
in_btc_prices as (
select a.symbol, a.date, a.close/b.close as price_in_btc
from coin_historical_price a 
join btc_prices b 
on a.date=b.date
), 
add_ta as (
select symbol, date, price_in_btc,
avg(price_in_btc) over (partition by symbol order by date rows between 139 preceding and current row) as sma_140d
from in_btc_prices
order by symbol, date
),
eval_ta as (
select *,
max(date) over(partition by symbol) - min(date) over(partition by symbol) as data_points,
case when price_in_btc >= sma_140d then 1 else 0 end as above_140d_sma 
from add_ta
),
ta_result as (
select symbol, data_points,
(100*sum(above_140d_sma)::float / count(*)::float) as pct_above_140d_sma
from eval_ta
group by symbol,data_points)

select *
from eval_ta where symbol='AIOZUSDT'





