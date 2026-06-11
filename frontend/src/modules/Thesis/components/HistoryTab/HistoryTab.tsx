import { useTranslation } from 'react-i18next';

// --- Sub-Components (Rule 2.21, 2.41) ---

interface HistoryCardProps {
  icon: string;
  iconColor: string;
  title: string;
  content: string;
}

function HistoryCard({ icon, iconColor, title, content }: HistoryCardProps) {
  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className={`material-symbols-outlined ${iconColor}`}>{icon}</span>
        {title}
      </h3>
      <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 h-[calc(100%-40px)]">
        <p>{content}</p>
      </div>
    </div>
  );
}

// --- Main Component ---

import type { QualitativeValuationResult } from '@/common/types/valuation';

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
