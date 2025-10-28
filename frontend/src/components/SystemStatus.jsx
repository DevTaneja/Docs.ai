import React from "react";

function SystemStatus({ status, onRefresh }) {
  if (!status) return null;

  return (
    <div className="flex items-center space-x-4">
      {/* LLM Status */}
      <div
        className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
          status.llm_available
            ? "bg-green-100 text-green-800"
            : "bg-red-100 text-red-800"
        }`}
      >
        <div
          className={`w-2 h-2 rounded-full ${
            status.llm_available ? "bg-green-500" : "bg-red-500"
          }`}
        ></div>
        <span className="text-sm font-medium">
          LLM: {status.llm_available ? "Connected" : "Offline"}
        </span>
      </div>

      {/* System Ready Status */}
      <div
        className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
          status.system_ready
            ? "bg-blue-100 text-blue-800"
            : "bg-gray-100 text-gray-800"
        }`}
      >
        <span>📚</span>
        <span className="text-sm font-medium">
          Documents: {status.loaded_documents?.length || 0}
        </span>
      </div>

      {/* Refresh Button */}
      <button
        onClick={onRefresh}
        className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
        title="Refresh status"
      >
        <span>🔄</span>
      </button>
    </div>
  );
}

export default SystemStatus;
