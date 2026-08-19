import { HeaderSkeleton } from './components/HeaderSkeleton';
import { SubNavSkeleton } from './components/SubNavSkeleton';
import { GridSkeleton } from './components/GridSkeleton';
import { DraftingToast } from './components/DraftingToast';

interface SectorSkeletonProps {
  language: string;
}

export function SectorSkeleton({ language }: SectorSkeletonProps) {
  return (
    <div className="max-w-[1600px] mx-auto w-full flex-1 flex flex-col gap-6 animate-in fade-in duration-500">
      <HeaderSkeleton />
      <SubNavSkeleton />
      <GridSkeleton />
      <DraftingToast language={language} />
    </div>
  );
}
