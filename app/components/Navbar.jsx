import Link from "next/link";

export default function NavMenu() {
  const dropdownWidth = "w-40"; // Changed from w-60 to w-40
  const dropdownItemHoverColor = "hover:bg-gray-100";
  const dropdownItemPadding = "pl-1 pr-3 py-1";
  const dropdownItemFontWeight = "font-normal";
  const dropdownItemFontSize = "text-sm tracking-widest uppercase";

  return (
    <nav className="sticky flex flex-row items-center justify-center top-0 left-0 z-50 w-full border-b-2 border-green-600 bg-white bg-opacity-85">
      <div className="px-10 py-6">
        <Link
          href="/"
          className="text-grey-800 hover:text-green-600 text-2xl font-normal tracking-widest uppercase"
        >
          <span>Trader Insights</span>
        </Link>
      </div>

      <div className="px-10 py-6 flex">
        <div className="relative group">
          <span className="text-black hover:text-black text-medium font-normal tracking-widest uppercase pr-12 py-2">
            Pair Trading
          </span>
          <div
            className={`absolute left-0 top-full mt-1 hidden group-hover:block bg-white border border-gray-200 rounded-md shadow-md ${dropdownWidth}`}
          >
            <div className="py-2">
              {/* <Link
                href="/trading_signals/stock_pair_cointegration"
                className="block px-4 py-2 text-left"
              >
                <span
                  className={`${dropdownItemHoverColor} ${dropdownItemPadding} ${dropdownItemFontWeight} ${dropdownItemFontSize} rounded`}
                >
                  Stocks
                </span>
              </Link> */}
              <Link
                href="/trading_signals/crypto_pair_cointegration"
                className="block px-4 py-2 text-left"
              >
                <span
                  className={`${dropdownItemHoverColor} ${dropdownItemPadding} ${dropdownItemFontWeight} ${dropdownItemFontSize} rounded`}
                >
                  Crypto
                </span>
              </Link>
              {/* <Link href="/todo" className="block px-4 py-2 text-left">
                <span
                  className={`${dropdownItemHoverColor} ${dropdownItemPadding} ${dropdownItemFontWeight} ${dropdownItemFontSize} rounded`}
                >
                  more to come
                </span>
              </Link> */}
            </div>
          </div>
        </div>
        <div className="relative group">
          <span className="text-black hover:text-black text-medium font-normal tracking-widest uppercase pr-12 py-2">
            Performance
          </span>
          <div
            className={`absolute left-0 top-full mt-1 hidden group-hover:block bg-white border border-gray-200 rounded-md shadow-md ${dropdownWidth}`}
          >
            <div className="py-2">
              <Link href="/perf/cryptos" className="block px-4 py-2 text-left">
                <span
                  className={`${dropdownItemHoverColor} ${dropdownItemPadding} ${dropdownItemFontWeight} ${dropdownItemFontSize} rounded`}
                >
                  Crypto
                </span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
