export const formatLargeCurrency = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return '-';
  
  const val = Number(rawVal);
  let actualValue = val;
  


  const absVal = Math.abs(actualValue);
  const sign = actualValue < 0 ? '-' : '';

  if (absVal >= 1e12) return `${sign}$${(absVal / 1e12).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}T`;
  if (absVal >= 1e9) return `${sign}$${(absVal / 1e9).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}B`;
  if (absVal >= 1e6) return `${sign}$${(absVal / 1e6).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}M`;
  return `${sign}$${absVal.toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}`;
};

export const formatLargeNumber = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return '-';
  
  const val = Number(rawVal);
  let actualValue = val;


  const absVal = Math.abs(actualValue);
  const sign = actualValue < 0 ? '-' : '';

  if (absVal >= 1e12) return `${sign}${(absVal / 1e12).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}T`;
  if (absVal >= 1e9) return `${sign}${(absVal / 1e9).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}B`;
  if (absVal >= 1e6) return `${sign}${(absVal / 1e6).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}M`;
  return `${sign}${absVal.toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}`;
};

export const formatCurrency = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return '-';
  const val = Number(rawVal);
  const absVal = Math.abs(val);
  const sign = val < 0 ? '-' : '';
  
  if (absVal >= 1e12) return `${sign}$${(absVal / 1e12).toFixed(2)}T`;
  if (absVal >= 1e9) return `${sign}$${(absVal / 1e9).toFixed(2)}B`;
  if (absVal >= 1e6) return `${sign}$${(absVal / 1e6).toFixed(2)}M`;
  return `${sign}$${absVal.toFixed(2)}`;
};

export const formatStockPrice = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return '-';
  return `$${Number(rawVal).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 2 })}`;
};


export const formatPercentage = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return '-';
  return `${Number(rawVal).toFixed(1)}%`;
};

export const formatMultiplier = (rawVal?: number | string | null): string => {
  if (rawVal == null || isNaN(Number(rawVal))) return '-';
  return `${Number(rawVal).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}x`;
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

export const formatDateString = (dateStr?: string | null, language: string = 'en'): string => {
  if (!dateStr) return '';
  try {
    return new Date(dateStr).toLocaleDateString(language === 'pt' ? 'pt-PT' : 'en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      timeZone: 'UTC'
    });
  } catch (e) {
    return dateStr;
  }
};

export const formatFinancialPeriod = (period: string, isQuarterly: boolean): string => {
  if (!period) return '';
  if (period === 'TTM') return 'TTM';
  
  // Handle SEC filing formats: "2026-Q1" -> "Q1 2026"
  if (isQuarterly && period.includes('-Q')) {
    const parts = period.split('-');
    if (parts.length === 2 && parts[1].startsWith('Q')) {
      return `${parts[1]} ${parts[0]}`;
    }
  }
  
  // Handle SEC filing formats: "FY2025" -> "FY 2025"
  if (!isQuarterly && period.toUpperCase().startsWith('FY')) {
    const yearMatch = period.match(/\d{4}/);
    if (yearMatch) {
      return `FY ${yearMatch[0]}`;
    }
  }
  
  try {
    const date = new Date(period);
    const year = date.getFullYear();
    
    if (isNaN(year)) return period;
    
    if (!isQuarterly) {
      return `FY ${year}`;
    } else {
      const month = date.getMonth() + 1; // 1 to 12
      const q = Math.ceil(month / 3);
      return `Q${q} ${year}`;
    }
  } catch (e) {
    return period;
  }
};

