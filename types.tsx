
export type Sender = 'user' | 'ai';

export type Message = {
  id: string;
  text: string;
  sender: Sender;
  file?: {
    name: string;
    type: string;
  };
  feedback?: 'up' | 'down';
  feedbackText?: string;
};

export enum ConversationStage {
  AWAITING_TITLE,
  AWAITING_GRIEVANCE_DESCRIPTION,
  AWAITING_CATEGORY_CONFIRMATION,
  AWAITING_EVIDENCE,
  AWAITING_SUMMARY_CONFIRMATION,
  FINALIZED,
}
