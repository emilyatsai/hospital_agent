import { Menu, X, Phone, MapPin } from 'lucide-react';
import { useState } from 'react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Hospital Name */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">E</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Emily Multispeciality Hospital</h1>
              <p className="text-sm text-gray-500">Excellence in Healthcare</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#home" className="text-gray-700 hover:text-primary-600 transition-colors">Home</a>
            <a href="#services" className="text-gray-700 hover:text-primary-600 transition-colors">Services</a>
            <a href="#about" className="text-gray-700 hover:text-primary-600 transition-colors">About</a>
            <a href="#contact" className="text-gray-700 hover:text-primary-600 transition-colors">Contact</a>
          </nav>

          {/* Contact Info */}
          <div className="hidden lg:flex items-center space-x-6 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <Phone className="w-4 h-4" />
              <span>+1 (555) 123-4567</span>
            </div>
            <div className="flex items-center space-x-2">
              <MapPin className="w-4 h-4" />
              <span>123 Health St, Medical City</span>
            </div>
          </div>

          {/* Emergency Button */}
          <button className="hidden md:block bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200">
            Emergency
          </button>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-100 py-4">
            <nav className="flex flex-col space-y-4">
              <a href="#home" className="text-gray-700 hover:text-primary-600 transition-colors px-2 py-1">Home</a>
              <a href="#services" className="text-gray-700 hover:text-primary-600 transition-colors px-2 py-1">Services</a>
              <a href="#about" className="text-gray-700 hover:text-primary-600 transition-colors px-2 py-1">About</a>
              <a href="#contact" className="text-gray-700 hover:text-primary-600 transition-colors px-2 py-1">Contact</a>
              <button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors w-fit">
                Emergency
              </button>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;