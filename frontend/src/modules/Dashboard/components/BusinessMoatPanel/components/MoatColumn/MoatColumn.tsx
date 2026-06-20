import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

interface MoatColumnProps {
  moatText?: string;
}

export function MoatColumn({ moatText }: MoatColumnProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded-lg flex flex-col h-48">
      <span className="font-label-caps text-label-caps text-primary mb-2 shrink-0">{t('company_profile.moat')}</span>
      <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
        <p className="text-body-sm text-on-surface-variant leading-relaxed">
          {moatText ? <CitedText text={moatText} /> : 'Evaluating...'}
        </p>
      </div>
    </div>
  );
}
