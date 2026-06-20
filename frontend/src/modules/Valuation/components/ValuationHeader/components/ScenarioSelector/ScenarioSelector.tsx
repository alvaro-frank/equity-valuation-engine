import type { ScenarioType } from '../../../../hooks/useValuationEngine';
import { useTranslation } from 'react-i18next';

export interface ScenarioSelectorProps {
  activeScenario: ScenarioType;
  onScenarioChange: (scenario: ScenarioType) => void;
}

export function ScenarioSelector({ activeScenario, onScenarioChange }: ScenarioSelectorProps) {
  const { t } = useTranslation();

  const scenarios: { type: ScenarioType; icon: string; label: string }[] = [
    { type: 'bear', icon: 'trending_down', label: t('valuation.scenario_bear', 'Bear') },
    { type: 'fair', icon: 'balance', label: t('valuation.scenario_fair', 'Fair') },
    { type: 'bull', icon: 'trending_up', label: t('valuation.scenario_bull', 'Bull') },
    { type: 'custom', icon: 'tune', label: t('valuation.scenario_custom', 'Custom') },
  ];

  return (
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
  );
}
