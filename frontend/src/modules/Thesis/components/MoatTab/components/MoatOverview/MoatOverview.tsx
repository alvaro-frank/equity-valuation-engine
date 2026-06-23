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
    <div className="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/50 flex flex-col gap-4">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface flex items-center gap-2">
        <span className="material-symbols-outlined text-primary text-xl">fort</span>
        {t('thesis_view.moat_title')}
      </h3>
      <div className="grid grid-cols-1 2xl:grid-cols-2 gap-6 items-center">
        <div className="text-body-md text-on-surface-variant leading-relaxed whitespace-pre-wrap">
          <CitedText text={content} />
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
