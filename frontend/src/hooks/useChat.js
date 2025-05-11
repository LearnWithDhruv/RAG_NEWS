import { useState, useEffect } from 'react'
import { sendMessageToBackend } from '../services/api'

const useChat = (sessionId) => {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (sessionId) {
      // Load chat history from backend when session changes
      const loadHistory = async () => {
        try {
          setLoading(true)
          // Replace with actual API call to fetch history
          // const history = await fetchChatHistory(sessionId)
          // setMessages(history)
        } catch (error) {
          console.error('Error loading chat history:', error)
        } finally {
          setLoading(false)
        }
      }
      loadHistory()
    } else {
      setMessages([])
    }
  }, [sessionId])

  const sendMessage = async (content) => {
    if (!sessionId) return
    
    const userMessage = {
      id: Date.now(),
      content,
      isBot: false,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setLoading(true)

    try {
      const botResponse = await sendMessageToBackend(content, sessionId)
      
      setMessages(prev => [
        ...prev, 
        {
          id: Date.now() + 1,
          content: botResponse,
          isBot: true,
          timestamp: new Date().toISOString()
        }
      ])
    } catch (error) {
      setMessages(prev => [
        ...prev, 
        {
          id: Date.now() + 1,
          content: "Sorry, I encountered an error. Please try again.",
          isBot: true,
          timestamp: new Date().toISOString()
        }
      ])
      console.error('Error sending message:', error)
    } finally {
      setLoading(false)
    }
  }

  const clearMessages = () => {
    setMessages([])
  }

  return { messages, sendMessage, loading, clearMessages }
}

export default useChat