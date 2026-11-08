import { Link, Outlet } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function Layout() {
  const { user, signOut } = useAuth()

  return (
    <div className="min-h-screen bg-green-50">
      <header className="flex items-center justify-between bg-green-900 p-4 text-white">
        <Link to="/" className="text-lg font-bold">AgroSense</Link>
        <div className="flex items-center gap-4 text-sm">
          <span>{user?.email}</span>
          <button onClick={signOut} className="rounded bg-green-700 px-3 py-1 hover:bg-green-600">
            Log out
          </button>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  )
}