import { CitedText } from '@/common/components/CitedText/CitedText';

interface CatalystCardProps {
  event: string;
  impact: string;
}

export function CatalystCard({ event, impact }: CatalystCardProps) {
  return (
    <div className="flex flex-col gap-3 bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/50">
      <h4 className="font-bold text-on-surface text-base flex items-start gap-2">
        <span className="material-symbols-outlined text-tertiary mt-0.5">bolt</span>
        {event}
      </h4>
      <div className="text-sm text-on-surface-variant leading-relaxed whitespace-pre-wrap">
        <CitedText text={impact} />
      </div>
    </div>
  );
}
