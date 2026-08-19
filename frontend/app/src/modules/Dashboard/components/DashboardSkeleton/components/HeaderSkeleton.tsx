import { Skeleton } from '@/common/components/Skeleton';

export function HeaderSkeleton() {
  return (
    <div className="flex items-end justify-between px-2 pt-2 pb-1">
      <div className="flex items-center gap-3">
        {/* Title */}
        <Skeleton className="h-10 w-64 rounded-md" />
        {/* Badge */}
        <Skeleton className="h-6 w-16 rounded-full" />
      </div>
      <div className="flex flex-col items-end gap-2">
        {/* Live Pricing tag */}
        <Skeleton className="h-4 w-32" />
        {/* Price */}
        <Skeleton className="h-10 w-48 rounded-md" />
      </div>
    </div>
  );
}
