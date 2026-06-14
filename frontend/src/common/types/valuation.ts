export interface BaseMetric {
  date: string;
  value: number;
}

export interface CAGRData {
  value: number;
  years: number;
}

export interface MetricSeries {
  metric_name: string;
  yearly_data: BaseMetric[];
  cagr?: number | null;
}

export interface TickerResult {
  symbol: string;
  name: string;
  sector: string;
  sector_key?: string;

  industry: string;
  industry_key?: string;
  market_cap?: number;
  pe_ratio?: number;
  forward_pe?: number;
  current_price?: number;
  regular_market_change?: number;
  regular_market_change_percent?: number;
}

export interface QuantitativeValuationResult {
  ticker: TickerResult;
  metrics: Record<string, MetricSeries>;
  quarterly_metrics?: Record<string, BaseMetric[]>;
}

export interface MoatSources {
  intangible_assets: number;
  switching_costs: number;
  network_effect: number;
  cost_advantage: number;
  efficient_scale: number;
}

export interface QualityPillars {
  management_quality: number;
  business_model_resilience: number;
  pricing_power: number;
  innovation_and_growth: number;
  tam_expansion: number;
}

export interface QualitativeValuationResult {
  ticker: TickerResult;
  business_description: string;
  company_history: string;
  key_executives: Array<{name: string; title: string; ownership: number | null}>;
  major_shareholders: Record<string, number>;
  revenue_model: string;
  strategy: string;
  products_services: Record<string, string>;
  competitive_advantage: string;
  competitors: Record<string, string>;
  management_insights: string;
  risk_factors: Record<string, string>;
  historical_context_crises: string;
  moat_trajectory?: string;
  moat_sources?: MoatSources;
  quality_pillars?: QualityPillars;
  forward_guidance?: string;
  bottom_line?: string;
}

export interface SectorIndustrialValuationResult {
  ticker: TickerResult;
  sector: string;
  industry: string;
  rivalry_among_competitors: Record<string, string>;
  bargaining_power_of_suppliers: Record<string, string>;
  bargaining_power_of_customers: Record<string, string>;
  threat_of_new_entrants: Record<string, string>;
  threat_of_obsolescence: Record<string, string>;
  economic_sensitivity: string;
  interest_rate_exposure: string;
}

export interface MetricWithGrowth {
  amount: number | null;
  yoy_growth: number | null;
}

export interface CorePerformance {
  adjusted_revenue: MetricWithGrowth;
  adjusted_eps: MetricWithGrowth;
  adjusted_gross_margin: MetricWithGrowth;
  adjusted_operating_margin: MetricWithGrowth;
  adjusted_net_margin: MetricWithGrowth;
  free_cash_flow: MetricWithGrowth;
}

export interface CapitalAllocation {
  share_buybacks: number;
  dividends: number;
  capex_rd: number;
  infrastructure_assessment: string;
}

export interface RiskDeconstruction {
  macro_risks: string[];
  internal_risks: string[];
}

export interface EarningsReportResult {
  ticker: {
    symbol: string;
    name?: string;
  };
  period_end_date: string;
  core_performance: CorePerformance;
  capital_allocation: CapitalAllocation;
  forward_guidance: string;
  moat_trajectory: string;
  risk_deconstruction: RiskDeconstruction;
  bottom_line: string;
}

export interface SectorPerformancePoint {
  date: string;
  [key: string]: string | number; // Support dynamic ETF ticker and SPY keys
}

export interface SectorPerformanceData {
  company_ticker: string;
  sector: string;
  industry: string;
  sector_etf: string;
  industry_etf?: string;
  benchmark_ticker: string;
  chart_data: Array<Record<string, number | string>>;
}
