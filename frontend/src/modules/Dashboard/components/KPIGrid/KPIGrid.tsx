import { MetricCard } from '../MetricCard';
import { formatLargeCurrency, formatLargeNumber } from '@/common/utils/formatters';
import type { QuantitativeValuationResult } from '@/common/types/valuation';

interface KPIGridProps {
  quantData?: QuantitativeValuationResult;
  ev: number | null;
  fcf: number | null;
  getLatestMetric: (metricKey: string, formatAs?: 'currency' | 'number' | 'percent') => string;
  getRawLatestMetric: (metricKey: string) => number | null;
}

export function KPIGrid({ quantData, ev, fcf, getLatestMetric, getRawLatestMetric }: KPIGridProps) {
  return (
    <section className="grid grid-cols-1 md:grid-cols-5 gap-panel-gap">
      <MetricCard 
        label="MARKET CAP" 
        value={formatLargeCurrency(quantData?.ticker?.market_cap)} 
        icon="public"
        flipData={{
          label: "ENTERPRISE VALUE",
          value: formatLargeCurrency(ev ?? undefined)
        }}
      />

      <MetricCard 
        label="P/E RATIO TTM" 
        value={formatLargeNumber(quantData?.ticker?.pe_ratio)} 
        icon="monitoring" 
        flipData={{
          label: "FORWARD P/E",
          value: formatLargeNumber(quantData?.ticker?.forward_pe)
        }}
      />
      
      <MetricCard 
        label="FREE CASH FLOW" 
        value={formatLargeCurrency(fcf ?? undefined)} 
        icon="payments" 
        flipData={{
          label: "FCF YIELD TTM",
          value: getLatestMetric('fcf_yield', 'percent')
        }}
      />

      <MetricCard 
        label="ROIC" 
        value={getLatestMetric('roic', 'percent')} 
        icon="account_balance_wallet" 
        flipData={{
          label: "ROE",
          value: getLatestMetric('roe', 'percent')
        }}
      />
      
      <MetricCard 
        label="DEBT-TO-EQUITY" 
        value={getLatestMetric('debt_to_equity', 'number')} 
        icon="balance" 
        flipData={{
          label: "CASH & EQUIVALENTS",
          value: formatLargeCurrency(getRawLatestMetric('cash_and_equivalents') ?? undefined)
        }}
      />
    </section>
  );
}
