import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Header from './components/Header'
import Hero from './components/Hero'
import Services from './components/Services'
import About from './components/About'
import Contact from './components/Contact'
import Footer from './components/Footer'
import LoginPage from './components/LoginPage'

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    )
  }

  return isAuthenticated ? children : <Navigate to="/login" />
}

// Landing Page Component
const LandingPage = () => (
  <div className="min-h-screen bg-white">
    <Header />
    <main>
      <Hero />
      <Services />
      <About />
      <Contact />
    </main>
    <Footer />
  </div>
)

// Dashboard Component (placeholder)
const Dashboard = () => {
  const { user, signOut } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {user?.user_metadata?.full_name || user?.email}</span>
              <button
                onClick={signOut}
                className="text-sm text-red-600 hover:text-red-700 font-medium"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
        <div className="bg-white rounded-xl shadow-sm p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Patient Dashboard</h2>
          <p className="text-gray-600 mb-6">
            Welcome to your healthcare dashboard. Here you can manage your appointments,
            view your medical records, and access AI-powered health insights.
          </p>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-6 bg-primary-50 rounded-lg">
              <h3 className="font-semibold text-primary-900 mb-2">Appointments</h3>
              <p className="text-sm text-primary-700">View and manage your upcoming appointments</p>
            </div>
            <div className="p-6 bg-primary-50 rounded-lg">
              <h3 className="font-semibold text-primary-900 mb-2">Medical Records</h3>
              <p className="text-sm text-primary-700">Access your medical history and test results</p>
            </div>
            <div className="p-6 bg-primary-50 rounded-lg">
              <h3 className="font-semibold text-primary-900 mb-2">AI Insights</h3>
              <p className="text-sm text-primary-700">View AI-powered health recommendations</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
