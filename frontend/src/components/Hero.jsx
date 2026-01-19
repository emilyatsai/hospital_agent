import { ArrowRight, Shield, Clock, Award } from 'lucide-react';

const Hero = () => {
  return (
    <section className="bg-gradient-to-br from-primary-50 to-white px-6 py-16 lg:px-8 lg:py-24">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Advanced Healthcare
                <span className="text-primary-600 block">Powered by AI</span>
              </h1>
              <p className="text-lg text-gray-600 leading-relaxed">
                Emily Multispeciality Hospital combines cutting-edge medical technology with compassionate care.
                Our AI-powered systems ensure accurate diagnoses and personalized treatment plans for every patient.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <button className="bg-primary-600 hover:bg-primary-700 text-white font-medium px-6 py-3 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2">
                <span>Book Appointment</span>
                <ArrowRight className="w-4 h-4" />
              </button>
              <button className="bg-white hover:bg-gray-50 text-primary-600 font-medium px-6 py-3 rounded-lg border border-primary-600 transition-colors duration-200">
                Learn More
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 pt-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">15+</div>
                <div className="text-sm text-gray-600">Years Experience</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">50K+</div>
                <div className="text-sm text-gray-600">Patients Served</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">98%</div>
                <div className="text-sm text-gray-600">Success Rate</div>
              </div>
            </div>
          </div>

          {/* Right Content - Features */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Shield className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">AI-Powered Diagnostics</h3>
                  <p className="text-sm text-gray-600">Advanced machine learning algorithms for accurate and fast diagnoses</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Clock className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">24/7 Emergency Care</h3>
                  <p className="text-sm text-gray-600">Round-the-clock emergency services with rapid response teams</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Award className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Expert Medical Team</h3>
                  <p className="text-sm text-gray-600">Board-certified specialists across all medical disciplines</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;