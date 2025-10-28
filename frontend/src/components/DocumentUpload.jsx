import React, { useState } from "react";
import { legalAIClient } from "../services/api";

function DocumentUpload({ onDocumentUpload }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleFileUpload = async (file) => {
    const allowedTypes = [".pdf", ".docx", ".txt", ".doc"];
    const fileExtension = "." + file.name.split(".").pop().toLowerCase();

    if (!allowedTypes.includes(fileExtension)) {
      setUploadResult({
        success: false,
        error: `File type ${fileExtension} not supported. Please upload: ${allowedTypes.join(
          ", "
        )}`,
      });
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setUploadResult({
        success: false,
        error: "File size too large. Maximum size is 10MB.",
      });
      return;
    }

    setIsUploading(true);
    setUploadResult(null);

    try {
      const result = await legalAIClient.uploadDocument(file);
      setUploadResult(result);

      if (result.success) {
        onDocumentUpload();
      }
    } catch (error) {
      setUploadResult({
        success: false,
        error:
          error.response?.data?.detail || "Upload failed. Please try again.",
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
          isDragging
            ? "border-blue-400 bg-blue-50"
            : "border-gray-300 hover:border-gray-400"
        } ${isUploading ? "opacity-50" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {isUploading ? (
          <div className="space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <div>
              <p className="text-lg font-medium text-gray-900">
                Processing document...
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Analyzing legal structure and creating semantic index
              </p>
            </div>
          </div>
        ) : (
          <>
            <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">📤</span>
            </div>
            <div className="space-y-2">
              <p className="text-lg font-medium text-gray-900">
                Drag and drop your legal documents
              </p>
              <p className="text-sm text-gray-500">
                Supports PDF, DOCX, DOC, and TXT files up to 10MB
              </p>
            </div>
            <label className="mt-6 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 cursor-pointer">
              <span className="mr-2">📄</span>
              Choose Files
              <input
                type="file"
                className="hidden"
                onChange={handleFileSelect}
                accept=".pdf,.docx,.doc,.txt"
              />
            </label>
          </>
        )}
      </div>

      {/* Upload Result */}
      {uploadResult && (
        <div
          className={`rounded-lg p-4 ${
            uploadResult.success
              ? "bg-green-50 border border-green-200"
              : "bg-red-50 border border-red-200"
          }`}
        >
          <div className="flex items-start space-x-3">
            <div
              className={`w-5 h-5 rounded-full flex items-center justify-center mt-0.5 ${
                uploadResult.success ? "bg-green-500" : "bg-red-500"
              }`}
            >
              <span className="text-white text-xs">
                {uploadResult.success ? "✓" : "!"}
              </span>
            </div>
            <div className="flex-1">
              <p
                className={`text-sm font-medium ${
                  uploadResult.success ? "text-green-800" : "text-red-800"
                }`}
              >
                {uploadResult.success
                  ? "Document processed successfully!"
                  : "Upload failed"}
              </p>
              <p
                className={`text-sm mt-1 ${
                  uploadResult.success ? "text-green-600" : "text-red-600"
                }`}
              >
                {uploadResult.success
                  ? uploadResult.message ||
                    `Created ${uploadResult.chunks_count} semantic chunks. You can now ask questions about this document.`
                  : uploadResult.error}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DocumentUpload;
