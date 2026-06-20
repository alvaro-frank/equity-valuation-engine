import { useTranslation } from 'react-i18next';

export function MatrixHelp() {
  const { t } = useTranslation();

  return (
    <div className="mt-6 bg-surface-container-high rounded-lg p-4 border border-outline-variant flex gap-4 items-start animate-in fade-in slide-in-from-bottom-2 duration-500">
      <span className="material-symbols-outlined text-primary mt-0.5">lightbulb</span>
      <div>
        <h4 className="text-label-md font-medium text-on-surface mb-1">
          {t('valuation.matrix_help_title', 'How to read this matrix?')}
        </h4>
        <p className="text-body-sm text-on-surface-variant leading-relaxed">
          {t('valuation.matrix_help_desc', 'The matrix shows how the valuation changes if our growth and risk assumptions are slightly wrong. A mostly green matrix indicates a high margin of safety—the investment remains profitable even if the economy worsens. A mostly red matrix warns that the investment is highly speculative.')}
        </p>
      </div>
    </div>
  );
}
