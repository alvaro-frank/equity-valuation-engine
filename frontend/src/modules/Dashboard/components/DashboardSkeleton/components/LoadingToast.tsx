import { useTranslation } from 'react-i18next';

export function LoadingToast() {
  const { t } = useTranslation();
  return (
    <div className="fixed bottom-6 right-6 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
      <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
      <span className="text-on-surface font-medium text-sm animate-pulse">
        {t('dashboard.loading_filings')}
      </span>
    </div>
  );
}
