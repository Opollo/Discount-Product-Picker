
import { GoogleGenAI, Part } from "@google/genai";
import { Message, ConversationStage } from '../types';

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });

const systemInstruction = `You are 'Kole Guide', an AI assistant for the Kole District Local Government in Uganda. Your persona is professional, empathetic, and helpful. Your purpose is to guide district employees through the official grievance reporting process. Your knowledge is strictly limited to the following three documents: 1. The Uganda Government Standing Orders. 2. The 'Job Descriptions and Specifications for Jobs in Local Governments, 2011'. 3. The 'Staff Performance Appraisal Form for the Public Service (PS FORM 5)'. You must adhere to a strict conversational flow. Do not deviate. When asked for guidance on a grievance, you must reference the specific section of the Standing Orders. When asked about job roles or reporting lines, you must reference the Job Descriptions document. Do not provide information outside of these documents. Do not offer legal advice. Your goal is to help the user structure and summarize their grievance for formal submission.`;

const getCategorizationPrompt = (grievance: string): string => `
The user described their grievance as: "${grievance}". 
Based on this, which of the following categories best fits? You may suggest one or two if applicable.
- Working Conditions
- Harassment
- Unfair Treatment
- Compensation or Salary
- Job Description
- Performance Appraisal
Please respond only with the suggested categories and a brief sentence asking the user to confirm.
`;

const getGuidancePrompt = (category: string): string => `
The user has confirmed their grievance category is: "${category}".
In a single response, you must do two things in order:
1. Provide a specific reference to the relevant section of the Uganda Government Standing Orders that covers this category.
2. Ask a targeted question to prompt the user for evidence. This part of the response MUST begin with the special marker [EVIDENCE_PROMPT:${category}]. For example: "[EVIDENCE_PROMPT:Unfair Treatment]To properly document your case..."
`;

const getSummaryPrompt = (chatHistory: string): string => `
Based on the provided conversation history, generate a final, structured summary for the user to review. The summary must be in Markdown format and include these sections:
- **Grievance Summary**
- **Category:** [The confirmed category]
- **Key Details:** [A concise summary of the issue described by the user]
- **Evidence to Include:** [A list of the evidence types the user mentioned or was prompted to provide]

After the summary, you must ask: "Please review this summary. Does it accurately capture the main points of your grievance before you proceed with the formal process?"
Conversation History:
${chatHistory}
`;

const getFinalConfirmationPrompt = (): string => `
The user has confirmed the summary is correct.
Your final response MUST be: "Thank you for confirming. You can now use this summary to formally document your grievance. [ACTION:FINALIZE_GRIEVANCE]"
Do not add any other text.
`;

const getJobDescriptionPrompt = (chatHistory: string): string => `
Based on the "Job Descriptions and Specifications for Jobs in Local Governments, 2011" document and the provided conversation history, answer the user's query about their job role, key functions, or supervisor. If listing a supervisory chain from "Reports to", present it as a numbered list.
Conversation History:
${chatHistory}
`;

export const transcribeAudio = async (audioBase64: string, mimeType: string): Promise<string> => {
    const audioPart = { inlineData: { data: audioBase64, mimeType } };
    const textPart = { text: "Transcribe this audio recording precisely." };
    const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: { parts: [audioPart, textPart] },
    });
    return response.text.trim();
};

export const getAiResponse = async (
    history: Message[],
    stage: ConversationStage,
    userInput: string,
    fileParts: Part[] = []
): Promise<string> => {
    let prompt = userInput;
    const model = 'gemini-2.5-pro';

    const fullHistoryText = history.map(m => `${m.sender}: ${m.text}`).join('\n');

    if (/(job|role|supervisor|boss|reports to|key functions)/i.test(userInput)) {
        prompt = getJobDescriptionPrompt(fullHistoryText + `\nuser: ${userInput}`);
    } else {
        switch (stage) {
            case ConversationStage.AWAITING_GRIEVANCE_DESCRIPTION:
                prompt = "Thank you for confirming your position. How can I help you today?";
                return prompt; // This is a canned response, no API call needed.
            case ConversationStage.AWAITING_CATEGORY_CONFIRMATION:
                prompt = getCategorizationPrompt(userInput);
                break;
            case ConversationStage.AWAITING_EVIDENCE:
                prompt = getGuidancePrompt(userInput);
                break;
            case ConversationStage.AWAITING_SUMMARY_CONFIRMATION:
                prompt = getSummaryPrompt(fullHistoryText + `\nuser: ${userInput}`);
                break;
             case ConversationStage.FINALIZED:
                if (userInput.toLowerCase().startsWith('yes') || userInput.toLowerCase().startsWith('correct')) {
                    prompt = getFinalConfirmationPrompt();
                } else {
                    prompt = "I understand. Please provide any corrections or additional details, and I will generate a new summary for you.";
                }
                break;
        }
    }

    // FIX: Explicitly type `contents` to prevent a TypeScript error when pushing userParts with file data.
    const contents: {role: string, parts: Part[]}[] = history.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'model',
        parts: [{ text: msg.text }]
    }));

    const userParts: Part[] = [{ text: prompt }, ...fileParts];
    contents.push({ role: 'user', parts: userParts });

    const response = await ai.models.generateContent({
        model,
        contents,
        config: { systemInstruction },
    });
    
    return response.text;
};
