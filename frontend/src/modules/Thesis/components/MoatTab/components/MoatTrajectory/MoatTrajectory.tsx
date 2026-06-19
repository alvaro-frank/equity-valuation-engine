import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

interface MoatTrajectoryProps {
  content?: string;
}

export function MoatTrajectory({ content }: MoatTrajectoryProps) {
  const { t } = useTranslation();
  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-tertiary">trending_up</span>
        {t('thesis_view.moat_trajectory')}
      </h3>
      <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50">
        <p><CitedText text={content || ''} /></p>
      </div>
    </div>
  );
}
