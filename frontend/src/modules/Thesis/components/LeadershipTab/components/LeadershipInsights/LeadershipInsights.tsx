import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

interface LeadershipInsightsProps {
  content: string;
}

export function LeadershipInsights({ content }: LeadershipInsightsProps) {
  const { t } = useTranslation();
  return (
    <div className="lg:col-span-2">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-primary">insights</span>
        {t('thesis_view.leadership_title')}
      </h3>
      <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 min-h-[400px]">
        <p><CitedText text={content} /></p>
      </div>
    </div>
  );
}
