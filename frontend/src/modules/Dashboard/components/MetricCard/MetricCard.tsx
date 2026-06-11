import React, { useState } from 'react';

// --- Types ---
export interface MetricCardFlipData {
  label: string;
  value: string;
  subValue?: string;
}

interface MetricCardProps {
  label: string;
  value: string;
  icon: string;
  subValue?: string;
  subValueColor?: string;
  flipData?: MetricCardFlipData;
  children?: React.ReactNode;
}

interface CardFaceProps {
  label: string;
  value: string;
  icon: string;
  subValue?: string;
  subValueColor?: string;
  isBackFace?: boolean;
  children?: React.ReactNode;
}

// --- Sub-Components (Rule 2.21, 2.31) ---
function CardFace({ 
  label, 
  value, 
  icon, 
  subValue, 
  subValueColor = 'text-on-surface-variant', 
  isBackFace = false,
  children 
}: CardFaceProps) {
  if (isBackFace) {
    return (
      <div 
        className="[grid-area:stack] bg-primary-container border border-primary p-3 flex flex-col transition-colors shadow-md rounded-xl overflow-hidden"
        style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
      >
        <div className="absolute top-3 left-1/2 -translate-x-1/2 flex gap-1 pointer-events-none">
          <span className="w-1 h-1 rounded-full bg-primary opacity-30"></span>
          <span className="w-1 h-1 rounded-full bg-primary opacity-80"></span>
        </div>
        <div className="flex justify-between items-start">
          <span className="font-label-caps text-label-caps text-on-primary-container">{label}</span>
          <span className="material-symbols-outlined text-primary text-[16px]">{icon}</span>
        </div>
        <div className="mt-2">
          <p className="font-data-mono text-[20px] text-on-primary-container">{value}</p>
          {subValue ? (
            <p className="text-[10px] mt-1 text-on-primary-container opacity-70">{subValue}</p>
          ) : null}
          {children}
        </div>
      </div>
    );
  }

  return (
    <div 
      className="[grid-area:stack] bg-surface-container-low border border-outline-variant p-3 flex flex-col h-full group hover:bg-surface-container transition-colors rounded-xl overflow-hidden"
      style={{ backfaceVisibility: 'hidden' }}
    >
      <div className="absolute top-3 left-1/2 -translate-x-1/2 flex gap-1 pointer-events-none">
        <span className="w-1 h-1 rounded-full bg-outline-variant opacity-50"></span>
        <span className="w-1 h-1 rounded-full bg-outline opacity-20"></span>
      </div>
      <div className="flex justify-between items-start">
        <span className="font-label-caps text-label-caps text-on-surface-variant">{label}</span>
        <span className="material-symbols-outlined text-outline text-[16px]">{icon}</span>
      </div>
      <div className="mt-2">
        <p className="font-data-mono text-[20px] text-on-surface">{value}</p>
        {subValue ? <p className={`text-[10px] mt-1 ${subValueColor}`}>{subValue}</p> : null}
        {children}
      </div>
    </div>
  );
}

// --- Main Component ---
export function MetricCard({ 
  label, 
  value, 
  icon, 
  subValue, 
  subValueColor,
  flipData,
  children 
}: MetricCardProps) {
  const [isFlipped, setIsFlipped] = useState(false);
  const canFlip = !!flipData;

  const handleClick = () => {
    if (canFlip) setIsFlipped(!isFlipped);
  };

  return (
    <div 
      className={`h-full ${canFlip ? 'group cursor-pointer perspective-1000' : ''}`}
      onClick={handleClick}
      style={canFlip ? { perspective: '1000px' } : undefined}
    >
      <div 
        className="grid w-full h-full duration-500 ease-in-out" 
        style={{ 
          transformStyle: 'preserve-3d', 
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
          gridTemplateAreas: '"stack"'
        }}
      >
        <CardFace 
          label={label} 
          value={value} 
          icon={icon} 
          subValue={subValue} 
          subValueColor={subValueColor}
        >
          {children}
        </CardFace>

        {flipData ? (
          <CardFace 
            label={flipData.label} 
            value={flipData.value} 
            icon="sync" 
            subValue={flipData.subValue} 
            isBackFace
          />
        ) : null}
      </div>
    </div>
  );
}
