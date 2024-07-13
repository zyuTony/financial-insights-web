import Link from "next/link";

export default function NavMenu() {
  return (
    <nav className="w-full bg-white bg-opacity-95 border-b-2 border-green-600 fixed top-0 left-0 z-50">
      <div className="flex px-4 py-6 justify-start items-center">
        {/* logo - home button */}
        <div className="flex px-16">
          <Link
            href="/"
            className="text-green-500 hover:text-blue-900 text-lg font-bold"
          >
            Fin Tools
          </Link>
        </div>

        {/* nav menu items */}
        <div className="flex px-10">
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
      </div>
    </nav>
  );
}
