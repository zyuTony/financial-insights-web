import { prisma } from "@/app/lib/prisma";
export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const signals = await prisma.stock_signal_api_output.findMany({
      where: {
        most_recent_coint_pct: { gt: 0.5 },
        recent_coint_pct: { gt: 0.3 },
        hist_coint_pct: { gt: 0.2 },
        r_squared: { gt: 0.5 },
      },
      orderBy: {
        most_recent_coint_pct: "desc",
      },
    });

    const formattedSignals = signals.map((signal) => ({
      ...signal,
      most_recent_coint_pct: parseFloat(signal.most_recent_coint_pct),
      recent_coint_pct: parseFloat(signal.recent_coint_pct),
      hist_coint_pct: parseFloat(signal.hist_coint_pct),
      ols_constant: parseFloat(signal.ols_constant),
      ols_coeff: parseFloat(signal.ols_coeff),
      r_squared: parseFloat(signal.r_squared),
      market_cap_1: signal.market_cap_1 ? parseInt(signal.market_cap_1) : null,
      market_cap_2: signal.market_cap_2 ? parseInt(signal.market_cap_2) : null,
      pe_ratio_1: signal.pe_ratio_1 ? parseFloat(signal.pe_ratio_1) : null,
      pe_ratio_2: signal.pe_ratio_2 ? parseFloat(signal.pe_ratio_2) : null,
      target_price_1: signal.target_price_1
        ? parseFloat(signal.target_price_1)
        : null,
      target_price_2: signal.target_price_2
        ? parseFloat(signal.target_price_2)
        : null,
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
