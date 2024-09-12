import { prisma } from "../../lib/prisma";

export async function GET() {
  try {
    const backtest_prices = await prisma.backtest_price.findMany({
      orderBy: {
        date: "asc",
      },
    });

    const backtest_trades = await prisma.backtest_trades.findMany({
      orderBy: {
        date: "asc",
      },
    });

    const priceData = backtest_prices.map((price) => ({
      date: price.date.toISOString().split(".")[0],
      open: parseFloat(price.open),
      high: parseFloat(price.high),
      low: parseFloat(price.low),
      close: parseFloat(price.close),
      volume: parseFloat(price.volume),
      symbol: price.symbol,
      RSI: parseFloat(price.rsi),
      RSI_2: parseFloat(price.rsi_2),
      close_SMA: parseFloat(price.close_sma),
      volume_short_sma: parseFloat(price.volume_short_sma),
      volume_long_sma: parseFloat(price.volume_long_sma),
    }));

    const tradesData = backtest_trades.map((trade) => ({
      date: trade.date.toISOString().split(".")[0],
      action: trade.action.toLowerCase(),
      symbol: trade.symbol,
      price: parseFloat(trade.price),
    }));

    return new Response(JSON.stringify({ priceData, tradesData }), {
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
