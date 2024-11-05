import React, { useState } from 'react';
import { toast } from 'sonner';
import Header from '@/components/Header';
import FileUpload from '@/components/FileUpload';
import AnalyzeButton from '@/components/AnalyzeButton';
import PDFPreview from '@/components/PDFPreview';
import DataTable from '@/components/DataTable';

const Index = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string>('');
  const [tablePositions, setTablePositions] = useState<Array<{ x: number, y: number, width: number, height: number }>>([]);
  const [tableData, setTableData] = useState<{ columns: string[], rows: any[][] } | null>(null);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPdfUrl(url);
    toast.success('PDF uploaded successfully!');
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setAnalyzing(true);
    toast.info('Analyzing PDF...');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:5000/analyze-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze PDF');
      }

      const data = await response.json();
      setTableData(data);
      setShowPreview(true);
      toast.success('Analysis complete! Table data extracted.');
    } catch (error) {
      toast.error('Error analyzing PDF');
      console.error('Error:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-swimbird-coral via-swimbird-orange to-swimbird-teal bg-clip-text text-transparent">
              PDF Table Analyzer
            </h1>
            <p className="text-gray-600">
              Upload your PDF and we'll extract table data into a structured format
            </p>
          </div>

          <FileUpload onFileSelect={handleFileSelect} />

          <div className="mt-8 flex justify-center">
            <AnalyzeButton
              onClick={handleAnalyze}
              disabled={!selectedFile || analyzing}
            />
          </div>

          {selectedFile && (
            <div className="mt-6 p-4 bg-white rounded-lg shadow-sm">
              <p className="text-sm text-gray-600">
                Selected file: <span className="font-medium">{selectedFile.name}</span>
              </p>
            </div>
          )}

          {tableData && (
            <div className="mt-8">
              <h2 className="text-2xl font-semibold mb-4">Extracted Table Data</h2>
              <DataTable data={tableData} />
            </div>
          )}

          <PDFPreview 
            isOpen={showPreview} 
            onClose={() => setShowPreview(false)} 
            pdfUrl={pdfUrl}
            tablePositions={tablePositions}
          />
        </div>
      </main>
    </div>
  );
};

export default Index;