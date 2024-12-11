import Link from "next/link";

export default function NavMenu() {
  const dropdownWidth = "w-60";
  const dropdownItemHoverColor = "hover:bg-gray-100";
  const dropdownItemPadding = "pl-1 pr-6 py-1";
  const dropdownItemFontWeight = "font-semibold";
  const dropdownItemFontSize = "text-sm";

  return (
    //flex-row with items-center: place items along the middle of crossaxis (Y axis for flex-row)
    //and justify-center: place items along middle of the main axis (X axis for flex-row)
    // z-50-always shown when stacked; 'sticky-fixed when scrol' on top left; take full width;
    <nav className="sticky flex flex-row items-center justify-center top-0 left-0 z-50 w-full border-b-2 border-green-600 bg-white bg-opacity-85">
      {/* home button; 32X6 padding */}
      <div className="px-10 py-6">
        <Link
          href="/"
          className="text-green-800 hover:text-green-600 text-2xl font-semibold"
        >
          <span>eutra insights</span>
        </Link>
      </div>

      {/* nav menu items; 10X6 padding*/}
      <div className="px-10 py-6 flex">
        {/* 'group' to ensure hover on this div get inherited to child divs */}
        {/* 'relative' to absolute children are positioned relative to this div */}
        <div className="relative group">
          <Link
            href="/todo"
            className="text-black hover:text-black text-medium font-bold pr-12 py-2"
          >
            Trading Signals
          </Link>
          <div
            className={`absolute left-0 top-full mt-1 hidden group-hover:block bg-white border border-gray-200 rounded-md shadow-md ${dropdownWidth}`}
          >
            <div className="py-2">
              <Link
                href="/trading_signals/stock_pair_cointegration"
                className="block px-4 py-2 text-left"
              >
                <span
                  className={`${dropdownItemHoverColor} ${dropdownItemPadding} ${dropdownItemFontWeight} ${dropdownItemFontSize} rounded`}
                >
                  Pairs Cointegration - Stock
                </span>
              </Link>
              <Link
                href="/trading_signals/crypto_pair_cointegration"
                className="block px-4 py-2 text-left"
              >
                <span
                  className={`${dropdownItemHoverColor} ${dropdownItemPadding} ${dropdownItemFontWeight} ${dropdownItemFontSize} rounded`}
                >
                  Pairs Cointegration - Crypto
                </span>
              </Link>
              <Link href="/todo" className="block px-4 py-2 text-left">
                <span
                  className={`${dropdownItemHoverColor} ${dropdownItemPadding} ${dropdownItemFontWeight} ${dropdownItemFontSize} rounded`}
                >
                  Coming Soon
                </span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
