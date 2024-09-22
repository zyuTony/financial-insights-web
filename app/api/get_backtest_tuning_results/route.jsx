import { prisma } from "../../lib/prisma";

export async function GET() {
  try {
    const backtestPerformances = await prisma.backtest_performances.findMany({
      orderBy: [
        { symbol: "asc" },
        { strat_name: "asc" },
        { start_date: "asc" },
        { rolling_30d_start: "asc" },
      ],
    });

    const backtestCharts = await prisma.backtest_charts.findMany({
      orderBy: [
        { symbol: "asc" },
        { strat_name: "asc" },
        { start_date: "asc" },
      ],
    });

    const backtestTrades = await prisma.backtest_trades.findMany({
      orderBy: [
        { symbol: "asc" },
        { strat_name: "asc" },
        { start_date: "asc" },
      ],
    });

    const backtestPerformancesOutput = backtestPerformances.map((result) => ({
      symbol: result.symbol,
      strat_name: result.strat_name,
      start_date: result.start_date.toISOString().split(".")[0],
      end_date: result.end_date.toISOString().split(".")[0],
      trade_df_tf: result.trade_df_tf,
      indi_df_tf: result.indi_df_tf,
      params: result.param_dict,
      rolling_30d_start: result.rolling_30d_start.toISOString().split(".")[0],
      rolling_30d_end: result.rolling_30d_end.toISOString().split(".")[0],
      baseline_pct: result.rolling_baseline_chg_pct,
      profit_pct: result.rolling_profit_pct,
    }));

    const backtestChartsOutput = backtestCharts.map((result) => ({
      symbol: result.symbol,
      strat_name: result.strat_name,
      start_date: result.start_date.toISOString().split(".")[0],
      end_date: result.end_date.toISOString().split(".")[0],
      trade_df_tf: result.trade_df_tf,
      indi_df_tf: result.indi_df_tf,
      params: result.param_dict,
      date: result.date.toISOString().split(".")[0],
      open: parseFloat(result.open),
      high: parseFloat(result.high),
      low: parseFloat(result.low),
      close: parseFloat(result.close),
      volume: parseFloat(result.volume),
    }));

    const backtestTradesOutput = backtestTrades.map((result) => ({
      symbol: result.symbol,
      strat_name: result.strat_name,
      start_date: result.start_date.toISOString().split(".")[0],
      end_date: result.end_date.toISOString().split(".")[0],
      trade_df_tf: result.trade_df_tf,
      indi_df_tf: result.indi_df_tf,
      params: result.param_dict,
      date: result.date.toISOString().split(".")[0],
      action: result.action,
      price: parseFloat(result.price),
    }));

    return new Response(
      JSON.stringify({
        backtestPerformancesOutput,
        backtestChartsOutput,
        backtestTradesOutput,
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({
        error: "Failed to retrieve data",
        message: error.message,
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}
