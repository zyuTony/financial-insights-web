--------------------------------------------------------------------------------------
--Find all pairs that are recently cointegrated, ranked by potential reward currently
with key_pairs as (
    select *, row_number() over (partition by symbol order by date desc) as rn
    from stock_historical_price
),
key_pairs_120d as (
    select *
    from key_pairs
    where rn <= 120
),
ols_spread as (
    select a.date, a.symbol as symbol_a, b.symbol as symbol_b,
    a.close as close_a, b.close as close_b, 
    a.close - c.ols_coeff * b.close as ols_spread, c.*
    from key_pairs_120d a 
    join key_pairs_120d b
    on a.date = b.date
    join stock_signal c
    on c.symbol1 = a.symbol and c.symbol2 = b.symbol
	where c.most_recent_coint_pct > 0.8 --ADJUSTABLE
),
bb_band as (
    select *,
    coalesce(avg(ols_spread) over (partition by symbol_a, symbol_b order by date rows between 19 preceding and current row), ols_spread) as sma,--ADJUSTABLE
    coalesce(stddev(ols_spread) over (partition by symbol_a, symbol_b order by date rows between 19 preceding and current row), 0) as sd--ADJUSTABLE
    from ols_spread
),
ranked_results as (
    select 
    symbol_a, symbol_b, date,
	round(close_a, 2) as close_a, round(close_b, 2) as close_b,
	round(ols_spread, 2) as ols_spread,
	round(most_recent_coint_pct, 2) as most_recent_coint_pct, 
    round(recent_coint_pct, 2) as recent_coint_pct, 
    round(hist_coint_pct, 2) as hist_coint_pct, 
	round(r_squared, 2) as r_squared, 
    round(ols_constant, 2) as ols_constant, 
    round(ols_coeff, 3) as ols_coeff,  
    round(((ols_spread - sma)/nullif(2 * sd, 0)) * 100, 0) as key_score,
	case 
        when abs(ols_coeff) < 1 then round(close_a/abs(ols_coeff) + close_b, 2)
        else round(close_a + abs(ols_coeff)*close_b, 2)
    end as investment,
	round(abs(ols_spread - sma), 2) as potential_win,
	round(sma, 2) as rolling_mean,
	round(sma + 2 * sd, 2) as upper_band, round(sma - 2 * sd, 2) as lower_band,
    row_number() over (partition by symbol_a, symbol_b order by date desc) as rn
    from bb_band
)
select 
symbol_a, symbol_b, date, 
most_recent_coint_pct, recent_coint_pct, hist_coint_pct, 
r_squared, ols_constant, ols_coeff, 
close_a, close_b, ols_spread, 
key_score, investment, potential_win,
round(potential_win/investment, 4) as potential_win_pct,
rolling_mean, upper_band, lower_band
from ranked_results
where rn = 1
order by potential_win_pct desc;


-- select * from stock_signal 
-- order by most_recent_coint_pct desc, recent_coint_pct desc, hist_coint_pct desc




