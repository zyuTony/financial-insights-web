import { prisma } from "@/app/lib/prisma";

export async function GET(request) {
  try {
    // Get performance data from binance_periods_performance table
    const performance = await prisma.binance_periods_performance.findMany({
      select: {
        symbol: true,
        latest_close: true,
        avg_volume_14d: true,
        pct_change_7d: true,
        pct_change_30d: true,
        pct_change_90d: true,
        pct_change_180d: true,
        pct_change_altseason_1: true,
        pct_change_altseason_2: true,
        pct_change_altseason_3: true,
        latest_date: true,
      },
      where: {
        NOT: {
          symbol: {
            in: ["EUR", "EURI", "AEUR", "USDC", "FDUSD", "TUSD", "USDP"],
          },
        },
      },
      orderBy: {
        avg_volume_14d: "desc",
      },
    });
    // Format the performance data
    const formattedPerformance = performance.map((p) => {
      return {
        symbol: p.symbol,
        currentPrice: parseFloat(p.latest_close),
        usdVolume14d: parseFloat(p.avg_volume_14d),
        gain7d: p.pct_change_7d ? parseFloat(p.pct_change_7d) * 100 : null,
        gain30d: p.pct_change_30d ? parseFloat(p.pct_change_30d) * 100 : null,
        gain90d: p.pct_change_90d ? parseFloat(p.pct_change_90d) * 100 : null,
        gain180d: p.pct_change_180d
          ? parseFloat(p.pct_change_180d) * 100
          : null,
        gainAltseason1: p.pct_change_altseason_1
          ? parseFloat(p.pct_change_altseason_1) * 100
          : null,
        gainAltseason2: p.pct_change_altseason_2
          ? parseFloat(p.pct_change_altseason_2) * 100
          : null,
        gainAltseason3: p.pct_change_altseason_3
          ? parseFloat(p.pct_change_altseason_3) * 100
          : null,
        last_updated: p.latest_date,
      };
    });

    return new Response(JSON.stringify(formattedPerformance), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error in GET request:", error);
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
