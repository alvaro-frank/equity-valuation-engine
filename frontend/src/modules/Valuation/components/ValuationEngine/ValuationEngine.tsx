import type { DCFAssumptions } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';

interface ValuationEngineProps {
  assumptions: DCFAssumptions | null;
  justification?: string;
  onAssumptionChange: (key: keyof DCFAssumptions, value: number) => void;
  isEditable?: boolean;
}

export const ValuationEngine = ({ assumptions, justification, onAssumptionChange, isEditable = true }: ValuationEngineProps) => {
  const { t } = useTranslation();

  if (!assumptions) return null;

  const renderSlider = (
    key: keyof DCFAssumptions,
    label: string,
    min: number,
    max: number,
    step: number,
    isPercentage: boolean = true,
    tooltipText?: string
  ) => {
    const value = assumptions[key] as number;
    const displayValue = isPercentage ? `${(value * 100).toFixed(1)}%` : value.toString();

    return (
      <div className="flex flex-col gap-2 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5 group relative">
            <label className={`text-label-md font-medium text-on-surface ${!isEditable ? 'opacity-60' : ''}`}>{label}</label>
            {tooltipText && (
              <div className="relative flex items-center">
                <span className={`material-symbols-outlined text-[16px] text-on-surface-variant cursor-help transition-opacity ${!isEditable ? 'opacity-60 group-hover:opacity-100' : ''}`}>info</span>
                <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-48 p-2 bg-surface-container-highest border border-outline-variant text-on-surface text-xs rounded-md shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all pointer-events-none z-50 text-center font-normal leading-relaxed">
                  {tooltipText}
                  <div className="absolute left-1/2 -translate-x-1/2 top-full w-0 h-0 border-l-[5px] border-r-[5px] border-t-[5px] border-transparent border-t-outline-variant"></div>
                  <div className="absolute left-1/2 -translate-x-1/2 top-[calc(100%-1px)] w-0 h-0 border-l-[4px] border-r-[4px] border-t-[4px] border-transparent border-t-surface-container-highest"></div>
                </div>
              </div>
            )}
          </div>
          <span className={`text-label-md text-primary font-bold bg-primary/10 px-2 py-0.5 rounded ${!isEditable ? 'opacity-60' : ''}`}>
            {displayValue}
          </span>
        </div>
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onAssumptionChange(key, parseFloat(e.target.value))}
          disabled={!isEditable}
          className={`w-full h-2 bg-surface-container-highest rounded-lg appearance-none ${
            isEditable ? 'cursor-pointer accent-primary' : 'cursor-not-allowed accent-outline opacity-60'
          }`}
        />
      </div>
    );
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="bg-surface-container rounded-xl border border-outline-variant p-6">
        <h2 className="text-title-md font-medium text-on-surface mb-6 flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">tune</span>
          {t('valuation.assumptions_engine', 'Assumptions Engine')}
        </h2>

        {renderSlider('fcf_growth_1_to_5', t('valuation.growth_1_5', 'FCF Growth (Years 1-5)'), -0.10, 0.40, 0.005, true, t('valuation.tooltip_growth_1_5', 'Estimated annual Free Cash Flow growth for the first 5 years.'))}
        {renderSlider('fcf_growth_6_to_10', t('valuation.growth_6_10', 'FCF Growth (Years 6-10)'), -0.10, 0.40, 0.005, true, t('valuation.tooltip_growth_6_10', 'Estimated annual Free Cash Flow growth from year 6 to 10.'))}
        {renderSlider('wacc', t('valuation.wacc', 'WACC (Discount Rate)'), 0.04, 0.20, 0.001, true, t('valuation.tooltip_wacc', 'Weighted Average Cost of Capital. Represents the risk and required rate of return.'))}
        {renderSlider('terminal_growth_rate', t('valuation.terminal_growth', 'Terminal Growth Rate'), 0.0, 0.05, 0.001, true, t('valuation.tooltip_terminal', 'Expected perpetual growth rate for the company after year 10.'))}
      </div>

      {justification && (
        <div className="bg-primary/5 rounded-xl border border-primary/20 p-6">
          <h3 className="text-title-sm font-medium text-primary mb-3 flex items-center gap-2">
            <span className="material-symbols-outlined">auto_awesome</span>
            {t('valuation.ai_rationale', 'AI Rationale')}
          </h3>
          <p className="text-body-md text-on-surface-variant leading-relaxed">
            {justification}
          </p>
        </div>
      )}
    </div>
  );
};
