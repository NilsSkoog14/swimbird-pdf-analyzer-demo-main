import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className="w-full py-4 px-6 bg-white shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center cursor-pointer" onClick={() => navigate('/')}>
          <img 
            src="/swimbird-logo.svg" 
            alt="Swimbird Logo" 
            className="h-12 w-auto" 
          />
        </div>
        <div className="text-2xl font-semibold bg-gradient-to-r from-swimbird-coral via-swimbird-orange to-swimbird-teal bg-clip-text text-transparent">
          Demo
        </div>
      </div>
    </header>
  );
};

export default Header;