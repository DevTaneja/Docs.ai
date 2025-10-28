import React, { useState, useEffect } from "react";
import DocumentUpload from "./components/DocumentUpload";
import ChatInterface from "./components/ChatInterface";
import SystemStatus from "./components/SystemStatus";
import { legalAIClient } from "./services/api";

function App() {
  const [activeTab, setActiveTab] = useState("upload");
  const [systemStatus, setSystemStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadSystemStatus();
  }, []);

  const loadSystemStatus = async () => {
    try {
      const status = await legalAIClient.getStatus();
      setSystemStatus(status);
    } catch (error) {
      console.error("Failed to load system status:", error);
      setSystemStatus({
        system_ready: false,
        llm_available: false,
        loaded_documents: [],
        error: "Cannot connect to backend",
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-blue-600 rounded-lg flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-xl">⚖️</span>
          </div>
          <div className="text-2xl font-bold text-gray-700">
            Loading Legal AI Assistant...
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">⚖️</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Legal AI Assistant
                </h1>
                <p className="text-sm text-gray-500">
                  AI-powered legal document analysis
                </p>
              </div>
            </div>
            <SystemStatus status={systemStatus} onRefresh={loadSystemStatus} />
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {["upload", "chat", "documents"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                <span>
                  {tab === "upload" && "📄"}
                  {tab === "chat" && "💬"}
                  {tab === "documents" && "📚"}
                </span>
                <span>
                  {tab === "upload" && "Upload Documents"}
                  {tab === "chat" && "Ask Questions"}
                  {tab === "documents" && "Documents"}
                </span>
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === "upload" && (
          <DocumentUpload onDocumentUpload={loadSystemStatus} />
        )}

        {activeTab === "chat" && (
          <ChatInterface systemReady={systemStatus?.system_ready} />
        )}

        {activeTab === "documents" && (
          <DocumentLibrary documents={systemStatus?.loaded_documents || []} />
        )}
      </main>
    </div>
  );
}

// Document Library Component
function DocumentLibrary({ documents }) {
  if (documents.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <span className="text-2xl">📚</span>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          No documents loaded
        </h3>
        <p className="text-gray-500">
          Upload legal documents to start analyzing them
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border">
      <div className="px-6 py-4 border-b">
        <h2 className="text-lg font-semibold text-gray-900">
          Document Library
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          {documents.length} document{documents.length !== 1 ? "s" : ""} loaded
        </p>
      </div>

      <div className="divide-y">
        {documents.map((doc, index) => (
          <div key={doc.document_id || index} className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs">✓</span>
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">{doc.filename}</h3>
                  <p className="text-sm text-gray-500">
                    {doc.chunks_count} chunks •{" "}
                    {Math.round(doc.file_size / 1024)} KB
                  </p>
                </div>
              </div>
              <div className="text-sm text-gray-500">
                {doc.loaded_at
                  ? new Date(doc.loaded_at).toLocaleDateString()
                  : "Recently"}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
