import { CitedText } from '@/common/components/CitedText/CitedText';

interface HistoryCardProps {
  icon: string;
  iconColor: string;
  title: string;
  content: string;
}

export function HistoryCard({ icon, iconColor, title, content }: HistoryCardProps) {
  return (
    <div className="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/50 flex flex-col gap-4 h-full">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface flex items-center gap-2">
        <span className={`material-symbols-outlined ${iconColor} text-xl`}>{icon}</span>
        {title}
      </h3>
      <div className="text-body-md text-on-surface-variant leading-relaxed whitespace-pre-wrap">
        <CitedText text={content} />
      </div>
    </div>
  );
}
