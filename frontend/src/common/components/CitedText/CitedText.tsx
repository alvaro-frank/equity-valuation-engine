import * as Tooltip from '@radix-ui/react-tooltip';

interface CitedTextProps {
  text: string;
  sources?: Record<string, string>;
}

export function CitedText({ text, sources }: CitedTextProps) {
  if (!text) return null;
  if (!sources || Object.keys(sources).length === 0) {
    return <span>{text}</span>;
  }

  // Split text by citations like [1], [2]
  // Capturing group ensures numbers are kept in the resulting array at odd indices
  const parts = text.split(/\[(\d+)\]/g);

  return (
    <Tooltip.Provider delayDuration={150}>
      <span className="leading-relaxed">
        {parts.map((part, index) => {
          // Even indices are regular text
          if (index % 2 === 0) {
            return <span key={index}>{part}</span>;
          }

          // Odd indices are the captured numbers from [1]
          const sourceText = sources[part];
          if (!sourceText) {
            // If there's no matching source, render nothing (clean text)
            return null;
          }

          return (
            <Tooltip.Root key={index}>
              <Tooltip.Trigger asChild>
                <button
                  className="inline-flex items-center justify-center w-[16px] h-[16px] mx-0.5 align-text-top text-primary/60 hover:text-primary hover:bg-primary/10 rounded cursor-help transition-all duration-150"
                  aria-label={`Fonte: ${sourceText}`}
                >
                  <span className="material-symbols-outlined" style={{ fontSize: '13px', fontVariationSettings: "'FILL' 0, 'wght' 400" }}>
                    format_quote
                  </span>
                </button>
              </Tooltip.Trigger>
              <Tooltip.Portal>
                <Tooltip.Content
                  className="z-50 max-w-[300px] px-3 py-2 text-xs font-medium text-surface bg-on-surface rounded-lg shadow-lg animate-in fade-in zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out data-[state=closed]:zoom-out-95"
                  sideOffset={6}
                >
                  <div className="flex items-start gap-2">
                    <span className="material-symbols-outlined text-[13px] text-primary mt-0.5 shrink-0" style={{ fontVariationSettings: "'FILL' 1" }}>
                      article
                    </span>
                    <span className="opacity-90">{sourceText}</span>
                  </div>
                  <Tooltip.Arrow className="fill-on-surface" />
                </Tooltip.Content>
              </Tooltip.Portal>
            </Tooltip.Root>
          );
        })}
      </span>
    </Tooltip.Provider>
  );
}
