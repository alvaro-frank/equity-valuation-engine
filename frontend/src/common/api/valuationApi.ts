import { api } from '@/common/utils/api';
import type {
  QuantitativeValuationResult,
  QualitativeValuationResult,
  SectorIndustrialValuationResult,
  SectorPerformanceData,
  DCFValuationResult,
} from '@/common/types/valuation';
import i18n from '@/common/i18n/i18n';

export const ValuationApi = {
  validateTicker: async (ticker: string): Promise<{ valid: boolean }> => {
    const response = await api.get(`/valuation/validate/${ticker}`);
    return response.data;
  },

  getQuantitative: async (ticker: string, years: number = 10): Promise<QuantitativeValuationResult> => {
    const response = await api.get(`/valuation/quantitative/${ticker}`, {
      params: { years },
    });
    return response.data;
  },

  getQualitative: async (ticker: string): Promise<QualitativeValuationResult> => {
    const response = await api.get(`/valuation/qualitative/${ticker}`, {
      params: { lang: i18n.language }
    });
    return response.data;
  },

  getSector: async (ticker: string): Promise<SectorIndustrialValuationResult> => {
    const response = await api.get(`/valuation/sector/${ticker}`, {
      params: { lang: i18n.language }
    });
    return response.data;
  },

  getSectorPerformance: async (ticker: string): Promise<SectorPerformanceData> => {
    const response = await api.get(`/valuation/sector-performance/${ticker}`);
    return response.data;
  },

  getDcf: async (ticker: string): Promise<DCFValuationResult> => {
    const response = await api.get(`/valuation/dcf/${ticker}`, {
      params: { lang: i18n.language }
    });
    return response.data;
  },

};
