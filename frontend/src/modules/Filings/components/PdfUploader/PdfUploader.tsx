import { useTranslation } from 'react-i18next';
import { usePdfUploader } from './usePdfUploader';

interface PdfUploaderProps {
  onFileSelect: (file: File) => void;
  isUploading: boolean;
}

export function PdfUploader({ onFileSelect, isUploading }: PdfUploaderProps) {
  const { t } = useTranslation();
  
  const {
    isDragging,
    error,
    fileInputRef,
    handleDragOver,
    handleDragLeave,
    handleDrop,
    handleFileChange
  } = usePdfUploader(onFileSelect);

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-10 flex flex-col items-center justify-center transition-colors text-center ${
        isDragging 
          ? 'border-primary bg-primary/5' 
          : 'border-outline-variant hover:border-outline bg-surface-container-low hover:bg-surface-container'
      } ${isUploading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'} ${error ? 'border-error bg-error/5' : ''}`}
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
      <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-4 transition-colors ${error ? 'bg-error/10 text-error' : 'bg-surface-container-high text-primary'}`}>
        <span className="material-symbols-outlined text-[32px]">
          {error ? 'error' : 'upload_file'}
        </span>
      </div>
      
      <h3 className={`text-header-sm font-bold mb-2 ${error ? 'text-error' : 'text-on-surface'}`}>
        {error ? t('pdf_uploader.invalid_pdf') : (isUploading ? t('pdf_uploader.uploading') : t('pdf_uploader.title'))}
      </h3>
      
      <p className="text-body-sm text-on-surface-variant max-w-md">
        {isUploading 
          ? t('pdf_uploader.extracting')
          : t('pdf_uploader.desc')}
      </p>
    </div>
  );
}
