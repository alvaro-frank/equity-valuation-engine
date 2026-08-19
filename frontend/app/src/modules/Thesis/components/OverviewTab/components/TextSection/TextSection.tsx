import { CitedText } from '@/common/components/CitedText/CitedText';

interface TextSectionProps {
  icon: string;
  iconColor: string;
  title: string;
  content: string;
}

export function TextSection({ icon, iconColor, title, content }: TextSectionProps) {
  return (
    <div className="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/50 flex flex-col gap-4">
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
