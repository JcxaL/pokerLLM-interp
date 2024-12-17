import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

// API base URL configuration
const API_BASE_URL = 'http://localhost:8000';  // 或者您的实际后端URL

interface Message {
  text: string;
  type: 'user' | 'bot';
  timestamp: Date;
  gameState?: GameState;
}

interface GameState {
  position?: string;
  stage?: string;
  stack_size?: number;
  board_cards?: Array<{ rank: string; suit: string }>;
  player_cards?: Array<{ rank: string; suit: string }>;
}

interface ChatInterfaceProps {
  gameState?: GameState;
  modelParams?: {
    model_id: string;
    temperature: number;
    max_tokens: number;
    top_p: number;
    frequency_penalty: number;
    presence_penalty: number;
  };
}

const formatCard = (card: { rank: string; suit: string }) => `${card.rank}${card.suit}`;

const formatGameState = (state: GameState): string => {
  const parts = [];
  
  if (state.position) parts.push(`Position: ${state.position}`);
  if (state.stage) parts.push(`Stage: ${state.stage}`);
  if (state.stack_size) parts.push(`Stack: ${state.stack_size}BB`);
  
  if (state.player_cards && state.player_cards.length > 0) {
    parts.push(`Hand: ${state.player_cards.map(formatCard).join(' ')}`);
  }
  
  if (state.board_cards && state.board_cards.length > 0) {
    parts.push(`Board: ${state.board_cards.map(formatCard).join(' ')}`);
  }
  
  return parts.join(' | ');
};

const hasValidGameState = (state?: GameState): boolean => {
  if (!state) return false;
  return !!(
    state.position ||
    state.stage ||
    state.stack_size ||
    (state.player_cards && state.player_cards.length > 0) ||
    (state.board_cards && state.board_cards.length > 0)
  );
};

const formatMessage = (text: string): string => {
  // 将常见的策略格式转换为 Markdown
  let formattedText = text;

  // 处理百分比和频率
  formattedText = formattedText.replace(
    /(\d+(?:-\d+)?%)/g,
    '**$1**'
  );

  // 处理标题
  formattedText = formattedText.replace(
    /((?:^|\n)[\w\s]+:)(?!\n)/g,
    '\n### $1'
  );

  // 处理列表项
  formattedText = formattedText.replace(
    /(?:^|\n)- /g,
    '\n• '
  );

  // 处理重要提示
  formattedText = formattedText.replace(
    /(Remember:|Note:|Important:)/g,
    '**$1**'
  );

  // 处理动作和决策
  formattedText = formattedText.replace(
    /(Bet|Call|Fold|Raise|Check)(?=[\s:])/g,
    '**$1**'
  );

  return formattedText;
};

const ChatInterface: React.FC<ChatInterfaceProps> = ({ gameState, modelParams }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    let userMessageText = inputMessage;
    if (hasValidGameState(gameState)) {
      userMessageText = `${inputMessage}\n\nGame State: ${formatGameState(gameState)}`;
    }

    const userMessage: Message = {
      text: userMessageText,
      type: 'user',
      timestamp: new Date(),
      gameState: gameState
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: userMessageText,
        game_state: gameState || null,
        model_params: modelParams || null
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.data.success) {
        const botMessage: Message = {
          text: response.data.data.message,
          type: 'bot',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        throw new Error(response.data.error);
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        text: error instanceof Error 
          ? `Error: ${error.message}. Please check if the backend server is running.`
          : 'Sorry, I encountered an error. Please try again.',
        type: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-4">
      {/* 显示当前游戏状态 */}
      {hasValidGameState(gameState) && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg text-sm text-gray-600">
          <div className="font-medium mb-1">Current Game State:</div>
          <div>{formatGameState(gameState)}</div>
        </div>
      )}
      
      <div className="h-96 overflow-y-auto mb-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.type === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[70%] rounded-lg px-4 py-2 ${
                message.type === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              {message.type === 'bot' ? (
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown>
                    {formatMessage(message.text)}
                  </ReactMarkdown>
                </div>
              ) : (
                <p className="text-sm whitespace-pre-wrap">{message.text}</p>
              )}
              <p className="text-xs mt-1 opacity-70">
                {message.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-2">
              <p className="text-gray-500">Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask for poker advice..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          disabled={isLoading}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface; 