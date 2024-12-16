-- CreateTable
CREATE TABLE "coin_historical_price" (
    "symbol" VARCHAR(20) NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "open" DECIMAL NOT NULL,
    "high" DECIMAL NOT NULL,
    "low" DECIMAL NOT NULL,
    "close" DECIMAL NOT NULL
);

-- CreateTable
CREATE TABLE "coin_pairs_coint" (
    "date" TIMESTAMPTZ(6) NOT NULL,
    "window_length" INTEGER NOT NULL,
    "symbol1" VARCHAR(50) NOT NULL,
    "symbol2" VARCHAR(50) NOT NULL,
    "pvalue" DECIMAL NOT NULL
);

-- CreateTable
CREATE TABLE "stock_historical_price" (
    "symbol" VARCHAR(10) NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "open" DECIMAL NOT NULL,
    "high" DECIMAL NOT NULL,
    "low" DECIMAL NOT NULL,
    "close" DECIMAL NOT NULL,
    "volume" BIGINT NOT NULL,

    CONSTRAINT "stock_historical_price_pkey" PRIMARY KEY ("symbol","date")
);

-- CreateTable
CREATE TABLE "stock_pairs_coint" (
    "date" TIMESTAMPTZ(6) NOT NULL,
    "window_length" INTEGER NOT NULL,
    "symbol1" VARCHAR(50) NOT NULL,
    "symbol2" VARCHAR(50) NOT NULL,
    "pvalue" DECIMAL NOT NULL
);

-- CreateTable
CREATE TABLE "stock_signal" (
    "symbol1" VARCHAR(50) NOT NULL,
    "symbol2" VARCHAR(50) NOT NULL,
    "window_length" INTEGER NOT NULL,
    "most_recent_coint_pct" DECIMAL NOT NULL,
    "recent_coint_pct" DECIMAL NOT NULL,
    "hist_coint_pct" DECIMAL NOT NULL,
    "r_squared" DECIMAL NOT NULL,
    "ols_constant" DECIMAL NOT NULL,
    "ols_coeff" DECIMAL NOT NULL,
    "last_updated" TIMESTAMPTZ(6) NOT NULL
);

-- CreateTable
CREATE TABLE "stock_overview" (
    "symbol" VARCHAR(10) NOT NULL,
    "assettype" VARCHAR(50),
    "name" VARCHAR(255),
    "description" TEXT,
    "cik" VARCHAR(10),
    "exchange" VARCHAR(10),
    "currency" VARCHAR(10),
    "country" VARCHAR(50),
    "sector" VARCHAR(50),
    "industry" VARCHAR(255),
    "address" VARCHAR(255),
    "fiscalyearend" VARCHAR(20),
    "latestquarter" DATE,
    "marketcapitalization" BIGINT,
    "ebitda" BIGINT,
    "peratio" DECIMAL(10,2),
    "pegratio" DECIMAL(10,3),
    "bookvalue" DECIMAL(10,2),
    "dividendpershare" DECIMAL(10,2),
    "dividendyield" DECIMAL(10,4),
    "eps" DECIMAL(10,2),
    "revenuepersharettm" DECIMAL(10,2),
    "profitmargin" DECIMAL(10,3),
    "operatingmarginttm" DECIMAL(10,3),
    "returnonassetsttm" DECIMAL(10,3),
    "returnonequityttm" DECIMAL(10,3),
    "revenuettm" BIGINT,
    "grossprofitttm" BIGINT,
    "dilutedepsttm" DECIMAL(10,2),
    "quarterlyearningsgrowthyoy" DECIMAL(10,3),
    "quarterlyrevenuegrowthyoy" DECIMAL(10,3),
    "analysttargetprice" DECIMAL(10,2),
    "analystratingstrongbuy" INTEGER,
    "analystratingbuy" INTEGER,
    "analystratinghold" INTEGER,
    "analystratingsell" INTEGER,
    "analystratingstrongsell" INTEGER,
    "trailingpe" DECIMAL(10,2),
    "forwardpe" DECIMAL(10,2),
    "pricetosalesratiottm" DECIMAL(10,3),
    "pricetobookratio" DECIMAL(10,2),
    "evtorevenue" DECIMAL(10,3),
    "evtoebitda" DECIMAL(10,2),
    "beta" DECIMAL(10,3),
    "high52week" DECIMAL(10,2),
    "low52week" DECIMAL(10,2),
    "movingaverage50day" DECIMAL(10,2),
    "movingaverage200day" DECIMAL(10,2),
    "sharesoutstanding" BIGINT,
    "dividenddate" DATE,
    "exdividenddate" DATE,

    CONSTRAINT "stock_overview_pkey" PRIMARY KEY ("symbol")
);

