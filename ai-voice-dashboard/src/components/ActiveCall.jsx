import { useRef, useEffect } from 'react';
import { jsPDF } from 'jspdf';
import { XIcon } from '@heroicons/react/solid';

function parseText(text) {
  // Bold (Text wrapped in **)
  const boldPattern = /\*\*(.*?)\*\*/g;
  text = text.replace(boldPattern, (match, content) => {
    return `<b>${content}</b>`;
  });

  // Italic (Text wrapped in *)
  const italicPattern = /\*(.*?)\*/g;
  text = text.replace(italicPattern, (match, content) => {
    return `<i>${content}</i>`;
  });

  // Medium Text (Text starting with ##)
  const MedTextPattern = /##(.*?)\n/g;
  text = text.replace(MedTextPattern, (match, content) => {
    return `<h2>${content}</h2>`;
  });

  // Large Text (Text starting with ###)
  const largeTextPattern = /###(.*?)\n/g;
  text = text.replace(largeTextPattern, (match, content) => {
    return `<h3>${content}</h3>`;
  });

  // Convert newlines to <br> for multi-line text
  text = text.replace(/\n/g, '<br/>');

  return text;
}

export default function ActiveCall({ call, onClose }) {
  const messagesEndRef = useRef(null);

  // Effect to scroll to the bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [call?.messages]); // Re-run when messages change

  // PDF Generation
  const generatePDF = (messages) => {
    const doc = new jsPDF();
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(12);
    doc.text('AI Voice assistant live conversation call logs details', 10, 10);

    let y = 20; // Initial y position for text
    const margin = 10;
    const pageWidth = doc.internal.pageSize.width;

    messages.forEach((msg) => {
      if (y > 270) {
        doc.addPage(); // Add a new page if the y position exceeds 270
        y = 10; // Reset y position to the top of the new page
      }

      // Determine max width based on the page size
      const maxWidth = pageWidth - 2 * margin;

      if (msg.speaker === 'user') {
        doc.setTextColor(0, 128, 0);  // Green for User
        doc.setFont('helvetica', 'bold');
        doc.text('Customer:', margin, y);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(0, 0, 0);  // Reset to black for text
        y += 10;

        // Wrap the text to avoid overflow
        const textLines = doc.splitTextToSize(msg.text, maxWidth);
        doc.text(textLines, margin, y);
        y += textLines.length * 5; // Adjust y based on text height
      } else {
        doc.setTextColor(0, 0, 255);  // Blue for Assistant
        doc.setFont('helvetica', 'bold');
        doc.text('Assistant:', margin, y);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(0, 0, 0);  // Reset to black for text
        y += 10;

        // Wrap the text to avoid overflow
        const textLines = doc.splitTextToSize(msg.text, maxWidth);
        doc.text(textLines, margin, y);
        y += textLines.length * 5; // Adjust y based on text height
      }

      y += 15; // Add some space between messages
    });

    doc.save('conversation.pdf');
  };

  const handleDownload = (e) => {
    e.stopPropagation(); // Prevent triggering onBack
    generatePDF(call.messages); // Call the generatePDF function
  };

  if (!call) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-12">
        <div className="relative mb-8">
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-cyan-600 rounded-full blur-xl opacity-20"></div>
          <div className="relative w-24 h-24 bg-gradient-to-r from-cyan-500 to-cyan-600 rounded-full flex items-center justify-center">
            <PhoneIcon className="h-12 w-12 text-white" />
          </div>
        </div>
        
        <h3 className="text-2xl font-light text-gray-900 mb-2">No Active Call</h3>
        <p className="text-gray-500 text-center max-w-md leading-relaxed font-normal">
          Select a call from the list to view live conversation details and real-time transcriptions.
        </p>
        
        <div className="mt-8 flex space-x-2">
          <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-50 to-white border-b border-gray-100 p-4 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-cyan-600 rounded-full flex items-center justify-center">
              <span className="text-white text-lg font-light">
                {call.From.slice(-2)}
              </span>
            </div>
            
            <div>
              <h2 className="text-xl font-light text-gray-900 flex items-center">
                {call.From}
                <StatusBadge status={call.status} className="ml-15" />
              </h2>
              <p className="text-sm text-gray-500 font-light">
                Call ID: {call.CallSid.slice(-8)}
              </p>
            </div>
          </div>
          
          {/* Close Button */}
          <button
            onClick={onClose}
            className="p-2 rounded-full hover:bg-gray-100 text-gray-500 transition-all duration-200"
            title="Close"
          >
            <XIcon className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full overflow-y-auto p-4">
          <div className="mx-auto" style={{ maxWidth: '800px' }}>
            {call.messages?.length > 0 ? (
              <div className="space-y-4">
                {call.messages.map((msg, index) => (
                  <div 
                    key={index}
                    className={`flex ${msg.speaker === 'user' ? 'justify-end' : 'justify-start'}`}
                    style={{ 
                      animation: `slideIn 0.5s ease-out ${index * 0.1}s both` 
                    }}
                  >
                    <div className={`max-w-[70%] ${
                        msg.speaker === 'user' 
                          ? 'bg-gradient-to-r from-cyan-50 to-cyan-100 text-cyan-900 border border-cyan-200'  
                          : 'bg-white border border-gray-100 shadow-sm'
                      } rounded-2xl p-4`}>
                      <div className="flex justify-between items-center text-xs font-light mb-2">
                        <span className="text-gray-500">
                          {msg.speaker === 'user' ? 'Customer' : 'AI Agent'}
                        </span>
                        <span>
                          {new Date(msg.timestamp).toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                      </div>

                      <div className="text-black leading-relaxed font-normal"
                        dangerouslySetInnerHTML={{ __html: parseText(msg.text) }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-gray-500">
                <div className="relative mb-6">
                  <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center">
                    <ChatIcon className="h-8 w-8 text-gray-400" />
                  </div>
                  <div className="absolute -top-1 -right-1 w-6 h-6 bg-gradient-to-r from-cyan-500 to-cyan-600 rounded-full flex items-center justify-center">
                    <div className="w-2 h-2 bg-white rounded-full animate-ping"></div>
                  </div>
                </div>
                <p className="text-lg font-light text-gray-600">Waiting for conversation...</p>
                <p className="text-sm text-gray-400 mt-1 font-light">Messages will appear here in real-time</p>
              </div>
            )}
            {/* The invisible element at the bottom to trigger the scroll */}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* Download Button */}
      <div className="p-4 border-t border-gray-100">
        <button
          onClick={handleDownload}
          className="w-full bg-cyan-600 text-white py-3 rounded-xl hover:bg-cyan-700 transition-all duration-200 flex items-center justify-center"
        >
          <DownloadIcon className="h-5 w-5 mr-2" />
          Download Conversation as PDF
        </button>
      </div>
    </div>
  );
}

// Icons
function PhoneIcon({ className = "h-6 w-6" }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
    </svg>
  );
}

function ChatIcon({ className = "h-8 w-8" }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
  );
}

// Download Icon
function DownloadIcon({ className = "h-4 w-4" }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8l-8 8-8-8" />
    </svg>
  );
}

// StatusBadge Component
function StatusBadge({ status, className = '' }) {
  const statusConfig = {
    ringing: {
      color: 'bg-cyan-100 text-cyan-800 border-cyan-200',
      text: 'Ringing',
      icon: '🔔',
      pulse: true,
    },
    in_progress: {
      color: 'bg-cyan-100 text-cyan-800 border-cyan-200',
      text: 'Active',
      icon: '🟢',
      pulse: true,
    },
    completed: {
      color: 'bg-cyan-100 text-cyan-800 border-cyan-200',
      text: 'Completed',
      icon: '✓',
      pulse: false,
    },
    failed: {
      color: 'bg-cyan-100 text-cyan-800 border-cyan-200',
      text: 'Failed',
      icon: '✗',
      pulse: false,
    },
  };

  const config = statusConfig[status] || statusConfig.ringing;

  return (
    <div
      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-normal border ${config.color} ${
        config.pulse ? 'animate-pulse' : ''
      } ${className}`}
    >
      <span className="mr-1">{config.icon}</span>
      {config.text}
    </div>
  );
}

// Inject animations
const styles = `
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

if (typeof document !== 'undefined') {
  const styleElement = document.createElement('style');
  styleElement.textContent = styles;
  document.head.appendChild(styleElement);
}