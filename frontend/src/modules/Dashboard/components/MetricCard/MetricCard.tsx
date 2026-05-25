import React, { useState } from 'react';

interface MetricCardProps {
  label: string;
  value: string;
  icon: string;
  subValue?: string;
  subValueColor?: string;
  flipLabel?: string;
  flipValue?: string;
  flipSubValue?: string;
  children?: React.ReactNode;
}

export function MetricCard({ 
  label, 
  value, 
  icon, 
  subValue, 
  subValueColor = 'text-on-surface-variant',
  flipLabel,
  flipValue,
  flipSubValue,
  children 
}: MetricCardProps) {
  const [isFlipped, setIsFlipped] = useState(false);
  const canFlip = !!flipLabel && !!flipValue;

  const handleClick = () => {
    if (canFlip) setIsFlipped(!isFlipped);
  };

  const frontFace = (
    <div className="bg-surface-container-low border border-outline-variant p-3 flex flex-col h-full group hover:bg-surface-container transition-colors">
      <div className="flex justify-between items-start">
        <span className="font-label-caps text-label-caps text-on-surface-variant">{label}</span>
        <span className="material-symbols-outlined text-outline text-[16px]">{icon}</span>
      </div>
      <div className="mt-2">
        <p className="font-data-mono text-[20px] text-on-surface">{value}</p>
        {subValue && <p className={`text-[10px] mt-1 ${subValueColor}`}>{subValue}</p>}
        {children}
      </div>
    </div>
  );

  if (!canFlip) return frontFace;

  return (
    <div 
      className="group cursor-pointer perspective-1000 h-full" 
      onClick={handleClick}
      style={{ perspective: '1000px' }}
    >
      {/* Flipping Container using CSS Grid for stacking */}
      <div 
        className="grid w-full h-full duration-500 ease-in-out" 
        style={{ 
          transformStyle: 'preserve-3d', 
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
          gridTemplateAreas: '"stack"'
        }}
      >
        {/* Front Face */}
        <div 
          className="[grid-area:stack]"
          style={{ backfaceVisibility: 'hidden' }}
        >
          {frontFace}
          <div className="absolute top-3 left-1/2 -translate-x-1/2 flex gap-1 pointer-events-none">
            <span className="w-1 h-1 rounded-full bg-outline-variant opacity-50"></span>
            <span className="w-1 h-1 rounded-full bg-outline opacity-20"></span>
          </div>
        </div>

        {/* Back Face */}
        <div 
          className="[grid-area:stack] bg-primary-container border border-primary p-3 flex flex-col transition-colors shadow-md rounded-[2px]"
          style={{ 
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)'
          }}
        >
          <div className="absolute top-3 left-1/2 -translate-x-1/2 flex gap-1 pointer-events-none">
            <span className="w-1 h-1 rounded-full bg-primary opacity-30"></span>
            <span className="w-1 h-1 rounded-full bg-primary opacity-80"></span>
          </div>
          <div className="flex justify-between items-start">
            <span className="font-label-caps text-label-caps text-on-primary-container">{flipLabel}</span>
            <span className="material-symbols-outlined text-primary text-[16px]">sync</span>
          </div>
          <div className="mt-2">
            <p className="font-data-mono text-[20px] text-on-primary-container">{flipValue}</p>
            {flipSubValue && (
              <p className="text-[10px] mt-1 text-on-primary-container opacity-70">{flipSubValue}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
