import { CitedText } from '@/common/components/CitedText/CitedText';
import type { SourceInfo } from '@/common/types/valuation';

export interface MacroCardProps {
  bgIcon: string;
  icon: string;
  title: string;
  text: string;
  sources?: Record<string, SourceInfo>;
}

export function MacroCard({ bgIcon, icon, title, text, sources }: MacroCardProps) {
  if (!text) return null;
  
  return (
    <div className="bg-surface-container border border-outline-variant p-8 rounded flex flex-col gap-4 relative overflow-hidden">
      <div className="absolute top-0 right-0 p-8 opacity-5">
        <span className="material-symbols-outlined text-[120px]">{bgIcon}</span>
      </div>
      <div className="flex items-center gap-3 pb-4 border-b border-outline-variant relative z-10">
        <span className="material-symbols-outlined text-primary text-[32px]">{icon}</span>
        <h3 className="font-display-sm text-2xl text-on-surface">{title}</h3>
      </div>
      <p className="text-on-surface-variant text-base leading-relaxed whitespace-pre-wrap relative z-10 mt-2">
        <CitedText text={text} sources={sources} />
      </p>
    </div>
  );
}
