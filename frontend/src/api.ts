import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export interface UploadResponse {
  message: string;
  filename: string;
  chunks: number;
}

export interface QuestionResponse {
  answer: string;
}

export const uploadPDF = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post<UploadResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const askQuestion = async (question: string): Promise<QuestionResponse> => {
  const response = await api.post<QuestionResponse>('/ask', { question });
  return response.data;
};

export const clearDatabase = async (): Promise<void> => {
  await api.delete('/clear');
};