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

export interface QuantitativeValuationResult {
  ticker: {
    symbol: string;
    name?: string;
    sector?: string;
    industry?: string;
    market_cap?: number;
    pe_ratio?: number;
    forward_pe?: number;
    current_price?: number;
  };
  metrics: Record<string, MetricSeries>;
}

export interface QualitativeValuationResult {
  ticker: {
    symbol: string;
    name: string;
    sector?: string;
    industry?: string;
  };
  business_description: string;
  company_history: string;
  ceo_name: string;
  ceo_ownership: number;
  major_shareholders: Record<string, number>;
  revenue_model: string;
  strategy: string;
  products_services: Record<string, string>;
  competitive_advantage: string;
  competitors: Record<string, string>;
  management_insights: string;
  risk_factors: Record<string, string>;
  historical_context_crises: string;
}

export interface SectorIndustrialValuationResult {
  ticker: {
    symbol: string;
    name: string;
  };
  sector_overview: string;
  industry_overview: string;
  porters_five_forces: {
    threat_of_new_entrants: string;
    bargaining_power_of_suppliers: string;
    bargaining_power_of_buyers: string;
    threat_of_substitutes: string;
    industry_rivalry: string;
  };
  regulatory_environment: string;
  technological_disruption: string;
}

export interface EarningsReportResult {
  ticker: {
    symbol: string;
    name?: string;
  };
  period: string;
  core_performance: string;
  capital_allocation: string;
  risk_deconstruction: string;
  forward_guidance: string;
}
