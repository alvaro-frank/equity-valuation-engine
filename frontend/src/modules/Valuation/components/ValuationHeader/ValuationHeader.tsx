import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import type { ScenarioType } from '../../hooks/useValuationEngine';
import type { TickerResult } from '@/common/types/valuation';

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
  const { t } = useTranslation();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState('dcf');
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const safeCurrentPrice = Number(currentPrice) || 0;
  const safeIntrinsicValue = Number(intrinsicValue) || 0;
  const marginOfSafety = safeCurrentPrice > 0 ? ((safeIntrinsicValue - safeCurrentPrice) / safeCurrentPrice) * 100 : 0;
  const isUndervalued = marginOfSafety > 0;

  const scenarios: { type: ScenarioType; icon: string; label: string }[] = [
    { type: 'bear', icon: 'trending_down', label: t('valuation.scenario_bear', 'Bear') },
    { type: 'fair', icon: 'balance', label: t('valuation.scenario_fair', 'Fair') },
    { type: 'bull', icon: 'trending_up', label: t('valuation.scenario_bull', 'Bull') },
    { type: 'custom', icon: 'tune', label: t('valuation.scenario_custom', 'Custom') },
  ];

  const methods = [
    { id: 'dcf', label: t('valuation.dcf_valuation', 'DCF Valuation') },
    { id: 'val1', label: t('valuation.val1', 'Valuation 1') },
    { id: 'val2', label: t('valuation.val2', 'Valuation 2') }
  ];

  const activeMethodLabel = methods.find(m => m.id === selectedMethod)?.label;

  return (
    <div className="flex flex-col md:flex-row md:items-start justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6 gap-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="font-display-md text-display-md text-on-surface">{name || ticker}</h1>
          
          <div className="relative mt-1" ref={dropdownRef}>
            <button 
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center gap-1 bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider hover:bg-primary/20 transition-colors"
            >
              {activeMethodLabel}
              <span className="material-symbols-outlined text-[14px]">arrow_drop_down</span>
            </button>
            
            {isDropdownOpen && (
              <div className="absolute top-full left-0 mt-1 bg-surface-container-high border border-outline-variant rounded shadow-lg z-50 min-w-[140px] overflow-hidden">
                {methods.map(method => (
                  <button
                    key={method.id}
                    onClick={() => { setSelectedMethod(method.id); setIsDropdownOpen(false); }}
                    className={`w-full text-left px-3 py-2 text-xs font-bold uppercase tracking-wider transition-colors ${selectedMethod === method.id ? 'bg-primary/10 text-primary' : 'text-on-surface hover:bg-surface-container-highest'}`}
                  >
                    {method.label}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
        <p className="text-body-sm text-on-surface-variant mt-1.5 flex items-center gap-2">
          <span className="material-symbols-outlined text-[16px]">domain</span>
          {translateSector(tickerInfo?.sector)} / {translateIndustry(tickerInfo?.industry)}
        </p>
      </div>

      <div className="flex items-center gap-8">
        {/* Verdict */}
        <div className="flex items-center gap-6">
          <div className="flex flex-col items-end">
            <span className="text-label-sm text-on-surface-variant">{t('valuation.current_price', 'Current Price')}</span>
            <span className="text-4xl font-bold text-on-surface">${safeCurrentPrice.toFixed(2)}</span>
          </div>

          {!isDcfUnavailable && (
            <>
              <div className="w-px h-14 bg-outline-variant hidden sm:block"></div>

              <div className="flex flex-col items-end">
                <span className="text-label-sm text-on-surface-variant">{t('valuation.intrinsic_value', 'Intrinsic Value')}</span>
                <div className="flex items-center gap-3">
                  <span className="text-4xl font-bold tracking-tight text-on-surface">
                    ${safeIntrinsicValue.toFixed(2)}
                  </span>
                  <span
                    className={`text-sm font-bold px-2 py-1 rounded border border-outline-variant ${isUndervalued ? 'text-secondary' : 'text-error'
                      }`}
                  >
                    {isUndervalued ? '+' : ''}{marginOfSafety.toFixed(1)}%
                  </span>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Scenario Selector */}
        {!isDcfUnavailable && (
          <div className="flex bg-surface-container-high rounded-lg p-1 border border-outline-variant hidden lg:flex">
            {scenarios.map((scen) => (
              <button
                key={scen.type}
                onClick={() => onScenarioChange(scen.type)}
                className={`flex items-center gap-2 px-4 py-1.5 rounded-md text-label-md font-medium transition-colors duration-200 ${activeScenario === scen.type
                    ? 'bg-surface-container-lowest text-primary shadow-sm border border-outline-variant/50'
                    : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest/50'
                  }`}
              >
                <span className="material-symbols-outlined text-[18px]">{scen.icon}</span>
                {scen.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
