import React from 'react';
import { SpeakerOnIcon, SpeakerOffIcon, TrashIcon } from './icons';
import { UGANDA_COAT_OF_ARMS_URL } from '../constants';

interface HeaderProps {
  isTtsEnabled: boolean;
  onToggleTts: () => void;
  onClearChat: () => void;
}

const Header: React.FC<HeaderProps> = ({ isTtsEnabled, onToggleTts, onClearChat }) => {
  return (
    <header className="bg-white shadow-md p-3 flex justify-between items-center fixed top-0 left-0 right-0 z-10">
      <div className="flex items-center gap-3">
        <img src={UGANDA_COAT_OF_ARMS_URL} alt="Uganda Coat of Arms" className="h-12 w-auto" />
        <div>
          <h1 className="text-lg md:text-xl font-bold text-gray-800">Kole District Grievance System</h1>
          <p className="text-sm text-gray-500">Your AI Assistant: Kole Guide</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <button
          onClick={onToggleTts}
          className="p-2 rounded-full hover:bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
          aria-label={isTtsEnabled ? 'Disable text-to-speech' : 'Enable text-to-speech'}
        >
          {isTtsEnabled ? (
            <SpeakerOnIcon className="h-6 w-6 text-blue-600" />
          ) : (
            <SpeakerOffIcon className="h-6 w-6 text-gray-500" />
          )}
        </button>
        <button
          onClick={onClearChat}
          className="p-2 rounded-full hover:bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500"
          aria-label="Clear chat history"
        >
          <TrashIcon className="h-6 w-6 text-gray-500 hover:text-red-600" />
        </button>
      </div>
    </header>
  );
};

export default Header;
