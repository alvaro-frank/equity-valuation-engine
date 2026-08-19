import { CatalystCard } from '../CatalystCard';

interface Catalyst {
  event: string;
  impact: string;
}

interface CatalystsListProps {
  catalysts: Catalyst[];
}

export function CatalystsList({ catalysts }: CatalystsListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {catalysts.map((catalyst, index) => (
        <CatalystCard
          key={index}
          event={catalyst.event}
          impact={catalyst.impact}
        />
      ))}
    </div>
  );
}
