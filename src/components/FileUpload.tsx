import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileType, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

const FileUpload = ({ onFileSelect }: { onFileSelect: (file: File) => void }) => {
  const [isDragging, setIsDragging] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file?.type !== 'application/pdf') {
      toast.error('Please upload a PDF file');
      return;
    }
    onFileSelect(file);
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: false,
  });

  return (
    <div
      {...getRootProps()}
      className={`
        w-full max-w-2xl mx-auto mt-8 p-8 rounded-xl border-2 border-dashed
        transition-all duration-300 ease-in-out cursor-pointer
        hover:border-swimbird-teal
        ${isDragActive ? 'border-swimbird-teal bg-swimbird-teal/5' : 'border-gray-300'}
      `}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center justify-center space-y-4">
        <Upload className="w-12 h-12 text-swimbird-coral animate-float" />
        <div className="text-center">
          <p className="text-lg font-medium">
            Drop your PDF here, or <span className="text-swimbird-coral">browse</span>
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Supports: PDF files
          </p>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;