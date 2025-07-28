import React, { useState } from 'react';
import { FileText, Users, Target, Brain, Layers, Zap } from 'lucide-react';

function App() {
  const [analysisRunning, setAnalysisRunning] = useState(false);

  const handleRunAnalysis = () => {
    setAnalysisRunning(true);
    // Simulate analysis running
    setTimeout(() => setAnalysisRunning(false), 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-indigo-600 rounded-lg">
              <FileText className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Multi-Collection PDF Analysis System</h1>
              <p className="text-gray-600 mt-1">Intelligent document analysis with persona-based content extraction</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
            Transform PDF Collections into 
            <span className="text-indigo-600"> Actionable Insights</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8 leading-relaxed">
            Our advanced AI system processes multiple PDF documents simultaneously, extracting and ranking 
            content based on specific personas and job requirements. Optimized for performance with 
            sophisticated natural language processing.
          </p>
          
          <div className="flex justify-center space-x-4">
            <button 
              onClick={handleRunAnalysis}
              disabled={analysisRunning}
              className="px-8 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-all duration-200 hover:shadow-lg transform hover:-translate-y-1 disabled:opacity-50 disabled:transform-none"
            >
              {analysisRunning ? (
                <span className="flex items-center space-x-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Running Analysis...</span>
                </span>
              ) : (
                <span className="flex items-center space-x-2">
                  <Zap className="h-5 w-5" />
                  <span>Run Demo Analysis</span>
                </span>
              )}
            </button>
            <button className="px-8 py-4 border-2 border-indigo-600 text-indigo-600 font-semibold rounded-lg hover:bg-indigo-50 transition-all duration-200">
              View Documentation
            </button>
          </div>
        </div>

        {/* Key Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100">
            <div className="flex items-center mb-4">
              <div className="p-3 bg-blue-100 rounded-lg mr-4">
                <FileText className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Multi-Document Processing</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              Simultaneously analyze 3-10 PDF documents with intelligent text extraction, 
              page number preservation, and robust error handling for various document formats.
            </p>
          </div>

          <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100">
            <div className="flex items-center mb-4">
              <div className="p-3 bg-green-100 rounded-lg mr-4">
                <Users className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Persona-Based Analysis</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              Tailored content extraction based on user roles and expertise areas. Optimized for 
              travel planning, HR management, and culinary domains with intelligent keyword recognition.
            </p>
          </div>

          <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100">
            <div className="flex items-center mb-4">
              <div className="p-3 bg-purple-100 rounded-lg mr-4">
                <Target className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Job-Aligned Ranking</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              Smart section ranking based on job-to-be-done requirements. Prioritizes content 
              relevance with multi-factor scoring combining importance, uniqueness, and completeness.
            </p>
          </div>
        </div>

        {/* Technical Specifications */}
        <div className="bg-white rounded-2xl p-8 shadow-lg mb-16 border border-gray-100">
          <div className="flex items-center mb-6">
            <Brain className="h-8 w-8 text-indigo-600 mr-3" />
            <h3 className="text-2xl font-bold text-gray-900">Technical Architecture</h3>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-4">Core Components</h4>
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-indigo-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span><strong>PDF Parser:</strong> PyMuPDF-based text extraction with page tracking</span>
                </li>
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-indigo-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span><strong>Content Segmenter:</strong> Header-based and topic-based section identification</span>
                </li>
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-indigo-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span><strong>Persona Analyzer:</strong> Semantic similarity with lightweight NLP models</span>
                </li>
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-indigo-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span><strong>Section Ranker:</strong> Multi-factor importance scoring algorithm</span>
                </li>
                <li className="flex items-start">
                  <div className="w-2 h-2 bg-indigo-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span><strong>Subsection Refiner:</strong> Content enhancement and quality optimization</span>
                </li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-4">Performance Specifications</h4>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700 font-medium">Processing Time</span>
                  <span className="text-indigo-600 font-semibold">≤ 60 seconds</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700 font-medium">Model Size</span>
                  <span className="text-indigo-600 font-semibold">≤ 1GB</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700 font-medium">Hardware</span>
                  <span className="text-indigo-600 font-semibold">CPU Only</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700 font-medium">Offline Capable</span>
                  <span className="text-green-600 font-semibold">✓ Yes</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Usage Example */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 text-white mb-16">
          <div className="flex items-center mb-6">
            <Layers className="h-8 w-8 mr-3" />
            <h3 className="text-2xl font-bold">Usage Example</h3>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-lg font-semibold mb-4 text-indigo-100">Input Format</h4>
              <div className="bg-black bg-opacity-20 rounded-lg p-4 font-mono text-sm">
                <pre className="text-indigo-100">{`{
  "challenge_info": {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planning"
  },
  "documents": [
    {"filename": "guide.pdf", "title": "Travel Guide"}
  ],
  "persona": {
    "role": "Travel planning specialist"
  },
  "job_to_be_done": {
    "task": "Plan 4-day itinerary for 10 friends"
  }
}`}</pre>
              </div>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold mb-4 text-indigo-100">Command Line</h4>
              <div className="bg-black bg-opacity-20 rounded-lg p-4 font-mono text-sm">
                <div className="text-indigo-100 mb-2"># Install dependencies</div>
                <div className="text-white mb-4">pip install -r requirements.txt</div>
                
                <div className="text-indigo-100 mb-2"># Run analysis</div>
                <div className="text-white mb-4">python run_analysis.py input.json ./docs/</div>
                
                <div className="text-indigo-100 mb-2"># Docker deployment</div>
                <div className="text-white">docker run pdf-analyzer</div>
              </div>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <h3 className="text-3xl font-bold text-gray-900 mb-4">Ready to Process Your PDF Collections?</h3>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get started with our comprehensive document analysis system. Perfect for hackathons, 
            research projects, and production applications requiring intelligent content extraction.
          </p>
          
          <div className="flex justify-center space-x-4">
            <button className="px-8 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-all duration-200 hover:shadow-lg transform hover:-translate-y-1">
              Download System
            </button>
            <button className="px-8 py-4 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition-all duration-200">
              View GitHub Repository
            </button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>Multi-Collection PDF Analysis System • Optimized for Challenge 1b • Built with advanced NLP techniques</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;