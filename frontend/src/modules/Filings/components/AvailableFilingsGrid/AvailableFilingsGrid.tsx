import type { LocalFilingDTO } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { formatFinancialPeriod } from '@/common/utils/formatters';

interface AvailableFilingsGridProps {
  filings: LocalFilingDTO[];
  onSelectFiling: (filing: LocalFilingDTO) => void;
  isAnalyzing: boolean;
  analyzingFilingId: string | null;
  analyzingPeriod?: string | null;
}

export function AvailableFilingsGrid({ filings, onSelectFiling, isAnalyzing, analyzingFilingId, analyzingPeriod }: AvailableFilingsGridProps) {
  const { t } = useTranslation();

  if (!filings || filings.length === 0) {
    return null;
  }

  const annualFilings = filings.filter((f) => f.form_type === '10-K');
  let quarterlyFilings = filings.filter((f) => f.form_type === '10-Q');

  quarterlyFilings = quarterlyFilings.sort((a, b) => b.period.localeCompare(a.period));

  const renderFilingButton = (filing: LocalFilingDTO) => {
    const isQuarterly = filing.form_type === '10-Q';
    const displayPeriod = formatFinancialPeriod(filing.period, isQuarterly);

    // If analyzingPeriod is provided, use it for exact matching (resolves Q4 vs FY overlap). Otherwise fallback to ID.
    const isThisAnalyzing = isAnalyzing && (analyzingPeriod ? analyzingPeriod === filing.period : analyzingFilingId === filing.id);
    return (
      <button
        key={`${filing.id}_${filing.period}`}
        onClick={() => onSelectFiling(filing)}
        disabled={isAnalyzing}
        className={`
          group relative flex items-center justify-between p-4 rounded-xl border
          transition-all duration-200 ease-out text-left
          ${isThisAnalyzing 
            ? 'bg-primary/5 border-primary/30 ring-1 ring-primary/20' 
            : 'bg-surface border-surface-border hover:bg-surface-hover hover:border-primary/30 hover:-translate-y-1 hover:shadow-lg'
          }
          ${isAnalyzing && !isThisAnalyzing ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
      >
        <div className="flex items-center gap-3">
          <div className={`
            p-2 rounded-lg flex items-center justify-center
            ${isThisAnalyzing ? 'bg-primary/20 text-primary' : 'bg-surface-border/50 text-on-surface-variant group-hover:bg-primary/10 group-hover:text-primary transition-colors'}
          `}>
            {isThisAnalyzing ? (
              <span className="material-symbols-outlined w-5 h-5 flex items-center justify-center animate-spin">
                progress_activity
              </span>
            ) : (
              <span className="material-symbols-outlined w-5 h-5 flex items-center justify-center">
                description
              </span>
            )}
          </div>
          <div>
            <h3 className="font-semibold text-on-surface leading-tight">
              {displayPeriod}
            </h3>
          </div>
        </div>
      </button>
    );
  };

  return (
    <div className="mb-10 animate-fade-in-up">
      <div className="space-y-8">
        {annualFilings.length > 0 ? (
          <div>
            <h3 className="text-sm font-bold text-primary uppercase tracking-wider mb-3">
              {t('filings.annual_filings')}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {annualFilings.map(renderFilingButton)}
            </div>
          </div>
        ) : null}

        {quarterlyFilings.length > 0 ? (
          <div>
            <h3 className="text-sm font-bold text-primary uppercase tracking-wider mb-3">
              {t('filings.quarterly_filings')}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {quarterlyFilings.map(renderFilingButton)}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