-- CreateTable
CREATE TABLE "coin_overview" (
    "symbol" VARCHAR(10) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "current_price" DECIMAL(20,8),
    "market_cap" BIGINT,
    "market_cap_rank" INTEGER,
    "fully_diluted_valuation" BIGINT,
    "total_volume" BIGINT,
    "high_24h" DECIMAL(20,8),
    "low_24h" DECIMAL(20,8),
    "price_change_24h" DECIMAL(20,8),
    "price_change_percentage_24h" DECIMAL(10,6),
    "market_cap_change_24h" BIGINT,
    "market_cap_change_percentage_24h" DECIMAL(10,6),
    "circulating_supply" DECIMAL(30,10),
    "total_supply" DECIMAL(30,10),
    "max_supply" DECIMAL(30,10),
    "ath" DECIMAL(20,8),
    "ath_date" TIMESTAMP(6),
    "atl" DECIMAL(20,8),
    "atl_date" TIMESTAMP(6),
    "last_updated" TIMESTAMP(6),

    CONSTRAINT "coin_overview_pkey" PRIMARY KEY ("symbol","name")
);

-- CreateTable
CREATE TABLE "coin_signal" (
    "symbol1" VARCHAR(50) NOT NULL,
    "symbol2" VARCHAR(50) NOT NULL,
    "window_length" INTEGER NOT NULL,
    "most_recent_coint_pct" DECIMAL NOT NULL,
    "recent_coint_pct" DECIMAL NOT NULL,
    "hist_coint_pct" DECIMAL NOT NULL,
    "r_squared" DECIMAL NOT NULL,
    "ols_constant" DECIMAL NOT NULL,
    "ols_coeff" DECIMAL NOT NULL,
    "last_updated" TIMESTAMPTZ(6) NOT NULL
);

-- CreateTable
CREATE TABLE "coin_signal_api_output" (
    "symbol1" VARCHAR(50) NOT NULL,
    "name1" VARCHAR(50) NOT NULL,
    "market_cap_1" BIGINT,
    "symbol2" VARCHAR(50) NOT NULL,
    "name2" VARCHAR(50) NOT NULL,
    "market_cap_2" BIGINT,
    "most_recent_coint_pct" DECIMAL,
    "recent_coint_pct" DECIMAL,
    "hist_coint_pct" DECIMAL,
    "r_squared" DECIMAL,
    "ols_constant" DECIMAL,
    "ols_coeff" DECIMAL,
    "last_updated" TIMESTAMPTZ(6) NOT NULL,

    CONSTRAINT "coin_signal_api_output_pkey" PRIMARY KEY ("symbol1","name1","symbol2","name2")
);

-- CreateTable
CREATE TABLE "ib_latest_trades" (
    "date" TIMESTAMPTZ(6) NOT NULL,
    "symbol" VARCHAR(10) NOT NULL,
    "action" VARCHAR(10) NOT NULL,
    "dollar_amt" DECIMAL NOT NULL,
    "price" DECIMAL NOT NULL,
    "amt" DECIMAL NOT NULL
);

-- CreateTable
CREATE TABLE "latest_trades" (
    "date" TIMESTAMPTZ(6) NOT NULL,
    "symbol" VARCHAR(10) NOT NULL,
    "action" VARCHAR(10) NOT NULL,
    "dollar_amt" DECIMAL NOT NULL,
    "price" DECIMAL NOT NULL,
    "amt" DECIMAL NOT NULL
);

