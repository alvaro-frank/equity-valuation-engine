import type { DCFAssumptions } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';

interface ValuationEngineProps {
  assumptions: DCFAssumptions | null;
  justification?: string;
  onAssumptionChange: (key: keyof DCFAssumptions, value: number) => void;
  isEditable?: boolean;
}

import { AssumptionSlider } from './components/AssumptionSlider';
import { AIRationale } from './components/AIRationale';

export const ValuationEngine = ({ assumptions, justification, onAssumptionChange, isEditable = true }: ValuationEngineProps) => {
  const { t } = useTranslation();

  if (!assumptions) return null;

  return (
    <div className="flex flex-col gap-6">
      <div className="bg-surface-container rounded-xl border border-outline-variant p-6">
        <h2 className="text-title-md font-medium text-on-surface mb-6 flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">tune</span>
          {t('valuation.assumptions_engine', 'Assumptions Engine')}
        </h2>

        <AssumptionSlider
          label={t('valuation.growth_1_5', 'FCF Growth (Years 1-5)')}
          min={-0.10}
          max={0.40}
          step={0.005}
          value={assumptions.fcf_growth_1_to_5}
          onChange={(val) => onAssumptionChange('fcf_growth_1_to_5', val)}
          isPercentage={true}
          tooltipText={t('valuation.tooltip_growth_1_5', 'Estimated annual Free Cash Flow growth for the first 5 years.')}
          isEditable={isEditable}
        />
        <AssumptionSlider
          label={t('valuation.growth_6_10', 'FCF Growth (Years 6-10)')}
          min={-0.10}
          max={0.40}
          step={0.005}
          value={assumptions.fcf_growth_6_to_10}
          onChange={(val) => onAssumptionChange('fcf_growth_6_to_10', val)}
          isPercentage={true}
          tooltipText={t('valuation.tooltip_growth_6_10', 'Estimated annual Free Cash Flow growth from year 6 to 10.')}
          isEditable={isEditable}
        />
        <AssumptionSlider
          label={t('valuation.wacc', 'WACC (Discount Rate)')}
          min={0.04}
          max={0.20}
          step={0.001}
          value={assumptions.wacc}
          onChange={(val) => onAssumptionChange('wacc', val)}
          isPercentage={true}
          tooltipText={t('valuation.tooltip_wacc', 'Weighted Average Cost of Capital. Represents the risk and required rate of return.')}
          isEditable={isEditable}
        />
        <AssumptionSlider
          label={t('valuation.terminal_growth', 'Terminal Growth Rate')}
          min={0.0}
          max={0.05}
          step={0.001}
          value={assumptions.terminal_growth_rate}
          onChange={(val) => onAssumptionChange('terminal_growth_rate', val)}
          isPercentage={true}
          tooltipText={t('valuation.tooltip_terminal', 'Expected perpetual growth rate for the company after year 10.')}
          isEditable={isEditable}
        />
      </div>

      {justification && (
        <AIRationale justification={justification} />
      )}
    </div>
  );
};
