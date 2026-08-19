import type { TranscriptStatement } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';

interface TranscriptViewProps {
  transcript: TranscriptStatement[];
}

type SpeakerRole = 'management' | 'analyst' | 'operator';

function getSpeakerRole(title: string): SpeakerRole {
  const lowerTitle = title.toLowerCase();
  if (lowerTitle.includes('operator')) return 'operator';
  if (lowerTitle.includes('analyst') || lowerTitle.includes('research')) return 'analyst';
  // Default to management (CEO, CFO, IR, etc)
  return 'management';
}

export function TranscriptView({ transcript }: TranscriptViewProps) {
  const { t } = useTranslation();

  if (!transcript || transcript.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-on-surface-variant/50">
        <span className="material-symbols-outlined text-4xl mb-4 opacity-50">
          speaker_notes_off
        </span>
        <p className="text-sm font-medium">No transcript available for this period</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col animate-in fade-in duration-500">
      <div className="w-full">
        <div className="space-y-6 md:space-y-8">
          {transcript.filter(s => getSpeakerRole(s.title) !== 'operator').map((statement, idx) => {
            const role = getSpeakerRole(statement.title);
            const isOperator = role === 'operator';
            const isManagement = role === 'management';
            const isRightAligned = !isManagement; // Analysts and Operators on the right
            
            // Avatar Colors
            const avatarClasses = isOperator
              ? "w-10 h-10 rounded-full flex items-center justify-center border border-outline/30 bg-surface-container text-on-surface-variant/50 flex-shrink-0"
              : isManagement
              ? "w-10 h-10 rounded-full flex items-center justify-center bg-primary text-on-primary ring-4 ring-background shadow-sm flex-shrink-0"
              : "w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-high border border-outline-variant text-on-surface flex-shrink-0";

            // Badge Colors
            const badgeClasses = isOperator
              ? "text-[10px] font-semibold text-on-surface-variant/50 uppercase tracking-widest"
              : isManagement
              ? "bg-primary/10 border border-primary/20 text-primary text-[11px] font-bold px-2 py-0.5 rounded uppercase tracking-wider"
              : "bg-surface-container border border-outline-variant text-on-surface-variant text-[11px] font-bold px-2 py-0.5 rounded uppercase tracking-wider";

            // Text Styles
            const textClasses = isOperator
              ? "text-on-surface-variant/60 text-sm italic leading-relaxed tracking-normal"
              : "text-on-surface text-[15px] leading-relaxed whitespace-pre-wrap tracking-normal";

            // Initials
            const initials = statement.speaker.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

            return (
              <div 
                key={idx} 
                className={`flex gap-3 md:gap-4 w-full ${isRightAligned ? 'flex-row-reverse' : 'flex-row'}`}
              >
                <div className={avatarClasses}>
                  <span className="font-bold text-sm tracking-wider">
                    {initials}
                  </span>
                </div>
                
                <div className={`flex flex-col max-w-[95%] md:max-w-[85%] ${isRightAligned ? 'items-end' : 'items-start'}`}>
                  <div className={`flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3 mb-2 px-1 ${isRightAligned ? 'sm:flex-row-reverse' : ''}`}>
                    <span className={`font-semibold ${isOperator ? 'text-on-surface-variant/70' : 'text-on-surface'} text-base`}>
                      {statement.speaker}
                    </span>
                    <span className={badgeClasses}>
                      {statement.title}
                    </span>
                  </div>
                  
                  <div className={`p-4 md:p-5 rounded-sm max-h-[175px] overflow-y-auto custom-scrollbar ${
                    isManagement ? 'bg-primary/5 border border-primary/20' : 
                    'bg-surface-container-low border border-outline-variant/50'
                  }`}>
                    <p className={`${textClasses} ${isRightAligned && isOperator ? 'text-right' : 'text-left'}`}>
                      {statement.content}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
