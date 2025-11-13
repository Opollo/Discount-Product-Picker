
import React, { useState, useRef } from 'react';
import { PaperclipIcon, SendIcon, MicrophoneIcon, StopIcon, TrashIcon } from './icons';
import { MAX_FILE_SIZE_BYTES, ALLOWED_FILE_TYPES, MAX_FILE_SIZE_MB } from '../constants';

interface InputBarProps {
  onSendMessage: (text: string, file?: File) => void;
  onStartRecording: () => void;
  onStopRecording: () => void;
  isRecording: boolean;
  isLoading: boolean;
  attachedFile: File | null;
  setAttachedFile: (file: File | null) => void;
  setFileError: (error: string | null) => void;
}

const InputBar: React.FC<InputBarProps> = ({ 
    onSendMessage, onStartRecording, onStopRecording, isRecording, isLoading, 
    attachedFile, setAttachedFile, setFileError 
}) => {
  const [text, setText] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if ((text.trim() || attachedFile) && !isLoading) {
      onSendMessage(text.trim(), attachedFile || undefined);
      setText('');
      setAttachedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFileError(null);
      if (file.size > MAX_FILE_SIZE_BYTES) {
        setFileError(`File is too large. Maximum size is ${MAX_FILE_SIZE_MB}MB.`);
        return;
      }
      if (!ALLOWED_FILE_TYPES.includes(file.type)) {
        setFileError('Invalid file type. Please upload images, PDFs, or documents.');
        return;
      }
      setAttachedFile(file);
    }
  };

  return (
    <div className="bg-white border-t border-gray-200 p-3 sm:p-4">
        <div className="flex items-center bg-gray-100 rounded-full px-2 py-1">
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              onChange={handleFileChange}
              accept={ALLOWED_FILE_TYPES.join(',')}
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="p-2 text-gray-500 hover:text-blue-600 rounded-full hover:bg-gray-200 transition-colors disabled:opacity-50"
              disabled={isLoading || isRecording}
            >
              <PaperclipIcon className="h-6 w-6" />
            </button>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Type your message..."
              className="flex-1 bg-transparent px-3 py-2 text-gray-800 resize-none border-none focus:ring-0 outline-none"
              rows={1}
              disabled={isLoading || isRecording}
            />
            <button
                onClick={isRecording ? onStopRecording : onStartRecording}
                className={`p-2 rounded-full transition-colors disabled:opacity-50 ${isRecording ? 'text-red-500 bg-red-100' : 'text-gray-500 hover:text-blue-600 hover:bg-gray-200'}`}
                disabled={isLoading}
            >
                {isRecording ? <StopIcon className="h-6 w-6" /> : <MicrophoneIcon className="h-6 w-6" />}
            </button>
            <button
              onClick={handleSend}
              className="p-2 ml-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors disabled:bg-blue-300"
              disabled={(!text.trim() && !attachedFile) || isLoading || isRecording}
            >
              <SendIcon className="h-5 w-5" />
            </button>
        </div>
        {attachedFile && (
            <div className="mt-2 flex items-center justify-between text-sm bg-blue-50 border border-blue-200 text-blue-800 px-3 py-1.5 rounded-lg">
                <span className="truncate">{attachedFile.name}</span>
                <button onClick={() => { setAttachedFile(null); if (fileInputRef.current) fileInputRef.current.value = ''; }}>
                    <TrashIcon className="h-4 w-4 text-blue-600 hover:text-blue-800"/>
                </button>
            </div>
        )}
    </div>
  );
};

export default InputBar;
