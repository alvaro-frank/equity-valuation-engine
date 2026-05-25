import React from 'react';

export function DashboardSkeleton() {
  return (
    <div className="max-w-[1600px] mx-auto space-y-panel-gap animate-pulse">
      {/* Dashboard Header Skeleton */}
      <div className="flex items-end justify-between px-2 pt-2 pb-1">
        <div className="flex items-center gap-3">
          {/* Title */}
          <div className="h-10 w-64 bg-surface-container-high rounded-md"></div>
          {/* Badge */}
          <div className="h-6 w-16 bg-surface-container-high rounded-full"></div>
        </div>
        <div className="flex flex-col items-end gap-2">
          {/* Live Pricing tag */}
          <div className="h-4 w-32 bg-surface-container-high rounded-sm"></div>
          {/* Price */}
          <div className="h-10 w-48 bg-surface-container-high rounded-md"></div>
        </div>
      </div>

      {/* Section 1: Fundamental KPIs (5 Cards) */}
      <section className="grid grid-cols-1 md:grid-cols-5 gap-panel-gap">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="bg-surface-container-low border border-outline-variant p-3 flex flex-col h-28 rounded-[2px]">
            <div className="flex justify-between items-start">
              <div className="h-4 w-24 bg-surface-container-high rounded-sm"></div>
              <div className="h-4 w-4 bg-surface-container-high rounded-full"></div>
            </div>
            <div className="mt-auto">
              <div className="h-6 w-32 bg-surface-container-high rounded-sm mb-2"></div>
              <div className="h-3 w-16 bg-surface-container-high rounded-sm"></div>
            </div>
          </div>
        ))}
      </section>

      {/* Section 2: Business & Moat (2/3 and 1/3) */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-panel-gap">
        {/* Left: Business Strategy */}
        <div className="lg:col-span-2 bg-surface-container-low border border-outline-variant flex flex-col rounded-[2px]">
          <div className="px-4 py-3 border-b border-outline-variant">
            <div className="h-5 w-64 bg-surface-container-high rounded-sm"></div>
          </div>
          <div className="p-6 space-y-4">
            <div className="space-y-2">
              <div className="h-4 w-full bg-surface-container-high rounded-sm"></div>
              <div className="h-4 w-[90%] bg-surface-container-high rounded-sm"></div>
              <div className="h-4 w-[95%] bg-surface-container-high rounded-sm"></div>
            </div>
            
            <div className="grid grid-cols-3 gap-4 pt-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="bg-surface-container-lowest p-3 border border-outline-variant/50 flex flex-col h-48 rounded-[2px]">
                  <div className="h-4 w-24 bg-surface-container-high rounded-sm mb-4"></div>
                  <div className="space-y-2">
                    <div className="h-3 w-full bg-surface-container-high rounded-sm"></div>
                    <div className="h-3 w-[85%] bg-surface-container-high rounded-sm"></div>
                    <div className="h-3 w-[90%] bg-surface-container-high rounded-sm"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right: Leadership & Governance */}
        <div className="bg-surface-container-low border border-outline-variant flex flex-col rounded-[2px]">
          <div className="px-4 py-3 border-b border-outline-variant">
            <div className="h-5 w-48 bg-surface-container-high rounded-sm"></div>
          </div>
          <div className="p-4 flex-1 flex flex-col space-y-6">
            <div className="flex items-center gap-4">
              <div className="h-12 w-12 rounded-full bg-surface-container-high shrink-0"></div>
              <div className="space-y-2 w-full">
                <div className="h-4 w-32 bg-surface-container-high rounded-sm"></div>
                <div className="h-3 w-24 bg-surface-container-high rounded-sm"></div>
              </div>
            </div>
            <div className="space-y-2">
              <div className="h-3 w-full bg-surface-container-high rounded-sm"></div>
              <div className="h-3 w-[90%] bg-surface-container-high rounded-sm"></div>
              <div className="h-3 w-[95%] bg-surface-container-high rounded-sm"></div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Floating Toast Notification for gathering intelligence */}
      <div className="fixed bottom-6 right-6 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
        <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
        <span className="text-on-surface font-medium text-sm animate-pulse">Parsing SEC filings & reports...</span>
      </div>
    </div>
  );
}
