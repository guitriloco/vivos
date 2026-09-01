"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Terminal, ShieldAlert, Cpu, Database, Send } from "lucide-react";

export const CommandCenter = () => {
  const [logs, setLogs] = useState<string[]>([
    "AUTHENTICATION_SUCCESSFUL",
    "MIRROR_PROTOCOL_STABLE",
    "READY_FOR_DIRECTIVES"
  ]);

  const executeDirective = (directive: string) => {
    setLogs(prev => [...prev.slice(-10), `> EXECUTING_${directive}...`, `[SUCCESS] ${directive}_COMPLETE`]);
  };

  return (
    <div className="glass-morphism p-8 rounded-none border-zinc-900/50 relative overflow-hidden h-full">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h2 className="text-xl font-light tracking-[0.2em] uppercase text-white mb-1">
            Architect Command Center
          </h2>
          <p className="text-[10px] tracking-widest text-zinc-500 font-mono uppercase">
            Directive Issuance Interface
          </p>
        </div>
        <ShieldAlert className="w-5 h-5 text-luxe-gold animate-pulse" />
      </div>

      <div className="grid grid-cols-2 gap-4 mb-8">
        <button 
          onClick={() => executeDirective('ACTIVATE_SPECTRE')}
          className="p-4 bg-zinc-900 border border-luxe-gold/30 hover:bg-luxe-gold/10 hover:border-luxe-gold text-luxe-gold text-[10px] font-mono tracking-widest uppercase transition-all flex items-center justify-center space-x-3"
        >
          <Cpu className="w-4 h-4" />
          <span>Activate Spectre</span>
        </button>
        <button 
          onClick={() => executeDirective('SYNC_ALL_NODES')}
          className="p-4 bg-zinc-900 border border-zinc-800 hover:bg-white/5 hover:border-white text-white text-[10px] font-mono tracking-widest uppercase transition-all flex items-center justify-center space-x-3"
        >
          <Database className="w-4 h-4" />
          <span>Sync All Nodes</span>
        </button>
        <button 
          onClick={() => executeDirective('EXECUTE_PURGE')}
          className="p-4 bg-zinc-900 border border-luxe-ruby/30 hover:bg-luxe-ruby/10 hover:border-luxe-ruby text-luxe-ruby text-[10px] font-mono tracking-widest uppercase transition-all flex items-center justify-center space-x-3"
        >
          <ShieldAlert className="w-4 h-4" />
          <span>Execute Purge</span>
        </button>
        <button 
          onClick={() => executeDirective('REBOOT_INTERFACE')}
          className="p-4 bg-zinc-900 border border-zinc-800 hover:bg-white/5 hover:border-white text-white text-[10px] font-mono tracking-widest uppercase transition-all flex items-center justify-center space-x-3"
        >
          <Terminal className="w-4 h-4" />
          <span>Reboot Interface</span>
        </button>
      </div>

      <div className="bg-black/80 border border-zinc-900 p-6 font-mono text-[10px] h-[180px] overflow-y-auto space-y-2">
        {logs.map((log, i) => (
          <div key={i} className={log.startsWith('[SUCCESS]') ? 'text-luxe-emerald' : log.startsWith('>') ? 'text-luxe-gold' : 'text-zinc-500'}>
            <span className="opacity-30 mr-2">[{new Date().toLocaleTimeString()}]</span>
            {log}
          </div>
        ))}
      </div>
    </div>
  );
};
