import { api } from '@/common/utils/api';
import type {
  QuantitativeValuationResult,
  QualitativeValuationResult,
  SectorIndustrialValuationResult,
  EarningsReportResult,
} from '@/common/types/valuation';
import i18n from '@/common/i18n/i18n';

export const ValuationApi = {
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

  uploadEarningsReport: async (ticker: string, file: File): Promise<EarningsReportResult> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/valuation/earnings/${ticker}`, formData, {
      params: { lang: i18n.language },
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
