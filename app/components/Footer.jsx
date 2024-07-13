import Link from "next/link";

// export default function Footer() {
//   return (
//     <footer className="w-full bg-white bg-opacity-95 py-6 fixed bottom-0 left-0 z-50">
//       <div className="mx-auto px-4 flex justify-center items-center">
//         <p className="text-center">
//           &copy; {new Date().getFullYear()} eutra LLC. All rights reserved.
//         </p>
//       </div>
//     </footer>
//   );
// }

export default function Footer() {
  return (
    <footer className="w-full bg-gray-200 py-8">
      <div className="flex flex- mx-auto px-4 grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="col-span-1 md:col-span-2">
          <p>
            &copy; {new Date().getFullYear()} Eutra LLC. All rights reserved.
            Eutra® is a registered trademark.
          </p>
          <ul className="list-none mt-4">
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
          <p className="text-sm mt-4">
            This website is provided “as is” without any representations or
            warranties, express or implied. Eutra makes no representations or
            warranties in relation to this website or the information and
            materials provided on this website. Nothing on this website
            constitutes, or is meant to constitute, advice of any kind. If you
            require advice in relation to any financial matter you should
            consult an appropriate professional.
          </p>
        </div>
        <div>
          <h3 className="font-bold">About Eutra</h3>
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
          </ul>
        </div>
        <div>
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
        <div>
          <h3 className="font-bold">Features</h3>
          <ul className="list-none mt-2">
            <li>
              <a href="#" className="text-black hover:underline">
                Pre-Built Screens
              </a>
            </li>
            <li>
              <a href="#" className="text-black hover:underline">
                Short Interest Data
              </a>
            </li>
          </ul>
        </div>
        <div>
          <h3 className="font-bold">Explore</h3>
          <ul className="list-none mt-2">
            <li>
              <a href="#" className="text-black hover:underline">
                Workbench
              </a>
            </li>
            <li>
              <a href="#" className="text-black hover:underline">
                Portfolio Builder
              </a>
            </li>
          </ul>
        </div>
        <div>
          <h3 className="font-bold">Help Center</h3>
          <ul className="list-none mt-2">
            <li>
              <a href="#" className="text-black hover:underline">
                Visit Help Center
              </a>
            </li>
            <li>
              <a href="#" className="text-black hover:underline">
                Technical Support
              </a>
            </li>
          </ul>
        </div>
      </div>
    </footer>
  );
}
