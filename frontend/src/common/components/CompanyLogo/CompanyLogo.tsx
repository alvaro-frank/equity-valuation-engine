import { useState, useEffect } from 'react';

interface CompanyLogoProps {
  ticker?: string;
  className?: string;
  fallbackLetter?: string;
}

const LOGO_BASE_URL = 'https://img.logo.dev/ticker';

export function CompanyLogo({ ticker, className = "w-8 h-8", fallbackLetter }: CompanyLogoProps) {
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setHasError(false);
  }, [ticker]);

  const token = import.meta.env.VITE_LOGODEV_API_KEY;
  
  // Base classes shared between fallback and image wrapper
  const containerClasses = `flex items-center justify-center rounded-md shrink-0 border border-outline-variant shadow-sm ${className}`;
  
  if (!ticker || hasError) {
    const letter = fallbackLetter || (ticker ? ticker[0].toUpperCase() : 'T');
    return (
      <div className={`${containerClasses} bg-surface-container-highest text-on-surface font-bold`}>
        {letter}
      </div>
    );
  }

  const imgUrl = `${LOGO_BASE_URL}/${ticker}?token=${token}&format=png&theme=dark`;

  return (
    <div className={`${containerClasses} bg-transparent overflow-hidden`}>
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
