import React, { useState, useRef, useEffect } from "react";
import { legalAIClient } from "../services/api";

function ChatInterface({ systemReady }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputMessage.trim() || isLoading || !systemReady) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      content: inputMessage.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await legalAIClient.askQuestion(inputMessage.trim());

      const botMessage = {
        id: Date.now() + 1,
        type: "bot",
        content: response.answer,
        confidence: response.confidence,
        sources: response.sources,
        performance: response.performance,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: "error",
        content:
          "Sorry, I encountered an error processing your question. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!systemReady) {
    return (
      <div className="bg-white rounded-lg shadow-sm border p-12 text-center">
        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <span className="text-2xl">📚</span>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          No documents loaded
        </h3>
        <p className="text-gray-500 mb-4">
          Please upload legal documents first to start asking questions
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border flex flex-col h-[600px]">
      {/* Chat Header */}
      <div className="px-6 py-4 border-b">
        <h2 className="text-lg font-semibold text-gray-900">
          Legal Document Q&A
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          Ask questions about your uploaded legal documents
        </p>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🤖</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Ask about your legal documents
            </h3>
            <p className="text-gray-500">
              Example: "What are the termination conditions?" or "Explain the
              compensation package"
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <Message key={message.id} message={message} />
          ))
        )}

        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-blue-600">🤖</span>
            </div>
            <div className="flex-1">
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                  <div
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.4s" }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 border-t">
        <form onSubmit={handleSendMessage} className="flex space-x-4">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask a question about your legal documents..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <span>📤</span>
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  );
}

// Message Component
function Message({ message }) {
  return (
    <div
      className={`flex items-start space-x-3 ${
        message.type === "user" ? "flex-row-reverse space-x-reverse" : ""
      }`}
    >
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          message.type === "user"
            ? "bg-blue-100"
            : message.type === "error"
            ? "bg-red-100"
            : "bg-green-100"
        }`}
      >
        {message.type === "user" ? (
          <span className="text-blue-600">👤</span>
        ) : message.type === "error" ? (
          <span className="text-red-600">⚠️</span>
        ) : (
          <span className="text-green-600">🤖</span>
        )}
      </div>

      <div className={`flex-1 ${message.type === "user" ? "text-right" : ""}`}>
        <div
          className={`inline-block rounded-lg px-4 py-2 max-w-[80%] ${
            message.type === "user"
              ? "bg-blue-600 text-white"
              : message.type === "error"
              ? "bg-red-100 text-red-800 border border-red-200"
              : "bg-gray-100 text-gray-900"
          }`}
        >
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* Bot message metadata */}
        {message.type === "bot" && (
          <div className="mt-2 space-y-2">
            {/* Confidence and Performance */}
            <div className="flex items-center space-x-4 text-xs text-gray-500">
              <span>Confidence: {(message.confidence * 100).toFixed(1)}%</span>
              <span>Response: {message.performance?.total_time_seconds}s</span>
            </div>

            {/* Sources */}
            {message.sources && message.sources.length > 0 && (
              <div className="bg-blue-50 rounded-lg p-3">
                <p className="text-xs font-medium text-blue-900 mb-2">
                  Sources:
                </p>
                <div className="space-y-2">
                  {message.sources.map((source, index) => (
                    <div key={index} className="text-xs text-blue-800">
                      <p className="font-medium">
                        Source {index + 1} (Relevance:{" "}
                        {(source.relevance_score * 100).toFixed(1)}%)
                      </p>
                      <p className="opacity-80 mt-1">
                        {source.content_preview}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        <p className="text-xs text-gray-500 mt-1">
          {message.timestamp.toLocaleTimeString()}
        </p>
      </div>
    </div>
  );
}

export default ChatInterface;
