import React from 'react';
import { MetricCard } from './components/MetricCard';

export function Dashboard() {
  return (
    <div className="max-w-[1600px] mx-auto space-y-panel-gap">
      {/* Dashboard Header Section */}
      <div className="flex items-end justify-between px-2 pt-2 pb-1">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display-md text-display-md text-on-surface">Microsoft Corporation (MSFT)</h1>
            <div className="flex gap-2">
              <span className="px-2 py-0.5 rounded bg-surface-container-highest border border-outline-variant text-[10px] font-bold text-primary uppercase">Sector: Technology</span>
              <span className="px-2 py-0.5 rounded bg-surface-container-highest border border-outline-variant text-[10px] font-bold text-secondary uppercase">Industry: Software</span>
            </div>
          </div>
        </div>
        <div className="text-right">
          <p className="text-data-mono text-body-sm text-on-surface-variant">Last Updated: Jun 14, 2024</p>
          <p className="text-data-mono text-display-md text-primary">
            $442.57 <span className="text-body-sm font-semibold text-[#4ade80]">+1.24%</span>
          </p>
        </div>
      </div>

      {/* Section 1: Fundamental KPIs (Bento Style Metrics) */}
      <section className="grid grid-cols-1 md:grid-cols-5 gap-panel-gap">
        <MetricCard label="MARKET CAP" value="$3.1T" icon="public">
          <div className="h-1 w-full bg-surface-container-highest mt-2 rounded-full overflow-hidden">
            <div className="h-full bg-primary w-[85%]"></div>
          </div>
        </MetricCard>

        <MetricCard label="P/E RATIO" value="35.2x" icon="monitoring" subValue="S&P 500 Avg: 22.4x" />
        
        <MetricCard label="FCF YIELD" value="2.8%" icon="payments">
          <div className="flex items-center gap-1 mt-1">
            <span className="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span className="text-[10px] text-on-surface-variant">Steady Cash Engine</span>
          </div>
        </MetricCard>

        <MetricCard label="ROIC" value="32.5%" icon="account_balance_wallet" subValue="Industry Top Decile" subValueColor="text-[#4ade80]" />
        
        <MetricCard label="DEBT-TO-EQUITY" value="0.45" icon="balance" subValue="Investment Grade: AAA" />
      </section>

      {/* Section 2: Business & Moat (2/3 and 1/3) */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-panel-gap">
        {/* Left: Business & MOAT */}
        <div className="lg:col-span-2 bg-surface-container-low border border-outline-variant flex flex-col">
          <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-primary">security</span>
              Business Strategy &amp; Competitive Moat
            </h3>
          </div>
          <div className="p-6 space-y-4">
            <p className="text-on-surface-variant leading-relaxed">
              Microsoft holds an unparalleled dominance across the technology stack. At its core, <span className="text-primary font-semibold">Azure</span> has emerged as the premier cloud backbone for enterprise digital transformation...
            </p>
            <div className="grid grid-cols-3 gap-4 pt-4">
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded">
                <span className="font-label-caps text-label-caps text-primary">SCALE MOAT</span>
                <p className="text-body-sm mt-1">Infrastructure density provides cost advantage in LLM training.</p>
              </div>
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded">
                <span className="font-label-caps text-label-caps text-secondary">NETWORK MOAT</span>
                <p className="text-body-sm mt-1">Teams and LinkedIn benefit from exponential user connectivity.</p>
              </div>
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded">
                <span className="font-label-caps text-label-caps text-tertiary">SWITCHING MOAT</span>
                <p className="text-body-sm mt-1">Windows/Server ecosystems remain deeply embedded in IT.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Leadership & Macro */}
        <div className="bg-surface-container-low border border-outline-variant flex flex-col">
          <div className="px-4 py-3 border-b border-outline-variant">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">Leadership &amp; Macro</h3>
          </div>
          <div className="p-4 flex-1 space-y-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-primary/20">
                <img alt="Satya Nadella" src="https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcR19qG-z9Fn9RwoXZYY8jKvgCvDGajDrBK9pc-8vAswRYNSJcong0hpE5P7Jf118mPEY5crxPigIGeDIqQ" />
              </div>
              <div>
                <p className="text-on-surface font-semibold">Satya Nadella</p>
                <p className="text-on-surface-variant text-[11px] uppercase tracking-tighter">Chief Executive Officer</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
