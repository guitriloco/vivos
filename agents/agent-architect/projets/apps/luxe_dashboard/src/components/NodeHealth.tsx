"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Cpu, Zap, Activity, Info } from "lucide-react";

const nodes = [
  { name: "Nexus", status: "STABLE", cpu: 12, iops: 4500, latency: 2, thermal: 32 },
  { name: "Shadow", status: "OPTIMIZED", cpu: 8, iops: 8200, latency: 1, thermal: 28 },
  { name: "Void", status: "STANDBY", cpu: 1, iops: 0, latency: 0, thermal: 24 },
  { name: "Nebula", status: "STABLE", cpu: 45, iops: 12400, latency: 5, thermal: 42 },
];

export const NodeHealth = () => {
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  return (
    <div className="glass-morphism p-8 rounded-none border-zinc-900/50 h-full">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h2 className="text-xl font-light tracking-[0.2em] uppercase text-white mb-1">
            Node Health Grid
          </h2>
          <p className="text-[10px] tracking-widest text-zinc-500 font-mono uppercase">
            Distributed Network Topology
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {nodes.map((node) => (
          <motion.div
            key={node.name}
            whileHover={{ scale: 1.02 }}
            onMouseEnter={() => setHoveredNode(node.name)}
            onMouseLeave={() => setHoveredNode(null)}
            className="p-6 bg-zinc-950 border border-zinc-900 relative group cursor-crosshair overflow-hidden"
          >
            <div className="flex justify-between items-start mb-6">
              <h3 className="text-sm font-bold tracking-widest uppercase text-white">
                {node.name}_NODE
              </h3>
              <div className="w-2 h-2 rounded-full bg-luxe-gold" />
            </div>

            <div className="space-y-4">
              <div className="flex justify-between items-end">
                <span className="text-[10px] text-zinc-600 font-mono uppercase">CPU LOAD</span>
                <div className="flex-1 mx-4 h-[1px] bg-zinc-900 overflow-hidden relative">
                   <motion.div 
                    animate={{ x: [-100, 100] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-0 w-1/4 bg-luxe-gold/30"
                   />
                </div>
                <span className="text-xs font-mono text-luxe-gold">{node.cpu}%</span>
              </div>
              
              <div className="flex justify-between items-end">
                <span className="text-[10px] text-zinc-600 font-mono uppercase">IOPS</span>
                <span className="text-xs font-mono text-zinc-400">{node.iops.toLocaleString()}</span>
              </div>

              <div className="flex justify-between items-end">
                <span className="text-[10px] text-zinc-600 font-mono uppercase">LATENCY</span>
                <span className="text-xs font-mono text-luxe-emerald">{node.latency}ms</span>
              </div>
            </div>

            {/* Hover Detail Overlay */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: hoveredNode === node.name ? 1 : 0 }}
              className="absolute inset-0 bg-black/80 backdrop-blur-sm flex flex-col justify-center items-center pointer-events-none p-4 text-center"
            >
              <Info className="w-6 h-6 text-luxe-gold mb-2" />
              <span className="text-[10px] font-mono text-luxe-gold uppercase tracking-[0.2em] mb-1">Thermal: {node.thermal}°C</span>
              <span className="text-[10px] font-mono text-luxe-emerald uppercase tracking-[0.2em]">{node.status}</span>
            </motion.div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
