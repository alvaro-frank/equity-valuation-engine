import { useTranslation } from 'react-i18next';
import type { QualitativeValuationResult } from '@/common/types/valuation';
import { HistoryCard } from './components/HistoryCard';

interface HistoryTabProps {
  qualData: QualitativeValuationResult;
}

export function HistoryTab({ qualData }: HistoryTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <HistoryCard 
          icon="history_edu" 
          iconColor="text-primary" 
          title={t('thesis_view.history_title')} 
          content={qualData.company_history || t('thesis_view.no_data')} 
        />
        <HistoryCard 
          icon="tsunami" 
          iconColor="text-error" 
          title={t('thesis_view.crises_title')} 
          content={qualData.historical_context_crises} 
        />
      </div>
    </div>
  );
}
