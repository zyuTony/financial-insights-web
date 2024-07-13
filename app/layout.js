import { Inter } from "next/font/google";
import "./globals.css";
import NavMenu from "./components/Navbar";
import Footer from "./components/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Fin Tools",
  description: "finacial tool for retail investors",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="flex flex-col w-full h-screen justify-between">
        <NavMenu />
        {children}
        <Footer />
      </body>
    </html>
  );
}
