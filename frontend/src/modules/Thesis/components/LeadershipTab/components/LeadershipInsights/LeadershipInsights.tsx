import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

interface LeadershipInsightsProps {
  content: string;
}

export function LeadershipInsights({ content }: LeadershipInsightsProps) {
  const { t } = useTranslation();
  return (
    <div className="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/50 flex flex-col gap-4">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface flex items-center gap-2">
        <span className="material-symbols-outlined text-primary text-xl">insights</span>
        {t('thesis_view.leadership_title')}
      </h3>
      <div className="text-body-md text-on-surface-variant leading-relaxed whitespace-pre-wrap">
        <CitedText text={content} />
      </div>
    </div>
  );
}
