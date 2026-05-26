import React, { useState, useEffect } from 'react';

interface CompanyLogoProps {
  ticker?: string;
  className?: string;
  fallbackLetter?: string;
}

export function CompanyLogo({ ticker, className = "w-8 h-8", fallbackLetter }: CompanyLogoProps) {
  const [hasError, setHasError] = useState(false);

  // Reset error state when ticker changes
  useEffect(() => {
    setHasError(false);
  }, [ticker]);
  
  // Read token from environment variables (defaults to a placeholder if not set)
  const token = import.meta.env.VITE_LOGODEV_API_KEY || 'pk_your_publishable_key';
  
  if (!ticker || hasError) {
    const letter = fallbackLetter || (ticker ? ticker[0].toUpperCase() : 'T');
    return (
      <div className={`flex items-center justify-center bg-surface-container-highest text-on-surface rounded-md font-bold shrink-0 border border-outline-variant shadow-sm ${className}`}>
        {letter}
      </div>
    );
  }

  const imgUrl = `https://img.logo.dev/ticker/${ticker}?token=${token}`;

  return (
    <div className={`flex items-center justify-center bg-white rounded-md overflow-hidden shrink-0 border border-outline-variant shadow-sm ${className}`}>
      <img 
        src={imgUrl} 
        alt={`${ticker} logo`}
        title={`${ticker} logo`}
        className="w-full h-full object-cover"
        onError={() => setHasError(true)}
      />
    </div>
  );
}