-- CreateTable
CREATE TABLE "stock_signal_api_output" (
    "symbol1" VARCHAR(50) NOT NULL,
    "market_cap_1" BIGINT,
    "pe_ratio_1" DECIMAL(10,2),
    "target_price_1" DECIMAL(10,2),
    "symbol2" VARCHAR(50) NOT NULL,
    "market_cap_2" BIGINT,
    "pe_ratio_2" DECIMAL(10,2),
    "target_price_2" DECIMAL(10,2),
    "most_recent_coint_pct" DECIMAL,
    "recent_coint_pct" DECIMAL,
    "hist_coint_pct" DECIMAL,
    "r_squared" DECIMAL,
    "ols_constant" DECIMAL,
    "ols_coeff" DECIMAL,
    "last_updated" TIMESTAMPTZ(6) NOT NULL,

    CONSTRAINT "stock_signal_api_output_pkey" PRIMARY KEY ("symbol1","symbol2")
);

-- CreateTable
CREATE TABLE "backtest_trades" (
    "symbol" VARCHAR(20) NOT NULL,
    "strat_name" VARCHAR(50) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "trade_df_tf" VARCHAR(10) NOT NULL,
    "indi_df_tf" VARCHAR(10) NOT NULL,
    "param_dict" JSONB NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "action" VARCHAR(4) NOT NULL,
    "price" DECIMAL NOT NULL,

    CONSTRAINT "backtest_trades_pkey" PRIMARY KEY ("symbol","strat_name","start_date","end_date","trade_df_tf","indi_df_tf","param_dict","date")
);

-- CreateTable
CREATE TABLE "binance_coin_4hours_historical_price" (
    "symbol" VARCHAR(20) NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "open" DECIMAL NOT NULL,
    "high" DECIMAL NOT NULL,
    "low" DECIMAL NOT NULL,
    "close" DECIMAL NOT NULL,
    "volume" DECIMAL NOT NULL,

    CONSTRAINT "binance_coin_4hours_historical_price_pkey" PRIMARY KEY ("symbol","date")
);

-- CreateTable
CREATE TABLE "binance_coin_5mins_historical_price" (
    "symbol" VARCHAR(20) NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "open" DECIMAL NOT NULL,
    "high" DECIMAL NOT NULL,
    "low" DECIMAL NOT NULL,
    "close" DECIMAL NOT NULL,
    "volume" DECIMAL NOT NULL,

    CONSTRAINT "binance_coin_5mins_historical_price_pkey" PRIMARY KEY ("symbol","date")
);

-- CreateTable
CREATE TABLE "binance_coin_historical_price" (
    "symbol" VARCHAR(20) NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "open" DECIMAL NOT NULL,
    "high" DECIMAL NOT NULL,
    "low" DECIMAL NOT NULL,
    "close" DECIMAL NOT NULL,
    "volume" DECIMAL NOT NULL,

    CONSTRAINT "binance_coin_historical_price_pkey" PRIMARY KEY ("symbol","date")
);

-- CreateTable
CREATE TABLE "binance_coin_hourly_historical_price" (
    "symbol" VARCHAR(20) NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "open" DECIMAL NOT NULL,
    "high" DECIMAL NOT NULL,
    "low" DECIMAL NOT NULL,
    "close" DECIMAL NOT NULL,
    "volume" DECIMAL NOT NULL,

    CONSTRAINT "binance_coin_hourly_historical_price_pkey" PRIMARY KEY ("symbol","date")
);

-- CreateTable
CREATE TABLE "coin_hourly_historical_price" (
    "symbol" VARCHAR(20) NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "open" DECIMAL NOT NULL,
    "high" DECIMAL NOT NULL,
    "low" DECIMAL NOT NULL,
    "close" DECIMAL NOT NULL,

    CONSTRAINT "coin_hourly_historical_price_pkey" PRIMARY KEY ("symbol","date")
);

-- CreateTable
CREATE TABLE "coin_stonewell_signal" (
    "symbol" VARCHAR(50) NOT NULL,
    "close_above_sma" BOOLEAN NOT NULL,
    "close_above_sma_pct" DECIMAL NOT NULL,
    "rsi_above_sma" BOOLEAN NOT NULL,
    "short_vol_above_long" BOOLEAN NOT NULL,
    "death_cross" BOOLEAN NOT NULL,
    "last_updated" TIMESTAMPTZ(6) NOT NULL,

    CONSTRAINT "coin_stonewell_signal_pkey" PRIMARY KEY ("symbol")
);

