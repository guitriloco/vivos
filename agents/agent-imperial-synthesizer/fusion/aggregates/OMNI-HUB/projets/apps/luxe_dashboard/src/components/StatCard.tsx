"use client";
import React from "react";
import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface StatCardProps {
  title: string;
  value: string | number;
  trend?: number;
  icon: LucideIcon;
  variant?: "gold" | "emerald" | "ruby" | "zinc";
  label?: string;
}

export const StatCard = ({
  title,
  value,
  trend,
  icon: Icon,
  variant = "zinc",
  label,
}: StatCardProps) => {
  const variantStyles = {
    gold: "border-luxe-gold/20 text-luxe-gold glow-gold",
    emerald: "border-luxe-emerald/20 text-luxe-emerald glow-emerald",
    ruby: "border-luxe-ruby/20 text-luxe-ruby shadow-ruby/20",
    zinc: "border-zinc-800 text-zinc-400",
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      className={cn(
        "glass-morphism p-6 rounded-none relative overflow-hidden group",
        variantStyles[variant]
      )}
    >
      <div className="flex justify-between items-start mb-4">
        <div className="p-2 bg-zinc-900/50 border border-zinc-800 group-hover:border-current transition-colors">
          <Icon className="w-5 h-5" />
        </div>
        {trend !== undefined && (
          <span
            className={cn(
              "text-xs font-mono",
              trend >= 0 ? "text-luxe-emerald" : "text-luxe-ruby"
            )}
          >
            {trend >= 0 ? "+" : ""}
            {trend}%
          </span>
        )}
      </div>

      <div>
        <p className="text-[10px] uppercase tracking-[0.2em] mb-1 font-bold text-zinc-500">
          {title}
        </p>
        <h3 className="text-3xl font-light tracking-tight text-white font-mono">
          {value}
        </h3>
        {label && (
          <p className="text-[10px] font-mono mt-2 text-zinc-600 italic">
            {label}
          </p>
        )}
      </div>

      <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-current to-transparent opacity-20" />
    </motion.div>
  );
};
