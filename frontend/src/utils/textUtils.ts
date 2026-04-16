export const cleanTextForSpeech = (text: string): string => {
  if (!text) return '';
  return text
    .replace(/[#*_>~`]/g, '') // Remove markdown characters
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Extract link text
    .replace(/\s+/g, ' ') // Collapse whitespace
    .trim();
};
