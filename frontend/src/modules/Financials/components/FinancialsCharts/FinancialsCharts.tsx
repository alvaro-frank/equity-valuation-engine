import { useTranslation, Trans } from 'react-i18next';
import { useFinancialsChartsData } from './hooks/useFinancialsChartsData';
import { ChartCard } from '@/common/components/ChartCard';
import { RevenueProfitChart } from './components/RevenueProfitChart';
import { FinancialsMarginChart } from './components/FinancialsMarginChart';
import { RoceWaccChart } from './components/RoceWaccChart';
import { CashFlowCapexChart } from './components/CashFlowCapexChart';
import { DebtProfileChart } from './components/DebtProfileChart';
import { LiquidityProfileChart } from './components/LiquidityProfileChart';
import { SharesOutstandingChart } from './components/SharesOutstandingChart';
import { EarningsQualityChart } from './components/EarningsQualityChart';
import { OpExBreakdownChart } from './components/OpExBreakdownChart';
import { EpsChart } from './components/EpsChart';
import { CapitalStructureChart } from './components/CapitalStructureChart';
import { WorkingCapitalChart } from './components/WorkingCapitalChart';
import { FcfConversionChart } from './components/FcfConversionChart';
import { ShareholderReturnsChart } from './components/ShareholderReturnsChart';
import { CashFlowPillarsChart } from './components/CashFlowPillarsChart';
import { ValuationMultiplesChart } from './components/ValuationMultiplesChart';
import { RoeRoicChart } from './components/RoeRoicChart';
import { FcfYieldChart } from './components/FcfYieldChart';
import { LeverageRatioChart } from './components/LeverageRatioChart';
import { EarningsVsCashFlowMultiplesChart } from './components/EarningsVsCashFlowMultiplesChart';
import { useParams } from 'react-router-dom';
import { useFinancialsView } from '../../hooks/useFinancialsView';

interface FinancialsChartsProps {
  isQuarterly: boolean;
  activeTab: string;
}

export function FinancialsCharts({ isQuarterly, activeTab }: FinancialsChartsProps) {
  const { t } = useTranslation();
  const { ticker } = useParams<{ ticker: string }>();
  // We re-use the hook to get quantData. It's cached by react-query.
  const { quantData } = useFinancialsView(ticker!);
  const chartData = useFinancialsChartsData(quantData, isQuarterly);


  if (!chartData || chartData.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] bg-surface-container-low rounded-xl border border-outline-variant shadow-sm p-8 text-center">
        <p className="text-on-surface-variant font-medium">
          {t('financials.no_chart_data', 'No historical data available for charts.')}
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in fade-in duration-500">
        
        {activeTab === 'income_statement' && (
          <>
            <ChartCard 
              title={t('financials.charts.revenue_profit_title', 'Revenue & Profitability')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.revenue_profit_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />,
                    3: <span style={{ color: 'var(--secondary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <RevenueProfitChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.margins_title', 'Margin Evolution')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.margins_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />,
                    3: <span style={{ color: 'var(--secondary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <FinancialsMarginChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.earnings_quality_title', 'Earnings Quality')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.earnings_quality_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <EarningsQualityChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.opex_breakdown_title', 'Operating Expenses Breakdown')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.opex_breakdown_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <OpExBreakdownChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.shares_title', 'Shares Outstanding')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.shares_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <SharesOutstandingChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.eps_title', 'Diluted EPS')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.eps_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <EpsChart data={chartData} />
            </ChartCard>
          </>
        )}

        {activeTab === 'balance_sheet' && (
          <>
            <ChartCard 
              title={t('financials.charts.capital_structure_title', 'Capital Structure')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.capital_structure_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <CapitalStructureChart data={chartData} />
            </ChartCard>
            
            <ChartCard 
              title={t('financials.charts.debt_profile_title', 'Debt Profile')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.debt_profile_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />,
                    3: <span style={{ color: 'var(--secondary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <DebtProfileChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.working_capital_title', 'Working Capital Evolution')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.working_capital_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />,
                    3: <span style={{ color: 'var(--secondary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <WorkingCapitalChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.liquidity_title', 'Liquidity Profile')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.liquidity_profile_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />,
                    3: <span style={{ color: 'var(--secondary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <LiquidityProfileChart data={chartData} />
            </ChartCard>
          </>
        )}

        {activeTab === 'cash_flow' && (
          <>
            <ChartCard 
              title={t('financials.charts.fcf_conversion_title', 'FCF Conversion (Earnings Quality)')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.fcf_conversion_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />,
                    3: <span style={{ color: 'var(--secondary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <FcfConversionChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.shareholder_returns_title', 'Shareholder Returns')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.shareholder_returns_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <ShareholderReturnsChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.cash_flow_pillars_title', 'The 3 Pillars (CF Summary)')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.cash_flow_pillars_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />,
                    3: <span style={{ color: 'var(--secondary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <CashFlowPillarsChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.operating_cash_flow_title', 'Operating Cash Flow vs CapEx')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.cashflow_capex_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />,
                    3: <span style={{ color: 'var(--secondary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <CashFlowCapexChart data={chartData} />
            </ChartCard>
          </>
        )}

        {activeTab === 'ratios' && (
          <>
            <ChartCard 
              title={t('financials.charts.valuation_multiples_title', 'Valuation Multiples')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.valuation_multiples_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <ValuationMultiplesChart data={chartData} />
            </ChartCard>
            
            <ChartCard 
              title={t('financials.charts.earnings_cashflow_multiples_title', 'Earnings vs Cash Flow Multiples')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.earnings_cashflow_multiples_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />,
                    2: <span style={{ color: 'var(--tertiary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <EarningsVsCashFlowMultiplesChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.fcf_yield_title', 'FCF Yield')}
              tooltipText={
                <Trans
                  i18nKey="financials.charts.fcf_yield_tooltip"
                  components={{
                    1: <span style={{ color: 'var(--primary)' }} className="font-semibold" />
                  }}
                />
              }
            >
              <FcfYieldChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.roe_roic_title', 'Profitability (ROE vs ROIC)')} 
            >
              <RoeRoicChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.roce_wacc_title', 'ROCE vs WACC')} 
            >
              <RoceWaccChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.leverage_ratio_title', 'Leverage (Debt-to-Equity)')} 
            >
              <LeverageRatioChart data={chartData} />
            </ChartCard>
          </>
        )}

      </div>
    </div>
  );
}
