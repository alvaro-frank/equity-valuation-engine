import { CitedText } from '@/common/components/CitedText/CitedText';

interface RiskCardProps {
  risk: string;
  description: string;
  index: number;
}

export function RiskCard({ risk, description, index }: RiskCardProps) {
  return (
    <div className="flex flex-col gap-3 bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/50">
      <h4 className="font-bold text-on-surface text-base flex items-start gap-2">
        <div className="w-6 h-6 rounded-full bg-error/10 flex items-center justify-center shrink-0 border border-error/20 mt-0.5">
          <span className="font-bold text-error text-xs">{index + 1}</span>
        </div>
        {risk}
      </h4>
      <div className="text-sm text-on-surface-variant leading-relaxed whitespace-pre-wrap">
        <CitedText text={description} />
      </div>
    </div>
  );
}
