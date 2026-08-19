
import { translateSector, translateIndustry } from '@/common/utils/translations';
import type { ScenarioType } from '../../hooks/useValuationEngine';
import type { TickerResult } from '@/common/types/valuation';
import { VerdictDisplay } from './components/VerdictDisplay';
import { ScenarioSelector } from './components/ScenarioSelector';
import { MethodDropdown } from './components/MethodDropdown';

interface ValuationHeaderProps {
  ticker: string;
  tickerInfo: TickerResult;
  name: string;
  currentPrice: number;
  intrinsicValue: number;
  activeScenario: ScenarioType;
  onScenarioChange: (scenario: ScenarioType) => void;
  isDcfUnavailable?: boolean;
}

export const ValuationHeader = ({
  ticker,
  tickerInfo,
  name,
  currentPrice,
  intrinsicValue,
  activeScenario,
  onScenarioChange,
  isDcfUnavailable = false,
}: ValuationHeaderProps) => {
  return (
    <div className="sticky top-16 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 pt-6 pb-4 mb-6 flex flex-col md:flex-row md:items-start justify-between border-b border-outline-variant/20 -mx-4 px-4 sm:-mx-8 sm:px-8 gap-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="font-display-md text-display-md text-on-surface">{name || ticker}</h1>
          <MethodDropdown />
        </div>
        <p className="text-body-sm text-on-surface-variant mt-1.5 flex items-center gap-2">
          <span className="material-symbols-outlined text-[16px]">domain</span>
          {translateSector(tickerInfo?.sector)} / {translateIndustry(tickerInfo?.industry)}
        </p>
      </div>

      <div className="flex items-center gap-8">
        {/* Verdict */}
        <div className="flex items-center gap-6">
          {!isDcfUnavailable ? (
            <VerdictDisplay currentPrice={currentPrice} intrinsicValue={intrinsicValue} />
          ) : (
            <div className="flex flex-col items-end">
              <span className="text-label-sm text-on-surface-variant">Current Price</span>
              <span className="text-4xl font-bold text-on-surface">${(Number(currentPrice) || 0).toFixed(2)}</span>
            </div>
          )}
        </div>

        {/* Scenario Selector */}
        {!isDcfUnavailable && (
          <ScenarioSelector activeScenario={activeScenario} onScenarioChange={onScenarioChange} />
        )}
      </div>
    </div>
  );
};
