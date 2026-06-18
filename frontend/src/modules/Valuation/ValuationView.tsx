import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useValuationEngine } from './hooks/useValuationEngine';
import { ValuationHeader } from './components/ValuationHeader/ValuationHeader';
import { ValuationEngine } from './components/ValuationEngine/ValuationEngine';
import { ValuationVisuals } from './components/ValuationVisuals/ValuationVisuals';
import { ValuationSkeleton } from './components/ValuationSkeleton/ValuationSkeleton';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { parseApiError } from '@/common/utils/apiErrors';

export const ValuationView = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const { t } = useTranslation();
  const {
    dcfData,
    tickerData,
    isLoading,
    error,
    refetch,
    activeScenario,
    handleScenarioChange,
    customAssumptions,
    handleCustomAssumptionChange,
    currentScenarioData,
  } = useValuationEngine(ticker!);

  if (isLoading) {
    return <ValuationSkeleton />;
  }

  if (error || !dcfData || !currentScenarioData) {
    const errorState = parseApiError(error || new Error('Missing valuation data'), t, ticker!);
    return <ApiErrorState errorState={errorState} onRetry={refetch} />;
  }

  return (
    <div className="max-w-[1600px] mx-auto w-full flex-1 pb-12 flex flex-col animate-in fade-in duration-500">
      <ValuationHeader
        ticker={tickerData?.symbol || ticker!}
        tickerInfo={tickerData!}
        name={tickerData?.name || ''}
        currentPrice={tickerData?.current_price || 0}
        intrinsicValue={currentScenarioData.intrinsic_value_per_share}
        activeScenario={activeScenario}
        onScenarioChange={handleScenarioChange}
        isDcfUnavailable={dcfData.base_fcf_ttm < 0}
      />

      {dcfData.base_fcf_ttm < 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center p-8 mt-4 bg-surface-container rounded-2xl border border-outline-variant text-center">
          <div className="w-16 h-16 rounded-full bg-error/10 flex items-center justify-center mb-6">
            <span className="material-symbols-outlined text-error text-[32px]">money_off</span>
          </div>
          <h2 className="text-title-lg font-medium text-on-surface mb-3">
            {t('valuation.negative_fcf_error_title', 'DCF Valuation Unavailable')}
          </h2>
          <p className="text-body-md text-on-surface-variant max-w-lg mb-8 leading-relaxed">
            {t('valuation.negative_fcf_error_desc', 'This company currently has a negative Free Cash Flow. The classic DCF model applies growth rates to the base FCF, meaning negative cash flows will mathematically "grow" larger into the future. Therefore, a DCF valuation is fundamentally incompatible with this company at its current stage.')}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1 mt-4">
          {/* Left Panel: Engine */}
          <div className="lg:col-span-4">
            <ValuationEngine
              assumptions={customAssumptions}
              justification={activeScenario === 'custom' ? undefined : currentScenarioData.assumptions.justification}
              onAssumptionChange={handleCustomAssumptionChange}
              isEditable={activeScenario === 'custom'}
            />
          </div>

          {/* Right Panel: Visuals */}
          <div className="lg:col-span-8">
            <ValuationVisuals
              scenario={currentScenarioData}
              currentPrice={tickerData?.current_price}
            />
          </div>
        </div>
      )}
    </div>
  );
};
