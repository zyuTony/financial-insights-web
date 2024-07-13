import Link from "next/link";

export default function Footer() {
  return (
    // 1 fixed width column with 96 length
    // + 3 variable width columns with min 48 length
    <footer className="w-full flex flex-row bg-gray-200">
      {/* 4X6 padding - 28 left X margin - fixed width */}
      <div className="flex-none w-96 py-6 px-4 mr-28">
        <p>
          &copy; {new Date().getFullYear()} eutra LLC. All rights reserved.
          eutra® is a registered trademark.
        </p>
        <p className="text-sm mt-4">
          This website is provided “as is” without any representations or
          warranties, express or implied. eutra makes no representations or
          warranties in relation to this website or the information and
          materials provided on this website. Nothing on this website
          constitutes, or is meant to constitute, advice of any kind. If you
          require advice in relation to any financial matter you should consult
          an appropriate professional.
        </p>
      </div>
      {/* 4X6 padding - variable width with min 48 length */}
      <div className="flex-auto w-48 py-6 px-4">
        <h3 className="font-bold">About eutra</h3>
        <ul className="list-none mt-2">
          <li>
            <a href="#" className="text-black hover:underline">
              Writing Team
            </a>
          </li>
          <li>
            <a href="#" className="text-black hover:underline">
              Webinars
            </a>
          </li>
          <li>
            <a href="#" className="text-black hover:underline">
              Privacy Policy
            </a>
          </li>
          <li>
            <a href="#" className="text-black hover:underline">
              Terms and Conditions
            </a>
          </li>
        </ul>
      </div>
      {/* 4X6 padding - variable width with min 48 length */}
      <div className="flex-auto w-48 py-6 px-4">
        <h3 className="font-bold">Top Investors</h3>
        <ul className="list-none mt-2">
          <li>
            <a href="#" className="text-black hover:underline">
              Berkshire Hathaway
            </a>
          </li>
          <li>
            <a href="#" className="text-black hover:underline">
              Scion Asset Management
            </a>
          </li>
        </ul>
      </div>
      {/* 4X6 padding - variable width with min 48 length */}
      <div className="flex-auto w-48 py-6 px-4">
        <h3 className="font-bold">TBD</h3>
        <ul className="list-none mt-2">
          <li>
            <a href="#" className="text-black hover:underline">
              xxxx xxxx
            </a>
          </li>
          <li>
            <a href="#" className="text-black hover:underline">
              xxxx xxxx
            </a>
          </li>
        </ul>
      </div>
      {/* 4X6 padding - variable width with min 48 length */}
      <div className="flex-auto w-48 py-6 px-4">
        <h3 className="font-bold">TBD</h3>
        <ul className="list-none mt-2">
          <li>
            <a href="#" className="text-black hover:underline">
              xxxx xxxx
            </a>
          </li>
          <li>
            <a href="#" className="text-black hover:underline">
              xxxx xxxx
            </a>
          </li>
        </ul>
      </div>
    </footer>
  );
}
