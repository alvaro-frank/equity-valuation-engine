import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';
import { MoatRadarChart } from '../../../MoatRadarChart';
import type { MoatSources } from '@/common/types/valuation';

interface MoatOverviewProps {
  content: string;
  moatSources?: MoatSources;
}

export function MoatOverview({ content, moatSources }: MoatOverviewProps) {
  const { t } = useTranslation();
  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-primary">fort</span>
        {t('thesis_view.moat_title')}
      </h3>
      <div className="grid grid-cols-1 2xl:grid-cols-2 gap-6 bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 items-center">
        <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed">
          <p><CitedText text={content} /></p>
        </div>
        {moatSources ? (
          <div className="2xl:border-l 2xl:pl-6 2xl:border-t-0 border-t pt-6 2xl:pt-0 border-outline-variant/50 w-full h-full flex items-center justify-center">
            <MoatRadarChart data={moatSources} />
          </div>
        ) : null}
      </div>
    </div>
  );
}
