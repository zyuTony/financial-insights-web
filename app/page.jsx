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
        <span className="text-green-500">&gt;</span> Welcome to the System
      </h1>
      <div className="text-center text-md mt-12 font-mono">
        <p className="mb-2">
          <span className="text-green-500">&gt;</span> Initiating connection...
        </p>
        <p className="mb-2">
          <span className="text-green-500">&gt;</span> Access granted: Tony
          Zongyuan Yu
        </p>
        <p className="mb-2">
          <span className="text-green-500">&gt;</span> Loading trading insights
          and signals...
        </p>
      </div>
      <div className="text-center text-md mt-4 font-mono">
        <p className="mb-2">
          <span className="text-green-500">&gt;</span> Current UTC:{" "}
          {currentTime}
        </p>
      </div>
      <p className="text-center text-md text-gray-500 mt-4 font-mono animate-pulse">
        <span className="text-green-500">&gt;</span> Signals refreshed daily_
      </p>
    </div>
  );
}
