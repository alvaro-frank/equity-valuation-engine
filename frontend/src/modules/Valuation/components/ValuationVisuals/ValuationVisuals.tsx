import { useState } from 'react';
import type { DCFScenario } from '@/common/types/valuation';
import { generateSensitivityMatrix } from '../../utils/dcfCalculator';
import { useTranslation } from 'react-i18next';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from 'recharts';

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

  const formatBillion = (val: number) => `$${val.toFixed(1)}B`;

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
            <div className="flex-1 flex items-stretch justify-center overflow-x-auto">
              <table className="w-full h-full border-collapse">
                <thead>
                  <tr>
                    <th className="p-4 border border-outline-variant bg-surface-container-highest text-sm text-on-surface-variant font-medium">
                      WACC \ T.G.R.
                    </th>
                    {matrix[0].map((cell, i) => (
                      <th key={i} className="p-4 border border-outline-variant bg-surface-container-highest text-base text-on-surface font-medium min-w-[100px]">
                        {(cell.terminal_growth * 100).toFixed(1)}%
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {matrix.map((row, i) => (
                    <tr key={i}>
                      <td className="p-4 border border-outline-variant bg-surface-container-highest text-base text-on-surface font-medium text-center">
                        {(row[0].wacc * 100).toFixed(1)}%
                      </td>
                      {row.map((cell, j) => {
                        const safeCurrentPrice = Number(currentPrice) || 0;
                        const margin = safeCurrentPrice > 0 ? ((cell.intrinsic_value - safeCurrentPrice) / safeCurrentPrice) * 100 : 0;
                        const isUndervalued = margin > 0;
                        // Calculate intensity (0 to 1) capping at 40% margin
                        const intensity = Math.min(Math.abs(margin) / 40, 1);
                        
                        // We use inline styles for the heatmap effect
                        const bgColor = isUndervalued 
                          ? `rgba(76, 175, 80, ${0.1 + intensity * 0.4})` // Green shades
                          : `rgba(244, 67, 54, ${0.1 + intensity * 0.4})`; // Red shades

                        return (
                          <td 
                            key={j} 
                            style={{ backgroundColor: bgColor }}
                            className="p-4 border border-outline-variant text-center text-lg font-medium text-on-surface transition-colors duration-300"
                          >
                            ${cell.intrinsic_value.toFixed(2)}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

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
          </div>
        )}

        {activeTab === 'cashflows' && (
          <div className="flex flex-col h-full min-h-[300px]">
             <p className="text-body-lg font-medium text-on-surface mb-6 text-center">
              {t('valuation.cashflows_subtitle', 'Projected Free Cash Flow for the next 10 years (in Billions USD).')}
            </p>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={cashflowData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--outline-variant)" />
                <XAxis dataKey="year" stroke="var(--on-surface)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis tickFormatter={formatBillion} stroke="var(--on-surface)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{fill: 'var(--surface-container-highest)', opacity: 0.4}}
                  contentStyle={{ backgroundColor: 'var(--surface-container-high)', border: '1px solid var(--outline-variant)', borderRadius: '8px' }}
                  itemStyle={{ color: 'var(--on-surface)', fontWeight: 'bold' }}
                  labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
                  formatter={(value: number) => [formatBillion(value), 'FCF']}
                />
                <Bar dataKey="fcf" fill="var(--tertiary)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
};
