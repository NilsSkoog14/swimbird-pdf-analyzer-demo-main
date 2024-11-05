import React, { useEffect, useRef } from 'react';
import { Dialog, DialogContent } from '@/components/ui/dialog';

interface PDFPreviewProps {
  isOpen: boolean;
  onClose: () => void;
  pdfUrl: string;
  tablePositions?: Array<{ x: number, y: number, width: number, height: number }>;
}

const PDFPreview = ({ isOpen, onClose, pdfUrl, tablePositions = [] }: PDFPreviewProps) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen && containerRef.current) {
      // Add table markers
      tablePositions.forEach(({ x, y, width, height }) => {
        const marker = document.createElement('div');
        marker.style.position = 'absolute';
        marker.style.left = `${x}px`;
        marker.style.top = `${y}px`;
        marker.style.width = `${width}px`;
        marker.style.height = `${height}px`;
        marker.style.border = '2px solid red';
        marker.style.pointerEvents = 'none';
        containerRef.current?.appendChild(marker);
      });
    }
  }, [isOpen, tablePositions]);

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl w-[90vw] h-[80vh]">
        <div ref={containerRef} className="w-full h-full relative">
          <iframe
            src={pdfUrl + '#toolbar=0'}
            className="w-full h-full border-0"
            title="PDF Preview"
          />
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default PDFPreview;