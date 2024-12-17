import React from 'react';

interface ChatMessage {
  type: 'user' | 'system';
  content: any;
}

interface ChatProps {
  messages: ChatMessage[];
}

const Chat: React.FC<ChatProps> = ({ messages }) => {
  const renderMessage = (message: ChatMessage) => {
    if (message.type === 'user') {
      return (
        <div className="flex justify-end mb-4">
          <div className="bg-blue-500 text-white rounded-lg py-2 px-4 max-w-[70%]">
            <pre className="whitespace-pre-wrap font-sans">
              {typeof message.content === 'string'
                ? message.content
                : JSON.stringify(message.content, null, 2)}
            </pre>
          </div>
        </div>
      );
    } else {
      return (
        <div className="flex justify-start mb-4">
          <div className="bg-gray-200 rounded-lg py-2 px-4 max-w-[70%]">
            <pre className="whitespace-pre-wrap font-sans">
              {typeof message.content === 'string'
                ? message.content
                : JSON.stringify(message.content, null, 2)}
            </pre>
          </div>
        </div>
      );
    }
  };

  return (
    <div className="h-[400px] overflow-y-auto p-4 bg-white rounded-lg shadow">
      {messages.map((message, index) => (
        <div key={index}>{renderMessage(message)}</div>
      ))}
    </div>
  );
};

export default Chat; 