export const formatLargeCurrency = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return 'N/A';
  
  const val = Number(rawVal);
  let actualValue = val;
  
  // Auto-detect if value is likely in raw dollars or already scaled.
  // We assume if it's less than 1,000,000, it's probably already scaled down to Millions by some LLM output.
  // But for raw quant data from yfinance, it's usually raw numbers (e.g. 198270000000.0)
  // We'll trust the raw number first. If it's suspiciously small for a company (e.g. < 1000) we can scale it.
  if (Math.abs(val) > 0 && Math.abs(val) < 1000) {
    actualValue = val * 1e9; // Treat as Billions
  } else if (Math.abs(val) >= 1000 && Math.abs(val) < 1000000) {
    actualValue = val * 1e6; // Treat as Millions
  }

  const absVal = Math.abs(actualValue);
  const sign = actualValue < 0 ? '-' : '';

  if (absVal >= 1e12) return `${sign}$${(absVal / 1e12).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}T`;
  if (absVal >= 1e9) return `${sign}$${(absVal / 1e9).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}B`;
  if (absVal >= 1e6) return `${sign}$${(absVal / 1e6).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}M`;
  return `${sign}$${absVal.toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}`;
};

export const formatLargeNumber = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return 'N/A';
  
  const val = Number(rawVal);
  let actualValue = val;
  
  if (Math.abs(val) > 0 && Math.abs(val) < 1000) {
    actualValue = val * 1e9; // Treat as Billions
  } else if (Math.abs(val) >= 1000 && Math.abs(val) < 1000000) {
    actualValue = val * 1e6; // Treat as Millions
  }

  const absVal = Math.abs(actualValue);
  const sign = actualValue < 0 ? '-' : '';

  if (absVal >= 1e12) return `${sign}${(absVal / 1e12).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}T`;
  if (absVal >= 1e9) return `${sign}${(absVal / 1e9).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}B`;
  if (absVal >= 1e6) return `${sign}${(absVal / 1e6).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}M`;
  return `${sign}${absVal.toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}`;
};

export const formatCurrency = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return 'N/A';
  const val = Number(rawVal);
  const absVal = Math.abs(val);
  const sign = val < 0 ? '-' : '';
  
  if (absVal >= 1e12) return `${sign}$${(absVal / 1e12).toFixed(2)}T`;
  if (absVal >= 1e9) return `${sign}$${(absVal / 1e9).toFixed(2)}B`;
  if (absVal >= 1e6) return `${sign}$${(absVal / 1e6).toFixed(2)}M`;
  return `${sign}$${absVal.toFixed(2)}`;
};

export const formatStockPrice = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return 'N/A';
  return `$${Number(rawVal).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 2 })}`;
};


export const formatPercentage = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return 'N/A';
  return `${Number(rawVal).toFixed(1)}%`;
};

export const formatMultiplier = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return 'N/A';
  return `${Number(rawVal).toFixed(1)}x`;
};

export type FormatType = 'currency' | 'small_currency' | 'percent' | 'multiplier' | 'raw' | 'number';

export const formatFinancialMetric = (val: number | null | undefined, formatAs?: FormatType): string => {
  if (val == null) return '-';
  switch (formatAs) {
    case 'currency': return formatLargeCurrency(val);
    case 'small_currency': return `$${val.toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 2 })}`;
    case 'number': return formatLargeNumber(val);
    case 'percent': return formatPercentage(val);
    case 'multiplier': return formatMultiplier(val);
    default: return val.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }
};
