import React from 'react';
import * as Tooltip from '@radix-ui/react-tooltip';
import { useSources } from '@/common/contexts/SourcesContext';
import { type SourceInfo } from '@/common/types/valuation';

interface CitedTextProps {
  text: string;
  sources?: Record<string, SourceInfo | string>;
}

export function CitedText({ text, sources: overrideSources }: CitedTextProps) {
  const contextSources = useSources();
  const sources = overrideSources || contextSources;

  if (!text) return null;
  // Pre-process text to remove citations that have no matching sources
  let processedText = text;
  processedText = processedText.replace(/\s*\[((?:\d+\s*(?:,\s*)?)+)\]/g, (match, numbersGroup) => {
    const numberStrings = numbersGroup.split(',').map((n: string) => n.trim());
    const validCount = Object.keys(sources).length > 0 
      ? numberStrings.filter((n: string) => sources[n] !== undefined).length 
      : 0;
    
    if (validCount === 0) {
      // Remove the entire citation and its preceding space
      return '';
    }
    // Keep the original match
    return match;
  });

  if (Object.keys(sources).length === 0) {
    return <span>{processedText}</span>;
  }

  // Capturing group ensures numbers block is kept in the resulting array at odd indices
  // Matches "[8, 14, 28]" or "[1]"
  const parts = processedText.split(/\[((?:\d+\s*(?:,\s*)?)+)\]/g);

  return (
    <Tooltip.Provider delayDuration={150}>
      <span className="leading-relaxed">
        {parts.map((part, index) => {
          // Even indices are regular text
          if (index % 2 === 0) {
            return <span key={index}>{part}</span>;
          }

          // Odd indices are the captured numbers, e.g., "8, 14, 28"
          const numberStrings = part.split(',').map(n => n.trim());
          
          // Filter numbers that actually have a source
          const validSources = numberStrings
            .map(n => ({ number: n, sourceText: sources[n] }))
            .filter(item => item.sourceText !== undefined);

          if (validSources.length === 0) {
            return null;
          }

          // Single button triggering the tooltip
          const TriggerElement = React.forwardRef<HTMLButtonElement, any>((props, ref) => {
            const className = "inline-flex items-center justify-center w-[16px] h-[16px] mx-0.5 align-text-top text-primary/60 hover:text-primary hover:bg-primary/10 rounded cursor-pointer transition-all duration-150";
            return (
              <button
                type="button"
                className={className}
                aria-label={`Fontes`}
                {...props}
                ref={ref}
              >
                <span className="material-symbols-outlined" style={{ fontSize: '13px', fontVariationSettings: "'FILL' 0, 'wght' 400" }}>
                  format_quote
                </span>
              </button>
            );
          });
          TriggerElement.displayName = 'TriggerElement';

          return (
            <Tooltip.Root key={index}>
              <Tooltip.Trigger asChild>
                <TriggerElement />
              </Tooltip.Trigger>
              <Tooltip.Portal>
                <Tooltip.Content
                  className="z-50 max-h-[300px] overflow-y-auto custom-scrollbar max-w-[300px] px-3 py-2 text-xs font-medium text-on-surface bg-surface-container-high border border-outline-variant rounded-lg shadow-lg animate-in fade-in zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out data-[state=closed]:zoom-out-95 flex flex-col gap-2"
                  sideOffset={6}
                >
                  {validSources.map((srcItem, idx) => {
                    const info = srcItem.sourceText;
                    
                    let quoteText = "";
                    let rawSourceName = null;

                    if (typeof info === 'string') {
                      quoteText = info;
                    } else {
                      quoteText = info.exact_quote;
                      rawSourceName = info.source_name;
                    }

                    const isUrl = rawSourceName?.startsWith('http') || quoteText.startsWith('http');
                    
                    if (isUrl) {
                      const url = rawSourceName?.startsWith('http') ? rawSourceName : quoteText;
                      const displayTitle = rawSourceName?.startsWith('http') ? quoteText : rawSourceName;
                      return (
                        <a 
                          key={idx}
                          href={url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="flex gap-2 group/link"
                        >
                          <span className="text-primary font-bold min-w-max">[{srcItem.number}]</span>
                          <span className="text-primary group-hover/link:underline">{displayTitle || url}</span>
                        </a>
                      );
                    }
                    
                    const formatSourceName = (name: string) => {
                      if (!name) return name;
                      // e.g., META_10-Q_2026-Q2_0000320193.txt or META_10-K_FY2025_000.txt
                      const match = name.match(/_(10-[KQ])_?(FY\d{4}|\d{4}-Q\d)/i);
                      if (match) {
                        const form = match[1].replace('-', ''); // "10K" or "10Q"
                        const period = match[2].replace('FY', ''); // "2025" or "2026-Q2"
                        // For 10Q, we want "Q2-2026" instead of "2026-Q2"
                        if (period.includes('-Q')) {
                          const [year, q] = period.split('-');
                          return `${form} ${q}-${year}`;
                        }
                        return `${form} ${period}`;
                      }
                      return name;
                    };

                    const formattedSourceName = rawSourceName ? formatSourceName(rawSourceName) : null;

                    return (
                      <div key={idx} className="flex gap-2 flex-col mb-1 border-b border-black/30 dark:border-outline-variant/50 pb-2 last:border-0 last:pb-0">
                        <div className="flex gap-2">
                          <span className="text-primary font-bold min-w-max">[{srcItem.number}]</span>
                          {formattedSourceName && <span className="font-bold">{formattedSourceName}</span>}
                        </div>
                        <span className="italic">"{quoteText}"</span>
                      </div>
                    );
                  })}
                  <Tooltip.Arrow className="fill-surface-container-high" />
                </Tooltip.Content>
              </Tooltip.Portal>
            </Tooltip.Root>
          );
        })}
      </span>
    </Tooltip.Provider>
  );
}
