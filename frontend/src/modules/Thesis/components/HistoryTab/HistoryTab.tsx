import { useTranslation } from 'react-i18next';

interface HistoryTabProps {
  qualData: any;
}

export function HistoryTab({ qualData }: HistoryTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary">history_edu</span>
            {t('thesis_view.history_title')}
          </h3>
          <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 h-[calc(100%-40px)]">
            <p>{qualData.company_history || t('thesis_view.no_data')}</p>
          </div>
        </div>

        <div>
          <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
            <span className="material-symbols-outlined text-error">tsunami</span>
            {t('thesis_view.crises_title')}
          </h3>
          <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 h-[calc(100%-40px)]">
            <p>{qualData.historical_context_crises}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
