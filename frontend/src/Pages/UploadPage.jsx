import React, { useState, useRef } from "react";
import { Upload, FileText, Briefcase, CheckCircle, X } from "lucide-react";
import axios from "axios";
import { toast } from "react-toastify";

const UploadPage = ({ onUploadComplete }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedPosition, setSelectedPosition] = useState("");
  const [isDragOver, setIsDragOver] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fileInputRef = useRef(null);

  const jobPositions = [
    {
      id: "software-engineer",
      title: "Software Engineer",
      department: "Engineering",
    },
    {
      id: "qa-engineer",
      title: "QA Engineer",
      department: "Engineering",
    },
    { id: "ui-ux", title: "UI/UX Designer", department: "Design" },
    { id: "product", title: "Product Manager", department: "Product" },
    { id: "project", title: "Project Manager", department: "Project" },
    {
      id: "dataScientist",
      title: "Data Scientist",
      department: "Data & Analytics",
    },
    { id: "devops", title: "DevOps Engineer", department: "Engineering" },
    { id: "marketing", title: "Marketing Specialist", department: "Marketing" },
    { id: "sales", title: "Sales Representative", department: "Sales" },
    { id: "hr", title: "HR Business Partner", department: "Human Resources" },
  ];

  const isValidFileType = (file) => {
    const validTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    const validExtensions = [".pdf", ".doc", ".docx"];

    return (
      validTypes.includes(file.type) ||
      validExtensions.some((ext) => file.name.toLowerCase().endsWith(ext))
    );
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (isValidFileType(file)) {
        setSelectedFile(file);
      } else {
        toast.error("Please upload a PDF or Word document (.pdf, .doc, .docx)");
      }
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (isValidFileType(file)) {
        setSelectedFile(file);
      } else {
        toast.error("Please upload a PDF or Word document (.pdf, .doc, .docx)");
      }
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile || !selectedPosition) {
      toast.error(
        "Please fill in all fields: upload file, and select a job position."
      );
      return;
    }

    setIsSubmitting(true);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("jobPosition", selectedPosition);

      const response = await axios.post(
        "http://localhost:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Handle successful response
      console.log("Upload success:", response);

      // Find the selected position details
      const selectedPositionDetails = jobPositions.find(
        (pos) => pos.id === selectedPosition
      );

      // Prepare data to pass to QA form
      const extractedData = {
        fileName: selectedFile.name,
        fileSize: selectedFile.size,
        jobPosition: selectedPosition,
        jobTitle: selectedPositionDetails?.title || selectedPosition,
        department: selectedPositionDetails?.department || "",
        uploadResponse: response.data, // Include server response data
        // Add any additional extracted data from the server response
        ...response.data,
      };

      // Call the callback function to move to QA page
      if (onUploadComplete) {
        onUploadComplete(extractedData);
      }

      toast.success("CV uploaded successfully! Proceeding to Q&A section...");
    } catch (error) {
      console.log("Upload failed:", error);
      toast.error("CV upload failed. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="mb-6">
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
              MetaCV
            </h1>
            <div className="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full"></div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Apply for Your Dream Job
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload your CV and select the position you're interested in. We'll
            review your application and get back to you soon.
          </p>
        </div>

        <div className="space-y-8">
          {/* CV Upload Section */}
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <div className="flex items-center mb-6">
              <FileText className="h-6 w-6 text-blue-600 mr-3" />
              <h2 className="text-2xl font-semibold text-gray-900">
                Upload Your CV
              </h2>
            </div>

            <div
              className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
                isDragOver
                  ? "border-blue-500 bg-blue-50"
                  : selectedFile
                  ? "border-green-500 bg-green-50"
                  : "border-gray-300 hover:border-blue-400 hover:bg-blue-50"
              }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileSelect}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />

              {selectedFile ? (
                <div className="space-y-4">
                  <CheckCircle className="h-16 w-16 text-green-500 mx-auto" />
                  <div>
                    <p className="text-lg font-medium text-green-700">
                      File Selected
                    </p>
                    <p className="text-gray-600">{selectedFile.name}</p>
                    <p className="text-sm text-gray-500">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={removeFile}
                    className="inline-flex items-center px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors"
                  >
                    <X className="h-4 w-4 mr-2" />
                    Remove File
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <Upload className="h-16 w-16 text-gray-400 mx-auto" />
                  <div>
                    <p className="text-lg font-medium text-gray-700">
                      Drag and drop your CV here, or click to browse
                    </p>
                    <p className="text-gray-500">
                      PDF, DOC, or DOCX files only, max 10MB
                    </p>
                  </div>
                  <div className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
                    Choose File
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Job Position Selection */}
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <div className="flex items-center mb-6">
              <Briefcase className="h-6 w-6 text-purple-600 mr-3" />
              <h2 className="text-2xl font-semibold text-gray-900">
                Select Job Position
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {jobPositions.map((position) => (
                <label
                  key={position.id}
                  className={`relative flex items-center p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                    selectedPosition === position.id
                      ? "border-purple-500 bg-purple-50 shadow-md"
                      : "border-gray-200 hover:border-purple-300 hover:bg-purple-25"
                  }`}
                >
                  <input
                    type="radio"
                    name="position"
                    value={position.id}
                    checked={selectedPosition === position.id}
                    onChange={(e) => setSelectedPosition(e.target.value)}
                    className="sr-only"
                  />
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-gray-900">
                        {position.title}
                      </h3>
                      <div
                        className={`w-4 h-4 rounded-full border-2 ${
                          selectedPosition === position.id
                            ? "border-purple-500 bg-purple-500"
                            : "border-gray-300"
                        }`}
                      >
                        {selectedPosition === position.id && (
                          <div className="w-full h-full rounded-full bg-white scale-50"></div>
                        )}
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">
                      {position.department}
                    </p>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <div className="text-center">
            <button
              type="button"
              onClick={handleSubmit}
              disabled={!selectedFile || !selectedPosition || isSubmitting}
              className={`inline-flex items-center px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-200 ${
                !selectedFile || !selectedPosition || isSubmitting
                  ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                  : "bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              }`}
            >
              {isSubmitting ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                  Submitting Application...
                </>
              ) : (
                <>
                  <Upload className="h-5 w-5 mr-3" />
                  Submit Application
                </>
              )}
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-600">
          <p>
            By submitting your application, you agree to our Terms of Service
            and Privacy Policy.
          </p>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
