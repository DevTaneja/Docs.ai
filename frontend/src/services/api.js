import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

class LegalAIClient {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
    });
  }

  async getStatus() {
    const response = await this.client.get("/status");
    return response.data;
  }

  async uploadDocument(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await this.client.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  }

  async askQuestion(question, topK = 3) {
    const response = await this.client.post("/ask", {
      question,
      top_k: topK,
    });
    return response.data;
  }

  async listDocuments() {
    const response = await this.client.get("/documents");
    return response.data;
  }

  async clearDocuments() {
    const response = await this.client.delete("/documents");
    return response.data;
  }

  async healthCheck() {
    const response = await this.client.get("/health");
    return response.data;
  }
}

export const legalAIClient = new LegalAIClient();
