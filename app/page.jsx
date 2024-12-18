"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [currentTime, setCurrentTime] = useState("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(now.toUTCString());
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col justify-start h-full w-full bg-white text-black">
      <h1 className="text-center text-3xl mt-16 font-mono">
        {">"} CRYPTO_INSIGHTS v1.0.0 _
      </h1>
      <div className="text-center mt-8 font-mono bg-black text-green-400 max-w-xl mx-auto p-4 rounded">
        <div className="grid grid-cols-1 gap-2 text-left">
          <p>
            <span className="text-green-600">$</span>{" "}
            <span className="text-gray-500">UTC:</span> {currentTime}
          </p>
          <p>
            <span className="text-green-600">$</span>{" "}
            <span className="text-gray-500">EST:</span>{" "}
            {new Date().toLocaleString("en-US", {
              timeZone: "America/New_York",
            })}
          </p>
          <p>
            <span className="text-green-600">$</span>{" "}
            <span className="text-gray-500">PST:</span>{" "}
            {new Date().toLocaleString("en-US", {
              timeZone: "America/Los_Angeles",
            })}
          </p>
          <p>
            <span className="text-green-600">$</span>{" "}
            <span className="text-gray-500">JST:</span>{" "}
            {new Date().toLocaleString("en-US", { timeZone: "Asia/Tokyo" })}
          </p>
          <p className="border-t border-green-800 pt-2">
            <span className="text-green-600">$</span>{" "}
            <span className="text-gray-500">UNIX:</span>{" "}
            <span className="text-yellow-400">
              {Math.floor(Date.now() / 1000)}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}
