import { useTranslation } from 'react-i18next';
import { ExecutiveCard } from '../ExecutiveCard';
import type { Executive } from '../ExecutiveCard';

interface ExecutivesSectionProps {
  executives?: Executive[];
}

export function ExecutivesSection({ executives }: ExecutivesSectionProps) {
  const { t } = useTranslation();
  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-secondary">groups</span>
        {t('company_profile.leadership')}
      </h3>
      <div className="space-y-2">
        {executives?.map((exec, idx) => (
          <ExecutiveCard key={idx} exec={exec} />
        ))}
      </div>
    </div>
  );
}
