import { useTranslation } from 'react-i18next';

export interface AIRationaleProps {
  justification: string;
}

export function AIRationale({ justification }: AIRationaleProps) {
  const { t } = useTranslation();
  return (
    <div className="bg-primary/5 rounded-xl border border-primary/20 p-6">
      <h3 className="text-title-sm font-medium text-primary mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined">auto_awesome</span>
        {t('valuation.ai_rationale', 'AI Rationale')}
      </h3>
      <p className="text-body-md text-on-surface-variant leading-relaxed">
        {justification}
      </p>
    </div>
  );
}
