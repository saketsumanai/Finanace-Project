import { useState, useRef, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { 
  Send, 
  Sparkles, 
  Bot, 
  User, 
  Loader2,
  TrendingUp,
  DollarSign,
  AlertCircle,
  Lightbulb,
  Paperclip,
  FileText,
  X
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { aiService } from '@/services/aiService'
import { projectService } from '@/services/projectService'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  suggestions?: string[]
  timestamp: Date
  fileAnalysis?: any
}

export default function AIChatPage() {
  const [searchParams] = useSearchParams()
  const projectId = searchParams.get('projectId')
  
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: '👋 Hello! I\'m your AI M&A advisor powered by Google Gemini. I can help you with:\n\n• Project analysis and risk assessment\n• Optimizing valuation assumptions\n• Suggesting synergies\n• Analyzing results and recommendations\n• Due diligence guidance\n• Deal structuring advice\n• **CSV file analysis** 📊 (Upload production, financial, or reserve data)\n\nWhat would you like to discuss?',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Fetch project if projectId provided
  const { data: project } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => projectService.getProject(projectId!),
    enabled: !!projectId,
  })

  // Chat mutation
  const chatMutation = useMutation({
    mutationFn: (message: string) => 
      aiService.chat(message, projectId ? parseInt(projectId) : undefined),
    onSuccess: (data) => {
      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response,
        suggestions: data.suggestions,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])
    },
    onError: () => {
      toast.error('Failed to get AI response')
    },
  })

  // CSV analysis mutation
  const csvAnalysisMutation = useMutation({
    mutationFn: (file: File) => aiService.analyzeCSV(file),
    onSuccess: (data) => {
      const analysisMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.success 
          ? `📊 **CSV Analysis: ${data.filename}**\n\n${data.ai_analysis}\n\n**Statistics:**\n• Rows: ${data.statistics?.rows}\n• Columns: ${data.statistics?.columns}\n• Column Names: ${data.statistics?.column_names.join(', ')}`
          : `❌ Failed to analyze CSV: ${data.message || data.error}`,
        fileAnalysis: data,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, analysisMessage])
      setSelectedFile(null)
    },
    onError: () => {
      toast.error('Failed to analyze CSV file')
      setSelectedFile(null)
    },
  })

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      if (!file.name.endsWith('.csv')) {
        toast.error('Only CSV files are supported')
        return
      }
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error('File size must be less than 10MB')
        return
      }
      setSelectedFile(file)
      toast.success(`File selected: ${file.name}`)
    }
  }

  const handleRemoveFile = () => {
    setSelectedFile(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleSend = () => {
    // If file is selected, analyze it
    if (selectedFile) {
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: `📎 Uploaded file: ${selectedFile.name}\n\nPlease analyze this CSV file.`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, userMessage])
      csvAnalysisMutation.mutate(selectedFile)
      return
    }

    // Otherwise, send text message
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    chatMutation.mutate(input)
    setInput('')
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion)
  }

  const handleQuickAction = (action: string) => {
    let message = ''
    switch (action) {
      case 'analyze':
        message = `Analyze this project and provide key insights on risks, opportunities, and recommended assumptions.`
        break
      case 'assumptions':
        message = `What assumptions should I use for this ${project?.project_type || 'acquisition'} deal? Consider decline rates, discount rates, and forecast period.`
        break
      case 'synergies':
        message = `What synergies should I consider for this deal? Provide specific categories and estimated values.`
        break
      case 'risks':
        message = `What are the key risks I should be aware of in this transaction? How can I mitigate them?`
        break
    }
    
    setInput(message)
  }

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">AI M&A Advisor</h1>
            <p className="text-purple-100">Powered by Google Gemini</p>
          </div>
        </div>
        {project && (
          <div className="mt-4 bg-white/10 rounded-lg p-3">
            <p className="text-sm text-purple-100">Discussing:</p>
            <p className="font-semibold">{project.name}</p>
            <p className="text-sm text-purple-100">
              {project.project_type} • ${(project.deal_size || 0).toLocaleString()}
            </p>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      {project && (
        <div className="p-4 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Quick Actions:</p>
          <div className="flex flex-wrap gap-2">
            <Button
              size="sm"
              variant="secondary"
              onClick={() => handleQuickAction('analyze')}
            >
              <TrendingUp className="w-4 h-4 mr-2" />
              Analyze Project
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => handleQuickAction('assumptions')}
            >
              <DollarSign className="w-4 h-4 mr-2" />
              Suggest Assumptions
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => handleQuickAction('synergies')}
            >
              <Lightbulb className="w-4 h-4 mr-2" />
              Identify Synergies
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => handleQuickAction('risks')}
            >
              <AlertCircle className="w-4 h-4 mr-2" />
              Assess Risks
            </Button>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {message.role === 'assistant' && (
              <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                <Bot className="w-5 h-5 text-white" />
              </div>
            )}
            
            <div
              className={`max-w-2xl ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700'
              } rounded-lg p-4 shadow-sm`}
            >
              <div className="whitespace-pre-wrap">{message.content}</div>
              
              {message.suggestions && message.suggestions.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Suggested questions:
                  </p>
                  <div className="space-y-1">
                    {message.suggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="block w-full text-left text-sm text-blue-600 dark:text-blue-400 hover:underline"
                      >
                        → {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>

            {message.role === 'user' && (
              <div className="w-8 h-8 bg-gray-300 dark:bg-gray-600 rounded-full flex items-center justify-center flex-shrink-0">
                <User className="w-5 h-5 text-gray-600 dark:text-gray-300" />
              </div>
            )}
          </div>
        ))}
        
        {chatMutation.isPending && (
          <div className="flex gap-3 justify-start">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-purple-600" />
                <span className="text-gray-600 dark:text-gray-400">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        {/* File attachment indicator */}
        {selectedFile && (
          <div className="mb-2 flex items-center gap-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <FileText className="w-4 h-4 text-blue-600" />
            <span className="text-sm text-blue-600 dark:text-blue-400 flex-1">
              {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
            </span>
            <button
              onClick={handleRemoveFile}
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}
        
        <div className="flex gap-2">
          {/* File upload button */}
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="px-3 py-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            disabled={chatMutation.isPending || csvAnalysisMutation.isPending}
            title="Upload CSV file"
          >
            <Paperclip className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
          
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder={selectedFile ? "Click send to analyze file..." : "Ask me anything about M&A valuation..."}
            className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-white"
            disabled={chatMutation.isPending || csvAnalysisMutation.isPending}
          />
          <Button
            onClick={handleSend}
            disabled={(!input.trim() && !selectedFile) || chatMutation.isPending || csvAnalysisMutation.isPending}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
          >
            {(chatMutation.isPending || csvAnalysisMutation.isPending) ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </Button>
        </div>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
          💡 Tip: Upload CSV files for AI analysis or ask specific questions for better insights
        </p>
      </div>
    </div>
  )
}
