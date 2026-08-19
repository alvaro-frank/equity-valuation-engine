import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

interface MoatTrajectoryProps {
  status?: string;
  description?: string;
}

export function MoatTrajectory({ status, description }: MoatTrajectoryProps) {
  const { t } = useTranslation();

  const safeStatus = status?.toUpperCase() || '';

  return (
    <div className="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/50 flex flex-col gap-4">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface flex items-center gap-2">
        <span className="material-symbols-outlined text-tertiary text-xl">trending_up</span>
        {t('thesis_view.moat_trajectory')}
        {safeStatus === 'EXPANDING' && (
          <span className="ml-2 px-2 py-0.5 text-[10px] font-bold tracking-wide rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
            {t('thesis_view.moat_expanding', 'EXPANDING')}
          </span>
        )}
        {safeStatus === 'STABLE' && (
          <span className="ml-2 px-2 py-0.5 text-[10px] font-bold tracking-wide rounded-full bg-blue-500/10 text-blue-500 border border-blue-500/20">
            {t('thesis_view.moat_stable', 'STABLE')}
          </span>
        )}
        {safeStatus === 'SHRINKING' && (
          <span className="ml-2 px-2 py-0.5 text-[10px] font-bold tracking-wide rounded-full bg-red-500/10 text-red-500 border border-red-500/20">
            {t('thesis_view.moat_shrinking', 'SHRINKING')}
          </span>
        )}
      </h3>
      <div className="text-body-md text-on-surface-variant leading-relaxed whitespace-pre-wrap">
        <CitedText text={description || ''} />
      </div>
    </div>
  );
}
