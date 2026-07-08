import { useTranslation } from 'react-i18next';
import { useFinancialsChartsData } from './hooks/useFinancialsChartsData';
import { ChartCard } from './components/ChartCard';
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
            >
              <RevenueProfitChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.margins_title', 'Margin Evolution')} 
            >
              <FinancialsMarginChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.earnings_quality_title', 'Earnings Quality')} 
            >
              <EarningsQualityChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.opex_breakdown_title', 'Operating Expenses Breakdown')} 
            >
              <OpExBreakdownChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.shares_title', 'Shares Outstanding')} 
            >
              <SharesOutstandingChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.eps_title', 'Diluted EPS')} 
            >
              <EpsChart data={chartData} />
            </ChartCard>
          </>
        )}

        {activeTab === 'balance_sheet' && (
          <>
            <ChartCard 
              title={t('financials.charts.debt_profile_title', 'Debt Profile')} 
            >
              <DebtProfileChart data={chartData} />
            </ChartCard>

            <ChartCard 
              title={t('financials.charts.liquidity_title', 'Liquidity Profile')} 
            >
              <LiquidityProfileChart data={chartData} />
            </ChartCard>
          </>
        )}

        {activeTab === 'cash_flow' && (
          <ChartCard 
            title={t('financials.charts.cashflow_capex_title', 'Cash From Operations vs CapEx')} 
          >
            <CashFlowCapexChart data={chartData} />
          </ChartCard>
        )}

        {activeTab === 'ratios' && (
          <ChartCard 
            title={t('financials.charts.roce_wacc_title', 'ROCE vs WACC')} 
          >
            <RoceWaccChart data={chartData} />
          </ChartCard>
        )}

      </div>
    </div>
  );
}
