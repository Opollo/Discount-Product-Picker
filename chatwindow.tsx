import React, { useRef, useEffect } from 'react';
import { Message } from '../types';
import MessageBubble from './MessageBubble';

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
  onFeedback: (messageId: string, feedback: 'up' | 'down') => void;
  onFeedbackText: (messageId: string, text: string) => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, isLoading, onFeedback, onFeedbackText }) => {
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex-1 p-4 md:p-6 overflow-y-auto">
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} onFeedback={onFeedback} onFeedbackText={onFeedbackText} />
      ))}
      {isLoading && (
        <div className="flex justify-start mb-4 animate-fade-in-up">
          <div className="max-w-xl px-4 py-3 rounded-xl shadow-md bg-white text-gray-800 rounded-bl-none">
            <div className="flex items-center space-x-2">
                <span className="text-gray-600 italic">Typing</span>
                <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"></div>
            </div>
          </div>
        </div>
      )}
      <div ref={endOfMessagesRef} />
    </div>
  );
};

export default ChatWindow;
