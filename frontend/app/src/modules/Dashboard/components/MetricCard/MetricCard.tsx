import React, { useState } from 'react';
import { CardFace } from './components/CardFace';

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
