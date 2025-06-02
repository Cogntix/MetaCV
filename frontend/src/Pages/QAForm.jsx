import React, { useState, useEffect } from "react";
import { Edit3, User, Briefcase, ArrowLeft, Send } from "lucide-react";
import { toast } from "react-toastify";
import axios from "axios";

const QAFormPage = ({ qaData, onBackToUpload }) => {
  const [answers, setAnswers] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState(null);
  const [tempAnswer, setTempAnswer] = useState("");

  const defaultQaData = [
    {
      id: "C1",
      question: "What is your full name?",
      answer: "N/A",
      source: "user",
    },
    {
      id: "C2",
      question: "What is your email address?",
      answer: "N/A",
      source: "user",
    },
    {
      id: "C3",
      question: "What is your phone number?",
      answer: "N/A",
      source: "user",
    },
    {
      id: "C4",
      question: "What is your LinkedIn profile URL?",
      answer: "N/A",
      source: "user",
    },
    {
      id: "C5",
      question: "What is your current location?",
      answer: "N/A",
      source: "user",
    },
  ];

  const ensureArrayData = (data) => {
    if (!data) return defaultQaData;
    if (Array.isArray(data)) return data;
    if (data.questions && Array.isArray(data.questions)) return data.questions;
    if (typeof data === "object") {
      const questionsArray = Object.values(data).filter(
        (item) => item && typeof item === "object" && item.id
      );
      return questionsArray.length > 0 ? questionsArray : defaultQaData;
    }
    return defaultQaData;
  };

  const getJobPrefix = () => {
    if (!qaData) return "SE";

    const jobPosition = qaData.jobPosition || qaData.jobTitle || "";

    // Map job positions to prefixes
    const jobPrefixMap = {
      "software-engineer": "SE",
      "ui-ux": "UX",
      "qa-engineer": "QA",
      product: "PM",
      project: "PJ",
      data: "DS",
      devops: "DO",
      marketing: "MK",
      sales: "SR",
      hr: "HR",
    };

    return jobPrefixMap[jobPosition] || "SE";
  };

  // Process the QA data
  const currentQaData = ensureArrayData(qaData?.qa);
  const jobPrefix = getJobPrefix();

  // Filter questions by category
  const personalQuestions = currentQaData.filter(
    (q) => q && q.id && q.id.startsWith("C")
  );

  const technicalQuestions = currentQaData.filter(
    (q) => q && q.id && q.id.startsWith(jobPrefix)
  );

  useEffect(() => {
    const initialAnswers = {};
    const allQuestions = [...personalQuestions, ...technicalQuestions];
    allQuestions.forEach((item) => {
      initialAnswers[item.id] = item.answer || "N/A";
    });
    setAnswers(initialAnswers);
  }, []);

  const handleAnswerChange = (questionId, newAnswer) => {
    console.log("questionId", questionId, "newAnswer", newAnswer);
    setAnswers((prev) => ({
      ...prev,
      [questionId]: newAnswer,
    }));
  };

  // Handle starting edit mode
  const handleStartEdit = (questionId) => {
    setEditingQuestion(questionId);
    setTempAnswer(answers[questionId] === "N/A" ? "" : answers[questionId]);
  };

  // Handle saving the edited answer
  const handleSaveEdit = (questionId) => {
    handleAnswerChange(questionId, tempAnswer);
    setEditingQuestion(null);
    setTempAnswer("");
  };

  // Handle canceling edit
  const handleCancelEdit = () => {
    setEditingQuestion(null);
    setTempAnswer("");
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);

    const questionsToSubmit = [...personalQuestions, ...technicalQuestions];

    const submissionData = {
      jobPosition: qaData?.jobPosition || "N/A",
      extracted_text: qaData?.extracted_text || "N/A",
      answers: questionsToSubmit.map((q) => ({
        question: q.question,
        correct_answer: answers[q.id] || "",
      })),
    };

    try {
      const response = await axios.post(
        "http://localhost:5000/confirm",
        submissionData
      );

      // console.log("Server response:", response.data);
      toast.success("Application submitted successfully!");
      setTimeout(() => {
        onBackToUpload();
      }, 2000);
    } catch (error) {
      console.error("Submission error:", error);
      toast.error("There was an error submitting your application.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBackClick = () => {
    if (onBackToUpload) {
      onBackToUpload();
    }
  };

  const questionsToShow = [...personalQuestions, ...technicalQuestions];
  const isFormComplete = () => {
    return questionsToShow.every(
      (q) =>
        answers[q.id] && answers[q.id].trim() !== "" && answers[q.id] !== "N/A"
    );
  };

  const completedAnswers = questionsToShow.filter(
    (q) =>
      answers[q.id] && answers[q.id].trim() !== "" && answers[q.id] !== "N/A"
  ).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="mb-6">
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
              MetaCV
            </h1>
            <div className="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full"></div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Review Your Application Details
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-6">
            {qaData
              ? `We've automatically filled in information from your CV for the ${
                  qaData.jobTitle || qaData.jobPosition || "selected"
                } position. Please review and complete any missing details.`
              : "Please complete the application form below."}
          </p>

          {/* Progress Bar */}
          <div className="bg-white rounded-xl p-4 shadow-lg border border-gray-100 max-w-md mx-auto">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                Progress
              </span>
              <span className="text-sm font-medium text-gray-900">
                {completedAnswers}/{questionsToShow.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                style={{
                  width: `${
                    questionsToShow.length > 0
                      ? (completedAnswers / questionsToShow.length) * 100
                      : 0
                  }%`,
                }}
              ></div>
            </div>
          </div>
        </div>

        {/* Back Button */}
        <div className="mb-6">
          <button
            onClick={handleBackClick}
            className="inline-flex items-center px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Upload
          </button>
        </div>

        <div className="space-y-8">
          {/* Personal Information Section */}
          {personalQuestions.length > 0 && (
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
              <div className="flex items-center mb-6">
                <User className="h-6 w-6 text-blue-600 mr-3" />
                <h3 className="text-2xl font-semibold text-gray-900">
                  Personal Information
                </h3>
              </div>

              <div className="space-y-6">
                {personalQuestions.map((qa) => (
                  <div
                    key={qa.id}
                    className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <h4 className="font-medium text-gray-900 flex-1">
                        {qa.question}
                      </h4>
                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={() => handleStartEdit(qa.id)}
                          className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                        >
                          <Edit3 className="h-4 w-4" />
                        </button>
                      </div>
                    </div>

                    {editingQuestion === qa.id ? (
                      <div className="mt-3">
                        <textarea
                          value={tempAnswer}
                          onChange={(e) => setTempAnswer(e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                          rows="3"
                          placeholder="Enter your answer..."
                          autoFocus
                        />
                        <div className="flex justify-end mt-2 space-x-2">
                          <button
                            onClick={handleCancelEdit}
                            className="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 transition-colors"
                          >
                            Cancel
                          </button>
                          <button
                            onClick={() => handleSaveEdit(qa.id)}
                            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                          >
                            Save
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div
                        className={`mt-3 p-3 rounded-lg cursor-pointer ${
                          answers[qa.id] === "N/A" || !answers[qa.id]?.trim()
                            ? "bg-red-50 border border-red-200"
                            : "bg-gray-50 border border-gray-200"
                        }`}
                        onClick={() => handleStartEdit(qa.id)}
                      >
                        <p
                          className={`text-sm ${
                            answers[qa.id] === "N/A" || !answers[qa.id]?.trim()
                              ? "text-red-600 italic"
                              : "text-gray-700"
                          }`}
                        >
                          {answers[qa.id] === "N/A" || !answers[qa.id]?.trim()
                            ? "Please provide this information"
                            : answers[qa.id]}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Technical Information Section */}
          {technicalQuestions.length > 0 && (
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
              <div className="flex items-center mb-6">
                <Briefcase className="h-6 w-6 text-purple-600 mr-3" />
                <h3 className="text-2xl font-semibold text-gray-900">
                  Technical Questions
                </h3>
              </div>

              <div className="space-y-6">
                {technicalQuestions.map((qa) => (
                  <div
                    key={qa.id}
                    className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <h4 className="font-medium text-gray-900 flex-1">
                        {qa.question}
                      </h4>
                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={() => handleStartEdit(qa.id)}
                          className="p-1 text-gray-400 hover:text-purple-600 transition-colors"
                        >
                          <Edit3 className="h-4 w-4" />
                        </button>
                      </div>
                    </div>

                    {editingQuestion === qa.id ? (
                      <div className="mt-3">
                        <textarea
                          value={tempAnswer}
                          onChange={(e) => setTempAnswer(e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                          rows="3"
                          placeholder="Enter your answer..."
                          autoFocus
                        />
                        <div className="flex justify-end mt-2 space-x-2">
                          <button
                            onClick={handleCancelEdit}
                            className="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 transition-colors"
                          >
                            Cancel
                          </button>
                          <button
                            onClick={() => handleSaveEdit(qa.id)}
                            className="px-3 py-1 text-sm bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
                          >
                            Save
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div
                        className={`mt-3 p-3 rounded-lg cursor-pointer ${
                          answers[qa.id] === "N/A" || !answers[qa.id]?.trim()
                            ? "bg-red-50 border border-red-200"
                            : "bg-gray-50 border border-gray-200"
                        }`}
                        onClick={() => handleStartEdit(qa.id)}
                      >
                        <p
                          className={`text-sm ${
                            answers[qa.id] === "N/A" || !answers[qa.id]?.trim()
                              ? "text-red-600 italic"
                              : "text-gray-700"
                          }`}
                        >
                          {answers[qa.id] === "N/A" || !answers[qa.id]?.trim()
                            ? "Please provide this information"
                            : answers[qa.id]}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Submit Section */}
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <div className="text-center">
              {!isFormComplete() && (
                <div className="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                  <p className="text-amber-800">
                    <strong>
                      Please complete all required fields before submitting.
                    </strong>
                    <br />
                    {questionsToShow.length - completedAnswers} questions still
                    need answers.
                  </p>
                </div>
              )}

              <button
                onClick={handleSubmit}
                disabled={!isFormComplete() || isSubmitting}
                className={`inline-flex items-center px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-200 ${
                  !isFormComplete() || isSubmitting
                    ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                    : "bg-gradient-to-r from-green-600 to-blue-600 text-white hover:from-green-700 hover:to-blue-700 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                }`}
              >
                {isSubmitting ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                    Submitting Application...
                  </>
                ) : (
                  <>
                    <Send className="h-5 w-5 mr-3" />
                    Submit Final Application
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QAFormPage;
