import { useTranslation } from 'react-i18next';
import { FilingsHeaderSkeleton } from './components/FilingsHeaderSkeleton';
import { FilingsGridSkeleton } from './components/FilingsGridSkeleton';
import { FilingsUploadSkeleton } from './components/FilingsUploadSkeleton';

export function FilingsSkeleton() {
  const { i18n } = useTranslation();
  
  return (
    <div className="w-full flex-1 flex flex-col max-w-[1600px] mx-auto animate-in fade-in duration-500">
      <FilingsHeaderSkeleton />
      
      <FilingsGridSkeleton />

      <hr className="border-t border-outline-variant my-10" />

      <FilingsUploadSkeleton />

      {/* Floating Toast Notification for SEC Filings Check */}
      <div className="fixed bottom-6 right-6 z-50 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
        <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
        <span className="text-on-surface font-medium text-sm animate-pulse">
          {i18n.language === 'pt' ? 'A verificar Documentos SEC...' : 'Verifying SEC Filings...'}
        </span>
      </div>
    </div>
  );
}
