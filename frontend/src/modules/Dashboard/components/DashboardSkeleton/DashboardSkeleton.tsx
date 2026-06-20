import { HeaderSkeleton, KPIsSkeleton, BusinessMoatSkeleton, LoadingToast } from './components';

export function DashboardSkeleton() {
  return (
    <div className="max-w-[1600px] mx-auto w-full flex-1 space-y-panel-gap">
      <HeaderSkeleton />
      <KPIsSkeleton />
      <BusinessMoatSkeleton />
      <LoadingToast />
    </div>
  );
}
