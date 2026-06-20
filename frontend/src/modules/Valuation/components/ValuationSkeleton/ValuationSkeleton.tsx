
import { HeaderSkeleton } from './components/HeaderSkeleton';
import { ContentSkeleton } from './components/ContentSkeleton';
import { CalculatingToast } from './components/CalculatingToast';

export function ValuationSkeleton() {
  return (
    <div className="max-w-[1600px] mx-auto w-full flex-1 pb-12 flex flex-col animate-in fade-in duration-500">
      <HeaderSkeleton />
      <ContentSkeleton />
      <CalculatingToast />
    </div>
  );
}
