import { api } from '@/common/utils/api';
import type {
  QuantitativeValuationResult,
  QualitativeValuationResult,
  SectorIndustrialValuationResult,
  EarningsReportResult,
} from '@/common/types/valuation';

export const ValuationApi = {
  getQuantitative: async (ticker: string, years: number = 10): Promise<QuantitativeValuationResult> => {
    const response = await api.get(`/valuation/quantitative/${ticker}`, {
      params: { years },
    });
    return response.data;
  },

  getQualitative: async (ticker: string): Promise<QualitativeValuationResult> => {
    const response = await api.get(`/valuation/qualitative/${ticker}`);
    return response.data;
  },

  getSector: async (ticker: string): Promise<SectorIndustrialValuationResult> => {
    const response = await api.get(`/valuation/sector/${ticker}`);
    return response.data;
  },

  uploadEarningsReport: async (ticker: string, file: File): Promise<EarningsReportResult> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/valuation/earnings/${ticker}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
