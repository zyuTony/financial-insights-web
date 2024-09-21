import { prisma } from "../../lib/prisma";

export async function GET() {
  try {
    const backtest_rolling_result =
      await prisma.backtest_tuning_rolling_results.findMany({
        orderBy: [
          { strat_name: "asc" },
          { start_date: "asc" },
          { end_date: "asc" },
          { rolling_30d_end: "asc" },
        ],
      });

    const tuningResult = backtest_rolling_result.map((result) => ({
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

    return new Response(JSON.stringify({ tuningResult }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
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
