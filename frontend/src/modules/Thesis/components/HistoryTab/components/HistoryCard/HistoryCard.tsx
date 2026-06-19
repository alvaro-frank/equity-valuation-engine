import { CitedText } from '@/common/components/CitedText/CitedText';

interface HistoryCardProps {
  icon: string;
  iconColor: string;
  title: string;
  content: string;
}

export function HistoryCard({ icon, iconColor, title, content }: HistoryCardProps) {
  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className={`material-symbols-outlined ${iconColor}`}>{icon}</span>
        {title}
      </h3>
      <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 h-[calc(100%-40px)]">
        <p><CitedText text={content} /></p>
      </div>
    </div>
  );
}
