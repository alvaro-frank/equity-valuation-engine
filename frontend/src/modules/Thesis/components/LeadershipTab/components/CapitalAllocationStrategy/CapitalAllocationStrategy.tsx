import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

interface CapitalAllocationStrategyProps {
  content?: string;
}

export function CapitalAllocationStrategy({ content }: CapitalAllocationStrategyProps) {
  const { t } = useTranslation();

  if (!content) return null;

  return (
    <div className="flex flex-col rounded-2xl border border-outline-variant/50 bg-surface/30 p-6 backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-4">
        <span className="material-symbols-outlined text-primary text-xl">account_balance</span>
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
          {t('thesis_view.capital_allocation_title', 'Capital Allocation Strategy')}
        </h3>
      </div>
      
      <div className="text-body-md text-on-surface-variant leading-relaxed whitespace-pre-wrap">
        <CitedText text={content} />
      </div>
    </div>
  );
}
