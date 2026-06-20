import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

interface RevenueColumnProps {
  revenueText?: string;
}

export function RevenueColumn({ revenueText }: RevenueColumnProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded-lg flex flex-col h-48">
      <span className="font-label-caps text-label-caps text-secondary mb-2 shrink-0">{t('company_profile.revenue_model')}</span>
      <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
        <p className="text-body-sm text-on-surface-variant leading-relaxed">
          {revenueText ? <CitedText text={revenueText} /> : 'Evaluating...'}
        </p>
      </div>
    </div>
  );
}
