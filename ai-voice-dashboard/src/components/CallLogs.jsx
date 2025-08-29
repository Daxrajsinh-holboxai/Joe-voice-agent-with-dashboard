import { useState, useEffect } from 'react';
import { TrashIcon, ChevronDownIcon, ChevronUpIcon, ChatIcon, ChatAlt2Icon } from '@heroicons/react/solid';

export default function CallLogs({ calls, activeCallSid, onSelectCall, onClearLogs, sidebarOpen, onUpdateCallRemark }) {
  const [expandedSummaries, setExpandedSummaries] = useState(new Set());
  const [expandedRemarks, setExpandedRemarks] = useState(new Set());
  const [remarkTexts, setRemarkTexts] = useState({});
  const [summaries, setSummaries] = useState({}); // Store summaries separately to display only the summary content
  const [customerNames, setCustomerNames] = useState({}); // Store customer names for each call

  const handleToggleSummary = (callSid, e) => {
    e.stopPropagation();
    setExpandedSummaries(prev => {
      const newSet = new Set(prev);
      if (newSet.has(callSid)) {
        newSet.delete(callSid);
      } else {
        newSet.add(callSid);
      }
      return newSet;
    });
  };

  const handleToggleRemark = (callSid, e) => {
    e.stopPropagation();
    setExpandedRemarks(prev => {
      const newSet = new Set(prev);
      if (newSet.has(callSid)) {
        newSet.delete(callSid);
      } else {
        newSet.add(callSid);
        // Initialize the remark text when opening editor
        if (!remarkTexts[callSid]) {
          const call = calls.find(c => c.CallSid === callSid);
          setRemarkTexts(prev => ({
            ...prev,
            [callSid]: call.remark || ''
          }));
        }
      }
      return newSet;
    });
  };

  const handleSaveRemark = (callSid, remark) => {
    if (onUpdateCallRemark) {
      onUpdateCallRemark(callSid, remark);
    }
    setExpandedRemarks(prev => {
      const newSet = new Set(prev);
      newSet.delete(callSid);
      return newSet;
    });
  };

  const handleRemarkChange = (callSid, text) => {
    setRemarkTexts(prev => ({
      ...prev,
      [callSid]: text
    }));
  };

  const handleClearRemark = (callSid) => {
    // Clear the local state
    setRemarkTexts(prev => ({
      ...prev,
      [callSid]: ''  // Reset the remark for the specific callSid
    }));

    // Also update the actual call data
    if (onUpdateCallRemark) {
      onUpdateCallRemark(callSid, '');
    }
  };

  // Update customer names and summaries when summary is generated
  const updateCustomerName = (callSid, name) => {
    setCustomerNames(prev => ({
      ...prev,
      [callSid]: name,
    }));
  };

  const updateSummary = (callSid, summary) => {
    setSummaries(prev => ({
      ...prev,
      [callSid]: summary,
    }));
  };

  useEffect(() => {
    // Whenever calls change, we can update customer names and summaries (if provided)
    calls.forEach((call) => {
      if (call.summary && !customerNames[call.CallSid]) {
        // Parse the summary JSON and extract the customer name
        try {
          const parsedSummary = JSON.parse(call.summary); // Assuming summary is in JSON format as shown
          if (parsedSummary && parsedSummary.cust_name) {
            // Update customer name in the state
            updateCustomerName(call.CallSid, parsedSummary.cust_name);
            // Update summary content to display only summary (without cust_name)
            updateSummary(call.CallSid, parsedSummary.summary);
          }
        } catch (error) {
          console.error('Error parsing summary:', error);
        }
      }
    });
  }, [calls, customerNames]);

  return (
    <div
      className={`w-full h-full bg-white/80 backdrop-blur-sm border border-gray-100 rounded-3xl shadow-xl flex flex-col overflow-hidden relative transition-all duration-300 ${
        sidebarOpen ? 'mr-96 opacity-100' : 'mr-0'
      }`}
    >
      <div className="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-lg font-light text-gray-900">Recent Calls</h2>
            <p className="text-sm text-gray-500 mt-1 font-normal">Live call monitoring</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="bg-cyan-50 text-cyan-700 px-3 py-1 rounded-full text-sm font-normal">
              {calls.length}
            </div>
            <div className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {calls.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 font-normal">No calls yet</p>
            <p className="text-sm text-gray-400 mt-1 font-light">Waiting for incoming calls...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {calls.map((call, index) => (
              <div
                key={call.CallSid}
                className={`group relative p-4 rounded-2xl cursor-pointer transition-all duration-300 ${
                  activeCallSid === call.CallSid
                    ? 'bg-gradient-to-r from-cyan-50 to-cyan-50 border-2 border-cyan-200 shadow-lg'
                    : 'bg-gray-50/50 hover:bg-white hover:shadow-md border border-gray-100'
                }`}
                onClick={() => onSelectCall(call)}
                style={{
                  animationDelay: `${index * 100}ms`,
                  animation: 'fadeInUp 0.5s ease-out forwards',
                }}
              >
                <div className="flex items-center justify-between">
                  {/* Left side: Caller info */}
                  <div className="flex items-center space-x-3 flex-shrink-0">
                    <div className="w-6 h-6 bg-gradient-to-r from-cyan-500 to-cyan-600 rounded-full flex items-center justify-center">
                      <PhoneIcon className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      {/* Display updated customer name */}
                      <div className="font-normal text-gray-900">{customerNames[call.CallSid] || call.From}</div> {/* Using the updated customer name */}
                      <div className="text-sm text-gray-500 font-light">To: {call.To}</div>
                    </div>
                  </div>

                  {/* Call summary section */}
                  <div className="mx-34 flex-1 relative min-w-19 flex">
                    {/* Left: Call Summary Card */}
                    {call.summary && (
                      <div
                        className="bg-gray-50 border border-gray-200 rounded-lg p-2 cursor-pointer mr-4 w-5/7"
                        onClick={(e) => handleToggleSummary(call.CallSid, e)}
                      >
                        <div className="flex justify-between items-center">
                          <h3 className="font-semibold text-gray-700 text-xs">Summary</h3>
                          <button
                            onClick={(e) => e.stopPropagation()}
                            className="text-gray-500 hover:text-gray-700 transition-all flex items-center text-xs"
                          >
                            {expandedSummaries.has(call.CallSid) ? (
                              <ChevronUpIcon className="h-3 w-3" />
                            ) : (
                              <ChevronDownIcon className="h-3 w-3" />
                            )}
                          </button>
                        </div>

                        {/* Expandable summary content */}
                        {expandedSummaries.has(call.CallSid) && (
                          <div className="mt-1 p-2 bg-gray-50 border border-gray-200 rounded-lg">
                            <p className="text-xs text-gray-600">{summaries[call.CallSid]}</p> {/* Display only the summary */}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Right: Call Remarks Card */}
                    <div className="w-2/7 flex-shrink-0">
                      {/* Remaining code for remarks goes here... */}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Clear Logs Button */}
      <div className="absolute bottom-4 right-4">
        <button
          onClick={onClearLogs}
          className="bg-cyan-600 p-3 rounded-full hover:bg-cyan-700 text-white transition-all duration-200"
          title="Clear Call Logs"
        >
          <TrashIcon className="h-4 w-4" />
        </button>
      </div>

      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}

// Updated Remark Editor with Clear functionality
function RemarkEditor({ call, remarkText, onRemarkChange, onSave, onCancel, onClear }) {
  const handleButtonClick = (e) => {
    e.stopPropagation();
  };

  const handleClear = (e) => {
    handleButtonClick(e);
    onClear(); // This should call handleClearRemark which now updates both local state and actual data
  };

  return (
    <div className="space-y-2">
      <textarea
        value={remarkText}
        onChange={(e) => onRemarkChange(e.target.value)}
        placeholder="Add your remarks about this call..."
        className="w-full h-20 p-2 text-sm border border-gray-300 rounded-md focus:ring-cyan-500 focus:border-cyan-500"
        onClick={handleButtonClick}
      />
      <div className="flex justify-between">
        <button
          onClick={handleClear}
          className="px-3 py-1 text-xs text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md"
        >
          Clear
        </button>
        <div className="flex space-x-2">
          <button
            onClick={(e) => {
              handleButtonClick(e);
              onCancel();
            }}
            className="px-3 py-1 text-xs text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md"
          >
            Cancel
          </button>
          <button
            onClick={(e) => {
              handleButtonClick(e);
              onSave();
            }}
            className="px-3 py-1 text-xs bg-cyan-600 text-white rounded-md hover:bg-cyan-700"
          >
            Save
          </button>
        </div>
      </div>
    </div>
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
      className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-normal border ${config.color} ${
        config.pulse ? 'animate-pulse' : ''
      } ${className}`}
    >
      <span className="mr-1 text-xs">{config.icon}</span>
      {config.text}
    </div>
  );
}

// PhoneIcon
function PhoneIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
    </svg>
  );
}

// RightArrowIcon
function RightArrowIcon({ className = "h-4 w-4" }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10 6l6 6-6 6" />
    </svg>
  );
}