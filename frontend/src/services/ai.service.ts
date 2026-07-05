import { api } from './api'
import { useAuthStore } from '@/store/auth.store'
import type { Conversation, Message } from '@/types/domain.types'

export const AIService = {
  listConversations: () =>
    api.get<{ count: number; results: Conversation[] }>('/ai/conversations/').then(r => r.data),

  createConversation: (initial_topic?: string) =>
    api.post<Conversation>('/ai/conversations/', { initial_topic }).then(r => r.data),

  getMessages: (convId: string, params?: { limit?: number; before?: string }) =>
    api.get<{ count: number; results: Message[] }>(`/ai/conversations/${convId}/messages/`, { params }).then(r => r.data),

  streamMessage: async (
    convId: string,
    content: string,
    onChunk: (chunk: string) => void,
    signal?: AbortSignal,
  ) => {
    const token = useAuthStore.getState().accessToken
    const baseUrl = import.meta.env.VITE_API_URL || '/api/v1'
    const response = await fetch(`${baseUrl}/ai/conversations/${convId}/messages/send/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
        'X-Language': localStorage.getItem('lang') || 'ru',
      },
      body: JSON.stringify({ content }),
      signal,
    })

    if (!response.ok || !response.body) throw new Error('Stream error')

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      const text = decoder.decode(value, { stream: true })
      for (const line of text.split('\n')) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            if (data.type === 'chunk') onChunk(data.content)
            if (data.type === 'error') throw new Error(data.message)
          } catch (e: any) {
            if (e?.message && e.message !== 'JSON parse error') throw e
          }
        }
      }
    }
  },
}
