import { createContext, useContext, type ReactNode } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { getMe, login, type User } from '../api/auth'
import { ApiError, tokenStore } from '../api/client'

type AuthValue = {
  user: User | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => void
}

const AuthContext = createContext<AuthValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['me'],
    enabled: !!tokenStore.get(),
    retry: false,
    queryFn: async () => {
      try {
        return await getMe()
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          tokenStore.clear() // expired or invalid token
          return null
        }
        throw error
      }
    },
  })

  async function signIn(email: string, password: string) {
    await login(email, password)
    queryClient.setQueryData(['me'], await getMe())
  }

  function signOut() {
    tokenStore.clear()
    queryClient.setQueryData(['me'], null)
    // remove cached data of other queries, but keep the 'me' entry the page is watching
    queryClient.removeQueries({ predicate: (query) => query.queryKey[0] !== 'me' })
  }

  return (
    <AuthContext.Provider
      value={{ user: data ?? null, loading: isLoading, signIn, signOut }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const value = useContext(AuthContext)
  if (!value) throw new Error('useAuth must be used inside AuthProvider')
  return value
}