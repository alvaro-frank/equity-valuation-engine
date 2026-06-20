import { useState } from 'react';
import type { DCFScenario } from '@/common/types/valuation';
import { generateSensitivityMatrix } from '../../utils/dcfCalculator';
import { useTranslation } from 'react-i18next';

import { SensitivityMatrix } from './components/SensitivityMatrix';
import { ProjectedCashFlowsChart } from './components/ProjectedCashFlowsChart';
import { MatrixHelp } from './components/MatrixHelp';

interface ValuationVisualsProps {
  scenario: DCFScenario | null;
  currentPrice: number;
}

export const ValuationVisuals = ({ scenario, currentPrice }: ValuationVisualsProps) => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<'sensitivity' | 'cashflows'>('sensitivity');

  if (!scenario) return null;

  const matrix = generateSensitivityMatrix(scenario);

  // Format cashflows for chart
  const cashflowData = scenario.projected_fcfs.map((fcf, index) => ({
    year: `Year ${index + 1}`,
    fcf: fcf / 1e9, // Convert to billions
  }));

  return (
    <div className="bg-surface-container rounded-xl border border-outline-variant flex flex-col h-full overflow-hidden">
      {/* Tabs Header */}
      <div className="flex border-b border-outline-variant">
        <button
          onClick={() => setActiveTab('sensitivity')}
          className={`flex-1 py-4 text-label-md font-medium text-center transition-colors ${
            activeTab === 'sensitivity'
              ? 'text-primary border-b-2 border-primary bg-surface-container-highest/30'
              : 'text-on-surface-variant hover:bg-surface-container-highest/50'
          }`}
        >
          {t('valuation.sensitivity_matrix', 'Sensitivity Matrix')}
        </button>
        <button
          onClick={() => setActiveTab('cashflows')}
          className={`flex-1 py-4 text-label-md font-medium text-center transition-colors ${
            activeTab === 'cashflows'
              ? 'text-primary border-b-2 border-primary bg-surface-container-highest/30'
              : 'text-on-surface-variant hover:bg-surface-container-highest/50'
          }`}
        >
          {t('valuation.projected_cashflows', 'Projected Cash Flows')}
        </button>
      </div>

      {/* Tab Content */}
      <div className="p-6 lg:p-10 lg:pb-12 flex-1 flex flex-col">
        {activeTab === 'sensitivity' && (
          <div className="flex flex-col h-full">
            <p className="text-body-lg font-medium text-on-surface mb-6 text-center">
              {t('valuation.matrix_subtitle', 'Intrinsic value per share based on variations in WACC (Y-axis) and Terminal Growth Rate (X-axis).')}
            </p>
            <SensitivityMatrix matrix={matrix} currentPrice={currentPrice} />
            <MatrixHelp />
          </div>
        )}

        {activeTab === 'cashflows' && (
          <div className="flex flex-col h-full min-h-[300px]">
             <p className="text-body-lg font-medium text-on-surface mb-6 text-center">
              {t('valuation.cashflows_subtitle', 'Projected Free Cash Flow for the next 10 years (in Billions USD).')}
            </p>
            <ProjectedCashFlowsChart cashflowData={cashflowData} />
          </div>
        )}
      </div>
    </div>
  );
};
