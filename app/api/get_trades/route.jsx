import { prisma } from "../../lib/prisma";

export async function GET() {
  try {
    const latest_trades = await prisma.latest_trades.findMany({
      orderBy: {
        date: "desc",
      },
    });

    const formattedSignals = latest_trades.map((trade) => ({
      ...trade,
      dollar_amt: parseFloat(trade.dollar_amt),
      price: parseFloat(trade.price),
      amt: parseFloat(trade.amt),
    }));

    return new Response(JSON.stringify(formattedSignals), {
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
