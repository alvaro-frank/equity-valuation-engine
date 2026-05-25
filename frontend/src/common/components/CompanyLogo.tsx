import React, { useState, useEffect } from 'react';

interface CompanyLogoProps {
  ticker?: string;
  className?: string;
}

export function CompanyLogo({ ticker, className = "w-8 h-8" }: CompanyLogoProps) {
  const [hasError, setHasError] = useState(false);

  // Reset error state when ticker changes
  useEffect(() => {
    setHasError(false);
  }, [ticker]);
  
  // Read token from environment variables (defaults to a placeholder if not set)
  const token = import.meta.env.VITE_LOGODEV_API_KEY || 'pk_your_publishable_key';
  
  if (!ticker || hasError) {
    return (
      <div className={`${className} rounded bg-primary-container flex items-center justify-center text-on-primary-container font-bold text-sm shrink-0`}>
        {ticker ? ticker[0].toUpperCase() : 'T'}
      </div>
    );
  }

  const imgUrl = `https://img.logo.dev/ticker/${ticker}?token=${token}`;

  return (
    <img 
      src={imgUrl} 
      alt={`${ticker} logo`}
      title={`${ticker} logo`}
      className={`${className} rounded object-cover shrink-0 bg-white`}
      onError={() => setHasError(true)}
    />
  );
}
