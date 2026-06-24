import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

interface RisksColumnProps {
  riskFactors?: Record<string, string>;
}

export function RisksColumn({ riskFactors }: RisksColumnProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-transparent p-4 border border-outline-variant/50 rounded-2xl flex flex-col h-56">
      <span className="font-label-caps text-label-caps text-tertiary mb-2 shrink-0">{t('company_profile.key_risks')}</span>
      <div className="overflow-y-auto custom-scrollbar pr-2 h-full flex flex-col gap-3">
        {!riskFactors ? (
          <p className="text-body-sm text-on-surface-variant leading-relaxed">Evaluating...</p>
        ) : (
          Object.entries(riskFactors).map(([risk, description]) => (
            <div key={risk} className="text-body-sm leading-relaxed">
              <strong className="text-on-surface font-semibold">{risk}: </strong>
              <span className="text-on-surface-variant">
                <CitedText text={description} />
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