-- CreateTable
CREATE TABLE "backtest_charts" (
    "symbol" VARCHAR(20) NOT NULL,
    "strat_name" VARCHAR(50) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "trade_df_tf" VARCHAR(10) NOT NULL,
    "indi_df_tf" VARCHAR(10) NOT NULL,
    "param_dict" JSONB NOT NULL,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "open" DECIMAL,
    "high" DECIMAL,
    "low" DECIMAL,
    "close" DECIMAL,
    "volume" DECIMAL,
    "rsi" DECIMAL,
    "rsi_2" DECIMAL,
    "volume_short_sma" DECIMAL,
    "volume_long_sma" DECIMAL,
    "close_sma" DECIMAL,
    "ema_12" DECIMAL,
    "ema_26" DECIMAL,
    "kc_upper" DECIMAL,
    "kc_lower" DECIMAL,
    "kc_middle" DECIMAL,
    "kc_position" DECIMAL,

    CONSTRAINT "backtest_charts_pkey" PRIMARY KEY ("symbol","strat_name","start_date","end_date","trade_df_tf","indi_df_tf","param_dict","date")
);

-- CreateTable
CREATE TABLE "backtest_peformances" (
    "symbol" VARCHAR(20) NOT NULL,
    "strat_name" VARCHAR(50) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "trade_df_tf" VARCHAR(10) NOT NULL,
    "indi_df_tf" VARCHAR(10) NOT NULL,
    "param_dict" JSONB NOT NULL,
    "rolling_30d_start" DATE NOT NULL,
    "rolling_30d_end" DATE NOT NULL,
    "rolling_baseline_chg_pct" DECIMAL NOT NULL,
    "rolling_profit_pct" DECIMAL NOT NULL,

    CONSTRAINT "backtest_peformances_pkey" PRIMARY KEY ("symbol","strat_name","start_date","end_date","trade_df_tf","indi_df_tf","param_dict","rolling_30d_start","rolling_30d_end")
);

-- CreateTable
CREATE TABLE "backtest_performances" (
    "symbol" VARCHAR(20) NOT NULL,
    "strat_name" VARCHAR(50) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "trade_df_tf" VARCHAR(10) NOT NULL,
    "indi_df_tf" VARCHAR(10) NOT NULL,
    "param_dict" JSONB NOT NULL,
    "rolling_30d_start" DATE NOT NULL,
    "rolling_30d_end" DATE NOT NULL,
    "rolling_baseline_chg_pct" DECIMAL NOT NULL,
    "rolling_profit_pct" DECIMAL NOT NULL,

    CONSTRAINT "backtest_performances_pkey" PRIMARY KEY ("symbol","strat_name","start_date","end_date","trade_df_tf","indi_df_tf","param_dict","rolling_30d_start","rolling_30d_end")
);

-- CreateIndex
CREATE UNIQUE INDEX "coin_historical_price_symbol_date_key" ON "coin_historical_price"("symbol", "date");

-- CreateIndex
CREATE UNIQUE INDEX "coin_pairs_coint_date_window_length_symbol1_symbol2_key" ON "coin_pairs_coint"("date", "window_length", "symbol1", "symbol2");

-- CreateIndex
CREATE UNIQUE INDEX "stock_pairs_coint_date_symbol1_symbol2_key" ON "stock_pairs_coint"("date", "symbol1", "symbol2");

-- CreateIndex
CREATE UNIQUE INDEX "stock_signal_symbol1_symbol2_window_length_key" ON "stock_signal"("symbol1", "symbol2", "window_length");

-- CreateIndex
CREATE UNIQUE INDEX "coin_overview_symbol_name_key" ON "coin_overview"("symbol", "name");

-- CreateIndex
CREATE UNIQUE INDEX "coin_signal_symbol1_symbol2_window_length_key" ON "coin_signal"("symbol1", "symbol2", "window_length");

-- CreateIndex
CREATE UNIQUE INDEX "ib_latest_trades_date_symbol_key" ON "ib_latest_trades"("date", "symbol");

-- CreateIndex
CREATE UNIQUE INDEX "latest_trades_date_symbol_key" ON "latest_trades"("date", "symbol");
