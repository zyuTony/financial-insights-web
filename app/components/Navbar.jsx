import Link from "next/link";

export default function NavMenu() {
  return (
    //flex-row with items-center: place items along the middle of crossaxis (Y axis for flex-row)
    //and justify-center: place items along middle of the main axis (X axis for flex-row)
    // z-50-always shown when stacked; 'sticky-fixed when scrol' on top left; take full width;
    <nav className="sticky flex flex-row items-center justify-center top-0 left-0 z-50 w-full border-b-2 border-green-600 bg-white bg-opacity-85">
      {/* home button; 32X6 padding */}
      <div className="px-20 py-6">
        <Link
          href="/"
          className="text-green-500 hover:text-blue-900 text-lg font-bold"
        >
          Fin Tools
        </Link>
      </div>

      {/* nav menu items; 10X6 padding*/}
      <div className="px-10 py-6">
        <Link
          href="/"
          className="text-black hover:text-black text-medium font-bold px-6"
        >
          Dashboard
        </Link>
        <Link
          href="/"
          className="text-black hover:text-black text-medium font-bold px-6"
        >
          Charts
        </Link>
        <Link
          href="/"
          className="text-black hover:text-black text-medium font-bold px-6"
        >
          Workbench
        </Link>
        <Link
          href="/"
          className="text-black hover:text-black text-medium font-bold px-6"
        >
          Crypto
        </Link>
        <Link
          href="/"
          className="text-black hover:text-black text-medium font-bold px-6"
        >
          Macro
        </Link>
      </div>
    </nav>
  );
}
