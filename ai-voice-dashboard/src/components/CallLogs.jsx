import { useState } from 'react';
import { TrashIcon } from '@heroicons/react/solid';

export default function CallLogs({ calls, activeCallSid, onSelectCall, onClearLogs }) {
  // State to track which call is minimized (using a Set)
  const [minimizedCalls, setMinimizedCalls] = useState(new Set());

  const handleToggleSummary = (callSid) => {
    setMinimizedCalls(prev => {
      const newSet = new Set(prev);
      if (newSet.has(callSid)) {
        newSet.delete(callSid); // If already minimized, remove it
      } else {
        newSet.add(callSid); // Otherwise, add to the set
      }
      return newSet;
    });
  };

  return (
    <div className="w-96 h-full bg-white/95 backdrop-blur-xl border border-gray-100 rounded-3xl shadow-xl flex flex-col overflow-hidden relative">
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

      <div className="flex-1 overflow-y-auto">
        <div className="p-4 space-y-3">
          {calls.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 font-normal">No calls yet</p>
              <p className="text-sm text-gray-400 mt-1 font-light">Waiting for incoming calls...</p>
            </div>
          ) : (
            calls.map((call, index) => (
              <div
                key={call.CallSid}
                className={`group relative p-4 rounded-2xl cursor-pointer transition-all duration-300 transform hover:scale-[1.02] ${
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
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <div className="w-7 h-7 bg-gradient-to-r rounded-full flex items-center justify-center">
                        <PhoneIcon className="h-4 w-4 text-white" />
                      </div>
                      <div>
                        <div className="font-normal text-gray-900">{call.From}</div>
                        <div className="text-sm text-gray-500 font-light">To: {call.To}</div>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col items-end space-y-2">
                    <StatusBadge status={call.status} />
                    <div className="text-xs text-gray-400 font-light">
                      {new Date().toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </div>
                  </div>
                </div>

                {/* Call Summary Box */}
                {call.summary && (
                  <div className="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-lg shadow-sm">
                    <div className="flex justify-between items-center">
                      <h3 className="font-semibold text-gray-700">Call Summary</h3>
                      <button
                        onClick={() => handleToggleSummary(call.CallSid)}
                        className="text-gray-500 hover:text-gray-700 transition-all"
                      >
                        {minimizedCalls.has(call.CallSid) ? '+' : '-'}
                      </button>
                    </div>

                    {/* Show summary or just title based on minimized state */}
                    {!minimizedCalls.has(call.CallSid) ? (
                      <p className="text-sm text-gray-600 mt-2">{call.summary}</p>
                    ) : null}
                  </div>
                )}

                {activeCallSid === call.CallSid && (
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-cyan-500/10 to-cyan-600/10 pointer-events-none"></div>
                )}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Clear Logs Button - Positioned Bottom Right */}
      <div className="absolute bottom-4 right-4">
        <button
          onClick={onClearLogs}
          className="bg-cyan-600 p-3 rounded-full hover:bg-cyan-700 text-white transition-all duration-200"
          title="Clear Call Logs"
        >
          <TrashIcon className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}

// StatusBadge Component remains unchanged
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

// PhoneIcon remains unchanged
function PhoneIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
    </svg>
  );
}

const styles = `
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

  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
`;

// Inject styles
if (typeof document !== 'undefined') {
  const styleElement = document.createElement('style');
  styleElement.textContent = styles;
  document.head.appendChild(styleElement);
}