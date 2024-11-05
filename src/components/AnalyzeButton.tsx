import React from 'react';
import { Search } from 'lucide-react';

interface AnalyzeButtonProps {
  onClick: () => void;
  disabled: boolean;
}

const AnalyzeButton = ({ onClick, disabled }: AnalyzeButtonProps) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        flex items-center justify-center space-x-2
        px-6 py-3 rounded-lg font-medium text-white
        transition-all duration-300
        ${disabled 
          ? 'bg-gray-300 cursor-not-allowed'
          : 'bg-gradient-swimbird hover:shadow-lg hover:-translate-y-0.5'
        }
      `}
    >
      <Search className="w-5 h-5" />
      <span>Analyze PDF</span>
    </button>
  );
};

export default AnalyzeButton;