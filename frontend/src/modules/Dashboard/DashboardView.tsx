import React from 'react';
import { MetricCard } from './components/MetricCard';
import type { QuantitativeValuationResult, QualitativeValuationResult } from '@/common/types/valuation';

interface DashboardViewProps {
  ticker: string;
  quantData?: QuantitativeValuationResult;
  qualData?: QualitativeValuationResult;
}

export function DashboardView({ ticker, quantData, qualData }: DashboardViewProps) {
  // Helper to safely extract the latest value of a metric by key
  const getLatestMetric = (metricKey: string, formatAs: 'currency' | 'number' | 'percent' = 'number') => {
    if (!quantData || !quantData.metrics) return 'N/A';
    
    // metrics is a dictionary (Record<string, MetricSeries>)
    const series = quantData.metrics[metricKey];
    
    if (!series || !series.yearly_data || series.yearly_data.length === 0) return 'N/A';
    
    // Sort by date descending and get the first one
    const latest = [...series.yearly_data].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())[0];
    const val = Number(latest.value);
    if (isNaN(val)) return 'N/A';

    if (formatAs === 'currency') {
      if (val >= 1e12) return `$${(val / 1e12).toFixed(2)}T`;
      if (val >= 1e9) return `$${(val / 1e9).toFixed(2)}B`;
      if (val >= 1e6) return `$${(val / 1e6).toFixed(2)}M`;
      return `$${val.toFixed(2)}`;
    }
    if (formatAs === 'percent') return `${val.toFixed(1)}%`;
    return val.toFixed(1) + 'x';
  };

  return (
    <div className="max-w-[1600px] mx-auto space-y-panel-gap">
      {/* Dashboard Header Section */}
      <div className="flex items-end justify-between px-2 pt-2 pb-1">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display-md text-display-md text-on-surface">{qualData?.ticker?.name || ticker} ({ticker})</h1>
            <div className="flex gap-2">
              <span className="px-2 py-0.5 rounded bg-surface-container-highest border border-outline-variant text-[10px] font-bold text-primary uppercase">Sector: {qualData?.ticker?.sector || 'Unknown'}</span>
              <span className="px-2 py-0.5 rounded bg-surface-container-highest border border-outline-variant text-[10px] font-bold text-secondary uppercase">Industry: {qualData?.ticker?.industry || 'Unknown'}</span>
            </div>
          </div>
        </div>
          <div className="text-right">
            <p className="text-[11px] font-medium text-on-surface-variant uppercase tracking-wider mb-1">
              Last Updated: {quantData?.metrics?.['year_end_price']?.yearly_data?.[0]?.date || 'N/A'}
            </p>
            <div className="flex items-end justify-end gap-2">
              <span className="font-display-lg text-display-lg font-bold text-primary-container">{getLatestMetric('year_end_price', 'currency')}</span>
              <span className="text-body-sm font-semibold text-on-surface-variant mb-1">(End of Year)</span>
            </div>
          </div>
      </div>

      {/* Section 1: Fundamental KPIs (Bento Style Metrics) */}
      <section className="grid grid-cols-1 md:grid-cols-5 gap-panel-gap">
        <MetricCard label="MARKET CAP" value={getLatestMetric('market_cap', 'currency')} icon="public" />

        <MetricCard label="P/E RATIO" value={getLatestMetric('pe_ratio', 'number')} icon="monitoring" />
        
        <MetricCard label="FCF YIELD" value={getLatestMetric('fcf_yield', 'percent')} icon="payments" />

        <MetricCard label="ROIC" value={getLatestMetric('roic', 'percent')} icon="account_balance_wallet" />
        
        <MetricCard label="DEBT-TO-EQUITY" value={getLatestMetric('debt_to_equity', 'number')} icon="balance" />
      </section>

      {/* Section 2: Business & Moat (2/3 and 1/3) */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-panel-gap">
        {/* Left: Business & MOAT */}
        <div className="lg:col-span-2 bg-surface-container-low border border-outline-variant flex flex-col">
          <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
              Business Strategy &amp; Competitive Moat
            </h3>
          </div>
          <div className="p-6 space-y-4">
            <p className="text-on-surface-variant leading-relaxed">
              {qualData?.business_description || 'Loading business description...'}
            </p>
            <div className="grid grid-cols-3 gap-4 pt-4">
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded flex flex-col h-40">
                <span className="font-label-caps text-label-caps text-primary mb-2 shrink-0">COMPETITIVE MOAT</span>
                <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
                  <p className="text-body-sm text-on-surface-variant leading-relaxed">{qualData?.competitive_advantage || 'Evaluating...'}</p>
                </div>
              </div>
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded flex flex-col h-40">
                <span className="font-label-caps text-label-caps text-secondary mb-2 shrink-0">REVENUE MODEL</span>
                <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
                  <p className="text-body-sm text-on-surface-variant leading-relaxed">{qualData?.revenue_model || 'Evaluating...'}</p>
                </div>
              </div>
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded flex flex-col h-40">
                <span className="font-label-caps text-label-caps text-tertiary mb-2 shrink-0">KEY RISKS</span>
                <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
                  <p className="text-body-sm text-on-surface-variant leading-relaxed">{qualData ? Object.keys(qualData.risk_factors).join(', ') : 'Evaluating...'}</p>
                </div>
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
              <div>
                <p className="text-on-surface font-semibold line-clamp-1">{qualData?.ceo_name || 'Unknown'}</p>
                <p className="text-on-surface-variant text-[11px] uppercase tracking-tighter">Chief Executive Officer</p>
              </div>
            </div>
            <div className="mt-4">
              <p className="text-body-sm text-on-surface-variant line-clamp-5" title={qualData?.management_insights}>{qualData?.management_insights || 'Analyzing leadership...'}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
