import React from 'react';
import * as Tooltip from '@radix-ui/react-tooltip';
import { useSources } from '@/common/contexts/SourcesContext';
import { type SourceInfo } from '@/common/types/valuation';

interface CitedTextProps {
  text: string;
  sources?: Record<string, SourceInfo>;
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
                  className="z-50 max-w-[300px] px-3 py-2 text-xs font-medium text-on-surface bg-surface-container-high border border-outline-variant rounded-lg shadow-lg animate-in fade-in zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out data-[state=closed]:zoom-out-95 flex flex-col gap-2"
                  sideOffset={6}
                >
                  {validSources.map((srcItem, idx) => {
                    const info = srcItem.sourceText;
                    
                    if (typeof info === 'string') {
                      return (
                        <div key={idx} className="flex gap-2">
                          <span className="text-primary font-bold min-w-max">[{srcItem.number}]</span>
                          <span>"{info}"</span>
                        </div>
                      );
                    }

                    const isUrl = info.url?.startsWith('http');
                    const displayTitle = info.title || (isUrl ? new URL(info.url).hostname : info.url);
                    
                    if (isUrl) {
                      return (
                        <a 
                          key={idx}
                          href={info.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="flex gap-2 group/link"
                        >
                          <span className="text-primary font-bold min-w-max">[{srcItem.number}]</span>
                          <span className="text-primary group-hover/link:underline">{displayTitle}</span>
                        </a>
                      );
                    }
                    
                    return (
                      <div key={idx} className="flex gap-2">
                        <span className="text-primary font-bold min-w-max">[{srcItem.number}]</span>
                        <span>"{displayTitle}"</span>
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
