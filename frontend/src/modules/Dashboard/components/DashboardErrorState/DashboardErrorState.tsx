import { useTranslation } from 'react-i18next';

export interface DashboardErrorDetails {
  key: number | string;
  details: {
    title: string;
    message: string;
    icon: string;
  };
  rawMessage?: string;
  ticker?: string;
}

interface DashboardErrorStateProps {
  errorState: DashboardErrorDetails;
  onRetry: () => void;
}

export function DashboardErrorState({ errorState, onRetry }: DashboardErrorStateProps) {
  const { t } = useTranslation();
  const { key, details, rawMessage, ticker } = errorState;

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 animate-in fade-in duration-500">
      <div className="w-20 h-20 bg-error/10 border border-error/20 rounded-full flex items-center justify-center mb-6">
        <span className="material-symbols-outlined text-[40px] text-error">{details.icon}</span>
      </div>
      <h2 className="font-display-sm text-display-sm font-bold text-on-surface mb-2">
        {key === 'DEFAULT' ? `${details.title} ${ticker || ''}` : details.title}
      </h2>
      <p className="text-body-md text-on-surface-variant max-w-md mb-8 leading-relaxed">
        {key === 'DEFAULT' && rawMessage ? rawMessage : details.message}
      </p>
      <button 
        onClick={onRetry}
        className="flex items-center gap-2 px-6 py-2.5 bg-surface-container-highest border border-outline-variant hover:border-outline text-on-surface rounded-full transition-all duration-200 font-label-lg font-medium hover:bg-surface-container-high active:scale-95"
      >
        <span className="material-symbols-outlined text-[18px]">refresh</span>
        {t('dashboard.try_again')}
      </button>
    </div>
  );
}
