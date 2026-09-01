"use client";
import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Shield, Clock, Terminal, Activity } from "lucide-react";

export const Header = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="glass-morphism py-6 px-10 border-b border-zinc-900 sticky top-0 z-50 flex justify-between items-center backdrop-blur-xl bg-black/60">
      <div className="flex items-center space-x-8">
        <motion.div
          initial={{ rotate: -90, opacity: 0 }}
          animate={{ rotate: 0, opacity: 1 }}
          transition={{ duration: 1, ease: "circOut" }}
          className="p-3 border-2 border-luxe-gold glow-gold relative"
        >
          <Shield className="w-8 h-8 text-luxe-gold" />
          <div className="absolute -top-1 -right-1 w-2 h-2 bg-luxe-gold" />
          <div className="absolute -bottom-1 -left-1 w-2 h-2 bg-luxe-gold" />
        </motion.div>
        <div>
          <h1 className="text-2xl font-light tracking-[0.3em] uppercase text-white mb-1">
            Sovereign <span className="font-bold">Luxe</span>
          </h1>
          <div className="flex items-center space-x-3 text-[10px] tracking-widest text-zinc-500 font-mono">
            <span className="flex items-center">
              <Activity className="w-3 h-3 mr-1 text-luxe-emerald" />
              SYSTEM ACTIVE
            </span>
            <span className="w-1 h-1 bg-zinc-800 rounded-full" />
            <span className="flex items-center">
              <Terminal className="w-3 h-3 mr-1" />
              ROOT ARCHITECT ACCESS
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-12">
        <div className="hidden md:flex flex-col items-end">
          <p className="text-[10px] tracking-[0.2em] text-zinc-500 mb-1 uppercase">
            Global Mirror Clock
          </p>
          <div className="flex items-center font-mono text-xl font-light text-luxe-gold">
            <Clock className="w-4 h-4 mr-2 opacity-50" />
            {time.toLocaleTimeString("en-US", {
              hour12: false,
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
            })}
          </div>
        </div>

        <div className="flex space-x-2">
          {[1, 2, 3].map((i) => (
            <motion.div
              key={i}
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.5,
              }}
              className="w-1 h-8 bg-luxe-gold/40"
            />
          ))}
        </div>
      </div>
    </header>
  );
};
