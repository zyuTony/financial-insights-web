"use client";
import { useEffect } from "react";
import { motion } from "framer-motion";
import Lenis from "@studio-freight/lenis";

export default function Home() {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      direction: "vertical",
      gestureDirection: "vertical",
      smooth: true,
      smoothTouch: false,
      touchMultiplier: 2,
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);

    return () => {
      lenis.destroy();
    };
  }, []);

  return (
    <div className="flex flex-col w-full">
      {/* How It Works */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
        className="py-20 bg-gray-50"
      >
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-normal text-center mb-12 tracking-widest uppercase">
            How It Works
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            {[1, 2].map((num, i) => (
              <motion.div
                key={num}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.2, duration: 0.8 }}
                className="text-center p-6"
              >
                <div className="bg-emerald-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-normal">{num}</span>
                </div>
                <h3 className="font-normal mb-2 tracking-widest uppercase">
                  {num === 1 && "Pair Trading Analysis"}
                  {num === 2 && "Performance Comparison"}
                </h3>
                <p className="text-gray-600 tracking-widest font-normal">
                  {num === 1 &&
                    "Discover cointegrated pairs for statistical arbitrage opportunities"}
                  {num === 2 &&
                    "Compare asset performance across different time periods"}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Personal Links */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
        className="py-20"
      >
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-normal text-center mb-12 tracking-widest uppercase">
            Connect With Me
          </h2>
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { title: "GitHub", link: "https://github.com/zyuTony" },
              {
                title: "Personal Website",
                link: "https://self-intro-iota.vercel.app/",
              },
              {
                title: "LinkedIn",
                link: "https://linkedin.com/in/z-yu",
              },
              {
                title: "Medium",
                link: "https://medium.com/@zongyuan1998",
              },
            ].map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.2, duration: 0.8 }}
                className="text-center"
              >
                <a
                  href={item.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block p-4 hover:bg-gray-50 rounded-lg transition-colors duration-300"
                >
                  <h3 className="font-normal text-xl mb-2 tracking-widest uppercase">
                    {item.title}
                  </h3>
                </a>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>
    </div>
  );
}
