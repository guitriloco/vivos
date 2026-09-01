"use client";
import React from "react";
import { Header } from "@/components/Header";
import { NeuralMesh } from "@/components/NeuralMesh";
import { StatCard } from "@/components/StatCard";
import { GlobalLedger } from "@/components/GlobalLedger";
import { NodeHealth } from "@/components/NodeHealth";
import { SpectreYield } from "@/components/SpectreYield";
import { CommandCenter } from "@/components/CommandCenter";
import { 
  TrendingUp, 
  Server, 
  Layers, 
  ShieldCheck 
} from "lucide-react";

export default function Dashboard() {
  return (
    <main className="min-h-screen bg-black text-white selection:bg-luxe-gold/30 overflow-x-hidden">
      <NeuralMesh />
      <Header />
      
      <div className="relative z-10 p-6 md:p-10 space-y-10">
        {/* Top Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard 
            title="SPECTRE_YIELD" 
            value="6.82%" 
            trend={12.4} 
            icon={TrendingUp} 
            variant="gold"
            label="12h Aggregated Performance"
          />
          <StatCard 
            title="Node Latency" 
            value="1.2ms" 
            trend={-4.2} 
            icon={Server} 
            variant="emerald"
            label="Global Mesh Average"
          />
          <StatCard 
            title="Ledger Integrity" 
            value="100.0%" 
            icon={ShieldCheck} 
            variant="zinc"
            label="No Unconfirmed Deltas"
          />
          <StatCard 
            title="IOPS Throughput" 
            value="42,800" 
            trend={8.1} 
            icon={Layers} 
            variant="zinc"
            label="Peak Sustained Load"
          />
        </div>

        {/* Main Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8 space-y-8">
            <SpectreYield />
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
              <NodeHealth />
              <CommandCenter />
            </div>
          </div>
          
          <div className="lg:col-span-4 h-full">
            <GlobalLedger />
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="p-10 border-t border-zinc-900 flex justify-between items-center text-[10px] tracking-widest text-zinc-600 font-mono uppercase">
        <div>© 2024 Sovereign Luxe // Root Architect Interface</div>
        <div>Mirror Protocol V5.2 // Build ID: 8A2-FX9</div>
      </footer>
    </main>
  );
}
