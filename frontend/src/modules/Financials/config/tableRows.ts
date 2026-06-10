import type { FinancialTableRow } from '../components/FinancialTable';

export const INCOME_STATEMENT_ROWS: FinancialTableRow[] = [
  { key: 'revenue', labelKey: 'financials.metrics.revenue', formatAs: 'currency' },
  { key: 'gross_profit', labelKey: 'financials.metrics.gross_profit', formatAs: 'currency' },
  { key: 'gross_margin', labelKey: 'financials.metrics.gross_margin', formatAs: 'percent' },
  { key: 'ebitda', labelKey: 'financials.metrics.ebitda', formatAs: 'currency' },
  { key: 'operating_income', labelKey: 'financials.metrics.operating_income', formatAs: 'currency' },
  { key: 'operating_margin', labelKey: 'financials.metrics.operating_margin', formatAs: 'percent' },
  { key: 'net_income', labelKey: 'financials.metrics.net_income', formatAs: 'currency' },
  { key: 'net_margin', labelKey: 'financials.metrics.net_margin', formatAs: 'percent' },
  { key: 'shares_outstanding', labelKey: 'financials.metrics.shares_outstanding', formatAs: 'number' },
  { key: 'eps', labelKey: 'financials.metrics.eps', formatAs: 'small_currency' },
];

export const BALANCE_SHEET_ROWS: FinancialTableRow[] = [
  { key: 'cash_and_equivalents', labelKey: 'financials.metrics.cash_and_equivalents', formatAs: 'currency' },
  { key: 'accounts_receivable', labelKey: 'financials.metrics.accounts_receivable', formatAs: 'currency' },
  { key: 'inventory', labelKey: 'financials.metrics.inventory', formatAs: 'currency' },
  { key: 'current_assets', labelKey: 'financials.metrics.current_assets', formatAs: 'currency' },
  { key: 'net_ppe', labelKey: 'financials.metrics.net_ppe', formatAs: 'currency' },
  { key: 'intangible_assets', labelKey: 'financials.metrics.intangible_assets', formatAs: 'currency' },
  { key: 'total_assets', labelKey: 'financials.metrics.total_assets', formatAs: 'currency' },
  { key: 'accounts_payable', labelKey: 'financials.metrics.accounts_payable', formatAs: 'currency' },
  { key: 'short_term_debt', labelKey: 'financials.metrics.short_term_debt', formatAs: 'currency' },
  { key: 'current_liabilities', labelKey: 'financials.metrics.current_liabilities', formatAs: 'currency' },
  { key: 'long_term_debt', labelKey: 'financials.metrics.long_term_debt', formatAs: 'currency' },
  { key: 'total_debt', labelKey: 'financials.metrics.total_debt', formatAs: 'currency' },
  { key: 'total_liabilities', labelKey: 'financials.metrics.total_liabilities', formatAs: 'currency' },
  { key: 'total_equity', labelKey: 'financials.metrics.total_equity', formatAs: 'currency' },
];

export const CASH_FLOW_ROWS: FinancialTableRow[] = [
  { key: 'operating_cash_flow', labelKey: 'financials.metrics.operating_cash_flow', formatAs: 'currency' },
  { key: 'capital_expenditures', labelKey: 'financials.metrics.capital_expenditures', formatAs: 'currency' },
  { key: 'free_cash_flow', labelKey: 'financials.metrics.free_cash_flow', formatAs: 'currency' },
];

export const RATIOS_ROWS: FinancialTableRow[] = [
  { key: 'roe', labelKey: 'financials.metrics.roe', formatAs: 'percent' },
  { key: 'roic', labelKey: 'financials.metrics.roic', formatAs: 'percent' },
  { key: 'debt_to_equity', labelKey: 'financials.metrics.debt_to_equity', formatAs: 'multiplier' },
  { key: 'pe_ratio', labelKey: 'financials.metrics.pe_ratio', formatAs: 'multiplier' },
  { key: 'pb_ratio', labelKey: 'financials.metrics.pb_ratio', formatAs: 'multiplier' },
  { key: 'ps_ratio', labelKey: 'financials.metrics.ps_ratio', formatAs: 'multiplier' },
  { key: 'fcf_yield', labelKey: 'financials.metrics.fcf_yield', formatAs: 'percent' },
];
