import { useState, useRef } from 'react';

interface PdfUploaderProps {
  onFileSelect: (file: File) => void;
  isUploading: boolean;
}

export function PdfUploader({ onFileSelect, isUploading }: PdfUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf') {
        onFileSelect(file);
      } else {
        alert('Please upload a PDF file.');
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      if (file.type === 'application/pdf') {
        onFileSelect(file);
      } else {
        alert('Please upload a PDF file.');
      }
    }
  };

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-10 flex flex-col items-center justify-center transition-colors text-center ${
        isDragging 
          ? 'border-primary bg-primary/5' 
          : 'border-outline-variant hover:border-outline bg-surface-container-low hover:bg-surface-container'
      } ${isUploading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
    >
      <input 
        type="file" 
        accept="application/pdf" 
        className="hidden" 
        ref={fileInputRef}
        onChange={handleFileChange}
      />
      <div className="w-16 h-16 rounded-full bg-surface-container-high flex items-center justify-center mb-4">
        <span className="material-symbols-outlined text-[32px] text-primary">upload_file</span>
      </div>
      <h3 className="text-header-sm font-bold text-on-surface mb-2">
        {isUploading ? 'Analyzing Document...' : 'Upload Earnings Report'}
      </h3>
      <p className="text-body-sm text-on-surface-variant max-w-md">
        {isUploading 
          ? 'Please wait while our AI engine extracts and analyzes the core fundamentals, capital allocation, and risk profile.'
          : 'Drag and drop a PDF file here (e.g., 10-K, 10-Q, Earnings Call Transcript), or click to browse your files.'}
      </p>
    </div>
  );
}
