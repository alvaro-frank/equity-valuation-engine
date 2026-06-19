import React from 'react';
import * as Tooltip from '@radix-ui/react-tooltip';
import { useSources } from '@/common/contexts/SourcesContext';

interface CitedTextProps {
  text: string;
  sources?: Record<string, string>;
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
                    const isUrl = srcItem.sourceText.startsWith('http');
                    const domain = isUrl ? new URL(srcItem.sourceText).hostname : srcItem.sourceText;
                    
                    if (isUrl) {
                      return (
                        <a 
                          key={idx}
                          href={srcItem.sourceText} 
                          target="_blank" 
                          rel="noreferrer" 
                          className="flex items-center gap-2 hover:text-primary transition-colors hover:underline cursor-pointer"
                        >
                          <span className="material-symbols-outlined text-[13px] text-primary shrink-0" style={{ fontVariationSettings: "'FILL' 1" }}>
                            link
                          </span>
                          <span className="opacity-90">{domain}</span>
                        </a>
                      );
                    }
                    
                    return (
                      <div key={idx} className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-[13px] text-primary shrink-0" style={{ fontVariationSettings: "'FILL' 1" }}>
                          article
                        </span>
                        <span className="opacity-90">{domain}</span>
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
