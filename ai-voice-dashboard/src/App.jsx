import { useState, useEffect } from 'react';
import CallLogs from './components/CallLogs';
import ActiveCall from './components/ActiveCall';
import Header from './components/Header';
import { Toaster } from 'react-hot-toast';

function App() {
  const [activeCallSid, setActiveCallSid] = useState(null);
  const [calls, setCalls] = useState([]);
  const [ws, setWs] = useState(null);
  const [showSidebar, setShowSidebar] = useState(false);

  // Load saved calls from localStorage on page load
  useEffect(() => {
    const savedCalls = localStorage.getItem("call_logs");
    if (savedCalls) {
      setCalls(JSON.parse(savedCalls));
    }
  }, []);

  // Save calls to localStorage whenever they change
  useEffect(() => {
    if (calls.length > 0) {
      localStorage.setItem("call_logs", JSON.stringify(calls));
    }
  }, [calls]);

  const handleUpdateCallRemark = (callSid, remark) => {
  setCalls(prevCalls => {
    const updatedCalls = prevCalls.map(call => 
      call.CallSid === callSid ? { ...call, remark } : call
    );
    
    // Save to localStorage
    localStorage.setItem('callLogs', JSON.stringify(updatedCalls));
    
    return updatedCalls;
  });
};

  // Derive active call from calls array
  const activeCall = activeCallSid ? calls.find(call => call.CallSid === activeCallSid) : null;

  // Connect to WebSocket server
  const handleWebSocketMessage = (data) => {
    setCalls(prevCalls => {
      switch (data.type) {
        case 'incoming_call':
          // Check if call already exists
          if (prevCalls.some(call => call.CallSid === data.data.CallSid)) {
            return prevCalls;
          }
          return [data.data, ...prevCalls];

        case 'call_status':
          return prevCalls.map(call =>
            call.CallSid === data.data.CallSid
              ? { ...call, status: data.data.CallStatus }
              : call
          );

        case 'transcription':
        case 'ai_response':
          return prevCalls.map(call => {
            if (call.CallSid === data.data.call_sid) {
              const existingMessages = call.messages || [];
              const isDuplicate = existingMessages.some(msg =>
                msg.text === data.data.message &&
                msg.speaker === (data.type === 'transcription' ? 'user' : 'ai') &&
                Math.abs(msg.timestamp - Date.now()) < 1000 // Within 1 second
              );

              if (isDuplicate) {
                return call;
              }

              const isTranscription = data.type === 'transcription';
              const newMessage = {
                speaker: isTranscription ? 'user' : 'ai',
                text: data.data.message,
                timestamp: Date.now()
              };

              let messages = [...existingMessages];

              if (isTranscription && messages.length > 0 && messages[messages.length - 1].speaker === 'user') {
                messages[messages.length - 1] = newMessage;
              } else {
                messages.push(newMessage);
              }

              return {
                ...call,
                messages
              };
            }
            return call;
          });
          
        case 'call_summary':
          return prevCalls.map(call =>
            call.CallSid === data.data.CallSid
              ? { ...call, summary: data.data.summary }
              : call
          );

        default:
          console.log('Unknown message type:', data.type);
          return prevCalls;
      }
    });
  };

  useEffect(() => {
    if (!ws || ws.readyState === WebSocket.CLOSED) {
      const websocket = new WebSocket(`${import.meta.env.VITE_BACKEND_URL_WS}/frontend-updates`);
      console.log('Connecting to WebSocket server...', websocket);

      websocket.onopen = () => {
        console.log('Connected to WebSocket server');
        setWs(websocket);
      };

      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      };

      websocket.onclose = () => {
        console.log('WebSocket disconnected');
        setWs(null);
      };

      return () => {
        if (websocket.readyState === WebSocket.OPEN) {
          websocket.close();
        }
      };
    }
  }, [ws]);

  const clearCallLogs = () => {
    localStorage.removeItem("call_logs");
    setCalls([]);
  };

  const handleSelectCall = (call) => {
    setActiveCallSid(call.CallSid);
    setShowSidebar(true);
  };

  const handleCloseSidebar = () => {
    setShowSidebar(false);
    setActiveCallSid(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 via-white to-cyan-50/30 font-light">
      <Header />
      <Toaster position="top-right" reverseOrder={false} />
      <main className="flex flex-1 p-6 max-w-7xl mx-auto w-full h-[calc(100vh-6rem)]">
        <CallLogs
          calls={calls}
          activeCallSid={activeCallSid}
          onSelectCall={handleSelectCall}
          onClearLogs={clearCallLogs}
          onUpdateCallRemark={handleUpdateCallRemark}
          sidebarOpen={showSidebar}
          className="z-20"
        />
        
        {/* Active Call Sidebar */}
        <div className={`fixed top-0 right-0 h-full w-96 bg-white/95 backdrop-blur-sm border-l border-gray-200 shadow-xl transform transition-transform duration-300 z-50 ${
          showSidebar ? 'translate-x-0' : 'translate-x-full'
        }`}>
          <ActiveCall
            call={activeCall}
            onClose={handleCloseSidebar}
          />
        </div>
        
        {/* Semi-transparent overlay when sidebar is open */}
        {showSidebar && (
          <div 
            className="fixed inset-0 bg-gray-900/10 backdrop-blur-sm z-40"
            onClick={handleCloseSidebar}
          />
        )}
      </main>
    </div>
  );
}

export default App;