export interface BaseMetric {
  date: string;
  value: number;
  yoy_growth?: number;
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

export interface LiveQuoteResult {
  amount: number;
  currency: string;
  change?: number;
  change_percent?: number;
  is_live_supported: boolean;
}

export interface QuantitativeValuationResult {
  ticker: TickerResult;
  metrics: Record<string, MetricSeries>;
  quarterly_metrics?: Record<string, BaseMetric[]>;
}

export interface LocalFilingDTO {
  id: string;
  form_type: string;
  period: string;
  accession_number: string;
  focus_period?: string;
}

export interface LocalFilingListResult {
  filings: LocalFilingDTO[];
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

export interface CompetitorData {
  name: string;
  ticker: string;
  overlap: string;
}

export interface SourceInfo {
  source_name: string;
  exact_quote: string;
}

export interface QualitativeValuationResult {
  ticker: TickerResult;
  company_name: string;
  business_description: string;
  company_history: string;
  key_executives: Array<{name: string; title: string; ownership: number | null}>;
  major_shareholders: Record<string, number>;
  revenue_model: string;
  strategy: string;
  products_services: Record<string, string>;
  competitive_advantage: string;
  competitors: CompetitorData[];
  management_insights: string;
  capital_allocation_strategy?: string;
  near_term_catalysts?: Array<{event: string; impact: string}>;
  risk_factors: Record<string, string>;
  historical_context_crises: string;
  moat_trajectory_status?: string;
  moat_trajectory_description?: string;
  moat_sources?: MoatSources;
  quality_pillars?: QualityPillars;
  forward_guidance?: string;
  bottom_line?: string;
  sources?: Record<string, SourceInfo>;
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
  sources?: Record<string, SourceInfo>;
}

export interface MetricWithGrowth {
  amount: number | null;
  yoy_growth?: number | null;
}

export interface CorePerformance {
  revenue: MetricWithGrowth;
  eps: MetricWithGrowth;
  gross_margin: MetricWithGrowth;
  operating_margin: MetricWithGrowth;
  net_margin: MetricWithGrowth;
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
    sector?: string;
    industry?: string;
  };
  period_end_date: string;
  core_performance: CorePerformance;
  capital_allocation: CapitalAllocation;
  forward_guidance: string;
  moat_trajectory_status: string;
  moat_trajectory_description: string;
  risk_deconstruction: RiskDeconstruction;
  bottom_line: string;
  sources: Record<string, SourceInfo>;
  transcript?: TranscriptStatement[];
}

export interface TranscriptStatement {
  speaker: string;
  title: string;
  content: string;
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

export interface DCFAssumptions {
  fcf_growth_1_to_5: number;
  fcf_growth_6_to_10: number;
  wacc: number;
  terminal_growth_rate: number;
  justification: string;
}

export interface DCFScenario {
  scenario_name: string;
  assumptions: DCFAssumptions;
  base_fcf: number;
  shares_outstanding: number;
  net_cash: number;
  projected_fcfs: number[];
  terminal_value: number;
  intrinsic_value_per_share: number;
}

export interface DCFScenarios {
  bear: DCFScenario;
  fair: DCFScenario;
  bull: DCFScenario;
  custom?: DCFScenario; // Custom is local to the frontend
}

export interface DCFValuationResult {
  base_fcf_ttm: number;
  shares_outstanding: number;
  net_cash: number;
  scenarios: DCFScenarios;
}
