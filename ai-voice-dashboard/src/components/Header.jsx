import { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';

export default function Header() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [showHint, setShowHint] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowHint(true);
    }, 3000);
    return () => clearTimeout(timer);
  }, []);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setShowHint(false);
  };

  return (
    <header className="bg-gray-100 backdrop-blur-xl border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Left side of header (unchanged) */}
          <div className="flex items-center space-x-4">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-cyan-600 rounded-2xl blur opacity-20"></div>
              <div className="relative bg-gradient-to-r from-cyan-500 to-cyan-600 p-3 rounded-2xl">
                <PhoneIcon className="h-5 w-5 text-white" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-light bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                Joe's AI Voice Assistant Dashboard
              </h1>
              <p className="text-sm text-gray-500 font-normal">Real-time call monitoring</p>
            </div>
          </div>
          
          {/* Right side of header */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center bg-emerald-50 border border-emerald-200 px-4 py-2 rounded-full">
              <div className="relative">
                <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                <div className="absolute inset-0 w-2 h-2 bg-emerald-500 rounded-full animate-ping"></div>
              </div>
              <span className="ml-2 text-sm font-normal text-emerald-700">Connected</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function PhoneIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
    </svg>
  );
}

function SettingsIcon({ className = "h-4 w-4" }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}