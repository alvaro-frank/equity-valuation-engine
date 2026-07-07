import { useTranslation } from 'react-i18next';
import { useFinancialsChartsData } from './hooks/useFinancialsChartsData';
import { ChartCard } from './components/ChartCard';
import { RoceWaccChart } from './components/RoceWaccChart';
import { CashFlowCapexChart } from './components/CashFlowCapexChart';
import { DebtProfileChart } from './components/DebtProfileChart';
import { useParams } from 'react-router-dom';
import { useFinancialsView } from '../../hooks/useFinancialsView';

export function FinancialsCharts() {
  const { t } = useTranslation();
  const { ticker } = useParams<{ ticker: string }>();
  // We re-use the hook to get quantData. It's cached by react-query.
  const { quantData } = useFinancialsView(ticker!);
  const chartData = useFinancialsChartsData(quantData);


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
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in fade-in duration-500">
      <ChartCard 
        title={t('financials.charts.roce_wacc_title', 'ROCE vs WACC')} 
      >
        <RoceWaccChart data={chartData} />
      </ChartCard>
      
      <ChartCard 
        title={t('financials.charts.cashflow_capex_title', 'Cash From Operations vs CapEx')} 
      >
        <CashFlowCapexChart data={chartData} />
      </ChartCard>

      <div className="col-span-1 lg:col-span-2">
        <ChartCard 
          title={t('financials.charts.debt_profile_title', 'Debt Profile')} 
        >
          <DebtProfileChart data={chartData} />
        </ChartCard>
      </div>
    </div>
  );
}
