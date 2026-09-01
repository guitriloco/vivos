"use client";
import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Hash, CheckCircle2, RefreshCw, XCircle } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface Transaction {
  id: string;
  hash: string;
  value: string;
  status: "APPROVED" | "SYNCING" | "VOID";
  timestamp: string;
}

export const GlobalLedger = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const generateTx = () => {
      const statuses: Transaction["status"][] = ["APPROVED", "SYNCING", "VOID"];
      const newTx: Transaction = {
        id: Math.random().toString(36).substring(2, 9),
        hash: "0x" + Math.random().toString(16).substring(2, 40),
        value: (Math.random() * 10).toFixed(4) + " SPECTRE",
        status: statuses[Math.floor(Math.random() * statuses.length)],
        timestamp: new Date().toLocaleTimeString(),
      };
      setTransactions((prev) => [newTx, ...prev.slice(0, 9)]);
    };

    generateTx();
    const interval = setInterval(generateTx, 3000);
    
    // Simulate connection attempt
    const timer = setTimeout(() => setIsConnected(true), 2000);

    return () => {
      clearInterval(interval);
      clearTimeout(timer);
    };
  }, []);

  return (
    <div className="glass-morphism p-8 rounded-none border-zinc-900/50 h-full">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h2 className="text-xl font-light tracking-[0.2em] uppercase text-white mb-1">
            Global Ledger Feed
          </h2>
          <p className="text-[10px] tracking-widest text-zinc-500 font-mono uppercase">
            Mirror Protocol V5.2 // Live Audit
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-zinc-900 px-4 py-2 border border-zinc-800">
          <div className={cn(
            "w-2 h-2 rounded-full animate-pulse",
            isConnected ? "bg-luxe-emerald" : "bg-luxe-ruby"
          )} />
          <span className="text-[10px] font-mono text-zinc-400">
            {isConnected ? "SYNCED" : "CONNECTING..."}
          </span>
        </div>
      </div>

      <div className="space-y-3 font-mono">
        <div className="grid grid-cols-12 text-[10px] text-zinc-600 uppercase pb-4 border-b border-zinc-900 font-bold tracking-widest">
          <div className="col-span-2">ID</div>
          <div className="col-span-5">HASH</div>
          <div className="col-span-2 text-right">VALUE</div>
          <div className="col-span-3 text-right">STATUS</div>
        </div>

        <div className="relative overflow-hidden min-h-[400px]">
          <AnimatePresence initial={false}>
            {transactions.map((tx) => (
              <motion.div
                key={tx.id}
                initial={{ x: -10, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: 10, opacity: 0 }}
                className="grid grid-cols-12 text-xs py-4 border-b border-zinc-900 group hover:bg-zinc-900/40 transition-colors"
              >
                <div className="col-span-2 text-zinc-400">#{tx.id}</div>
                <div className="col-span-5 text-zinc-500 truncate group-hover:text-luxe-gold transition-colors pr-4">
                  {tx.hash}
                </div>
                <div className="col-span-2 text-right text-white font-medium">
                  {tx.value}
                </div>
                <div className="col-span-3 text-right">
                  <span
                    className={
                      tx.status === "APPROVED"
                        ? "text-luxe-emerald"
                        : tx.status === "SYNCING"
                        ? "text-luxe-gold"
                        : "text-luxe-ruby"
                    }
                  >
                    {tx.status}
                  </span>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};
