import { useState, type FormEvent } from 'react'
import { Link, Navigate } from 'react-router-dom'
import { register } from '../api/auth'
import { useAuth } from '../auth/AuthContext'

export default function AuthPage({ mode }: { mode: 'login' | 'register' }) {
  const { user, signIn } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  if (user) return <Navigate to="/" replace />

  const isRegister = mode === 'register'

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    setError(null)
    setBusy(true)
    try {
      if (isRegister) await register(email, password)
      await signIn(email, password)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-green-50 p-4">
      <form
        onSubmit={onSubmit}
        className="w-full max-w-sm space-y-4 rounded-xl bg-white p-6 shadow"
      >
        <h1 className="text-2xl font-bold text-green-900">
          {isRegister ? 'Create your account' : 'Welcome back'}
        </h1>

        <label className="block text-sm font-medium text-gray-700">
          Email
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full rounded border border-gray-300 p-2"
          />
        </label>

        <label className="block text-sm font-medium text-gray-700">
          Password
          <input
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded border border-gray-300 p-2"
          />
        </label>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={busy}
          className="w-full rounded bg-green-700 p-2 font-semibold text-white hover:bg-green-800 disabled:opacity-50"
        >
          {busy ? 'Please wait…' : isRegister ? 'Register' : 'Log in'}
        </button>

        <p className="text-center text-sm text-gray-600">
          {isRegister ? 'Already have an account? ' : 'No account yet? '}
          <Link
            to={isRegister ? '/login' : '/register'}
            className="font-medium text-green-700 underline"
          >
            {isRegister ? 'Log in' : 'Register'}
          </Link>
        </p>
      </form>
    </div>
  )
}