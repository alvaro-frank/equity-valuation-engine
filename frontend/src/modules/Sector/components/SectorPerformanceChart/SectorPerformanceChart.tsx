
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import type { SectorPerformanceData } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { useSectorPerformanceChart } from './useSectorPerformanceChart';
import { translateSector, translateIndustry } from '@/common/utils/translations';

// --- Sub-Components (Rule 2.23) ---

function NoDataState() {
  return (
    <div className="h-full flex items-center justify-center text-on-surface-variant p-8 bg-surface-container-low border border-outline-variant rounded-xl">
      No performance data available
    </div>
  );
}

interface ChartHeaderProps {
  companyTicker: string;
  companyName?: string;
  sector: string;
  industry: string;
  benchmarkTicker: string;
}

function ChartHeader({ companyTicker, companyName, sector, industry, benchmarkTicker }: ChartHeaderProps) {
  const { t } = useTranslation();
  return (
    <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
      <div>
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
          {t('sector_view.market_momentum', 'Relative Market Momentum (5Y)')}
        </h3>
        <p className="text-body-sm text-on-surface-variant">
          {t('sector_view.market_momentum_desc', 'Comparing Sector ETF performance vs Benchmark')}
        </p>
      </div>
      <div className="flex gap-2 cursor-default">
        {companyTicker && (
          <span className="text-xs px-2 py-1 bg-surface-container text-on-surface font-bold border border-outline-variant rounded">
            {companyName || companyTicker}
          </span>
        )}
        {industry && (
          <span className="text-xs px-2 py-1 bg-surface-container text-tertiary font-bold border border-outline-variant rounded">
            {translateIndustry(industry)}
          </span>
        )}
        {sector && (
          <span className="text-xs px-2 py-1 bg-surface-container text-primary font-bold border border-outline-variant rounded">
            {translateSector(sector)}
          </span>
        )}
        <span className="text-xs px-2 py-1 bg-surface-container font-bold border border-outline-variant rounded text-[var(--chart-benchmark)]">
          S&P 500
        </span>
      </div>
    </div>
  );
}

// --- Main Component ---

interface SectorPerformanceChartProps {
  data?: SectorPerformanceData;
  companyName?: string;
}

export function SectorPerformanceChart({ data, companyName }: SectorPerformanceChartProps) {
  const { formattedData, hasData, companyTicker, sector, industry, sectorEtf, industryEtf, benchmarkTicker, hiddenLines, handleLegendClick } = useSectorPerformanceChart(data);
  const { t } = useTranslation();

  if (!hasData) {
    return <NoDataState />;
  }

  return (
    <div className="bg-surface-container-low border border-outline-variant rounded-xl overflow-hidden h-[400px] flex flex-col w-full">
      <ChartHeader companyTicker={companyTicker} companyName={companyName} sector={sector} industry={industry} benchmarkTicker={benchmarkTicker} />
      <div className="p-4 flex-1 min-h-0 min-w-0">
        <ResponsiveContainer width="99%" height="100%" debounce={300}>
          <LineChart data={formattedData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--outline-variant)" vertical={false} />
            <XAxis 
              dataKey="formattedDate" 
              stroke="var(--outline)" 
              fontSize={11} 
              tickLine={false} 
              axisLine={false} 
              dy={10}
              minTickGap={40}
            />
            <YAxis 
              stroke="var(--outline)" 
              fontSize={11} 
              tickLine={false} 
              axisLine={false} 
              tickFormatter={(val) => `${val}%`}
            />
            <Tooltip 
              cursor={{ stroke: 'var(--outline-variant)', strokeWidth: 1, strokeDasharray: '3 3' }}
              contentStyle={{ backgroundColor: 'var(--surface-container-high)', borderColor: 'var(--outline-variant)', color: 'var(--on-surface)', borderRadius: '8px' }}
              itemStyle={{ color: 'var(--on-surface)' }}
              formatter={(value: unknown, name: unknown) => [`${Number(value).toFixed(2)}%`, name as string]}
              labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
            />
            <Legend 
              onClick={handleLegendClick}
              iconType="circle" 
              wrapperStyle={{ fontSize: '11px', color: 'var(--on-surface-variant)', paddingTop: '10px', cursor: 'pointer' }}
            />
            {companyTicker && (
              <Line 
                type="monotone" 
                dataKey={companyTicker} 
                name={companyName || t('sector_view.chart.company', 'Empresa')} 
                stroke="var(--on-surface)" 
                strokeWidth={3}
                dot={false}
                hide={hiddenLines[companyTicker]}
                activeDot={{ r: 5, strokeWidth: 0 }}
              />
            )}
            <Line 
              type="monotone" 
              dataKey={sectorEtf} 
              name={`${t('sector_view.chart.sector', 'Setor')}: ${translateSector(sector)}`} 
              stroke="var(--primary)" 
              strokeWidth={1.5}
              dot={false}
              hide={hiddenLines[sectorEtf]}
              activeDot={{ r: 4, strokeWidth: 0 }}
            />
            {industryEtf && (
              <Line 
                type="monotone" 
                dataKey={industryEtf} 
                name={`${t('sector_view.chart.industry', 'Indústria')}: ${translateIndustry(industry)}`} 
                stroke="var(--tertiary)" 
                strokeWidth={1.5}
                dot={false}
                hide={hiddenLines[industryEtf]}
                activeDot={{ r: 4, strokeWidth: 0 }}
              />
            )}
            <Line 
              type="monotone" 
              dataKey={benchmarkTicker} 
              name={`${t('sector_view.chart.benchmark', 'Benchmark')} (S&P 500)`} 
              stroke="var(--chart-benchmark)" 
              strokeWidth={1.5}
              dot={false}
              hide={hiddenLines[benchmarkTicker]}
              activeDot={{ r: 4, strokeWidth: 0 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
