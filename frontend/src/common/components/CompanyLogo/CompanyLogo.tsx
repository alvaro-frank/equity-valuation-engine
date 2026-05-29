import { useState } from 'react';

interface CompanyLogoProps {
  ticker?: string;
  className?: string;
  fallbackLetter?: string;
}

export function CompanyLogo({ ticker, className = "w-8 h-8", fallbackLetter }: CompanyLogoProps) {
  const [hasError, setHasError] = useState(false);

  const [prevTicker, setPrevTicker] = useState(ticker);

  if (ticker !== prevTicker) {
    setPrevTicker(ticker);
    setHasError(false);
  }

  const token = import.meta.env.VITE_LOGODEV_API_KEY;
  
  if (!ticker || hasError) {
    const letter = fallbackLetter || (ticker ? ticker[0].toUpperCase() : 'T');
    return (
      <div className={`flex items-center justify-center bg-surface-container-highest text-on-surface rounded-md font-bold shrink-0 border border-outline-variant shadow-sm ${className}`}>
        {letter}
      </div>
    );
  }

  const imgUrl = `https://img.logo.dev/ticker/${ticker}?token=${token}&format=png&theme=dark`;

  return (
    <div className={`flex items-center justify-center bg-transparent rounded-md overflow-hidden shrink-0 border border-outline-variant shadow-sm ${className}`}>
      <img 
        src={imgUrl} 
        alt={`${ticker} logo`}
        title={`${ticker} logo`}
        className="w-full h-full object-contain"
        onError={() => setHasError(true)}
      />
    </div>
  );
}
