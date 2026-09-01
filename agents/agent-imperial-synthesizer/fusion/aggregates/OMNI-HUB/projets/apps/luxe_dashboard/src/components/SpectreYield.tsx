"use client";
import React from "react";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  ComposedChart, Line, Bar 
} from "recharts";

const data = [
  { time: "00:00", yield: 4.2, target: 4.0, nodeLoad: 2400 },
  { time: "04:00", yield: 4.8, target: 4.1, nodeLoad: 3200 },
  { time: "08:00", yield: 5.1, target: 4.2, nodeLoad: 4100 },
  { time: "12:00", yield: 4.7, target: 4.3, nodeLoad: 3800 },
  { time: "16:00", yield: 5.9, target: 4.4, nodeLoad: 5200 },
  { time: "20:00", yield: 6.4, target: 4.5, nodeLoad: 6100 },
  { time: "23:59", yield: 6.8, target: 4.6, nodeLoad: 6800 },
];

export const SpectreYield = () => {
  return (
    <div className="glass-morphism p-8 rounded-none border-zinc-900/50 h-full">
      <div className="flex justify-between items-end mb-10">
        <div>
          <h2 className="text-xl font-light tracking-[0.2em] uppercase text-white mb-1">
            SPECTRE_YIELD Analysis
          </h2>
          <p className="text-[10px] tracking-widest text-zinc-500 font-mono uppercase">
            Predictive vs. Actual Performance
          </p>
        </div>
      </div>

      <div className="h-[400px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data}>
            <defs>
              <linearGradient id="yieldGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#D4AF37" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#D4AF37" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#18181B" vertical={false} />
            <XAxis 
              dataKey="time" 
              stroke="#52525B" 
              fontSize={10} 
              tickLine={false} 
              axisLine={false}
              tick={{ fill: '#52525B' }}
            />
            <YAxis 
              stroke="#52525B" 
              fontSize={10} 
              tickLine={false} 
              axisLine={false}
              tick={{ fill: '#52525B' }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#09090B', 
                border: '1px solid #18181B',
                fontSize: '10px',
                fontFamily: 'monospace',
                color: '#D4AF37'
              }}
              itemStyle={{ color: '#D4AF37' }}
            />
            <Area 
              type="monotone" 
              dataKey="yield" 
              stroke="#D4AF37" 
              fillOpacity={1} 
              fill="url(#yieldGradient)" 
              strokeWidth={2}
            />
            <Line 
              type="monotone" 
              dataKey="target" 
              stroke="#52525B" 
              strokeDasharray="5 5" 
              dot={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
