import { Phone, MapPin, Clock, Mail, Send } from 'lucide-react';

const Contact = () => {
  const contactInfo = [
    {
      icon: Phone,
      title: "Phone",
      details: ["+1 (555) 123-4567", "+1 (555) 123-4568"],
      description: "24/7 Emergency Hotline"
    },
    {
      icon: MapPin,
      title: "Address",
      details: ["123 Health Street", "Medical City, MC 12345"],
      description: "Main Hospital Location"
    },
    {
      icon: Clock,
      title: "Hours",
      details: ["Mon-Fri: 8:00 AM - 8:00 PM", "Sat-Sun: 9:00 AM - 6:00 PM"],
      description: "Emergency services available 24/7"
    },
    {
      icon: Mail,
      title: "Email",
      details: ["info@emilyhospital.com", "appointments@emilyhospital.com"],
      description: "General inquiries and appointments"
    }
  ];

  return (
    <section id="contact" className="bg-white px-6 py-16 lg:px-8 lg:py-24">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Contact Us
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Get in touch with our healthcare professionals. We're here to help you with all your medical needs.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Contact Information */}
          <div className="space-y-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Get In Touch</h3>
            <div className="grid gap-6">
              {contactInfo.map((info, index) => (
                <div key={index} className="flex items-start space-x-4 p-6 bg-gray-50 rounded-xl">
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <info.icon className="w-6 h-6 text-primary-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">{info.title}</h4>
                    {info.details.map((detail, idx) => (
                      <p key={idx} className="text-gray-600">{detail}</p>
                    ))}
                    <p className="text-sm text-gray-500 mt-1">{info.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Contact Form */}
          <div className="bg-gray-50 rounded-xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Send us a Message</h3>
            <form className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    First Name
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
                    placeholder="John"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Last Name
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
                    placeholder="Doe"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
                  placeholder="john.doe@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number
                </label>
                <input
                  type="tel"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
                  placeholder="+1 (555) 123-4567"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Message
                </label>
                <textarea
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors resize-none"
                  placeholder="Please describe your inquiry or concern..."
                ></textarea>
              </div>

              <button
                type="submit"
                className="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium px-6 py-3 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
              >
                <span>Send Message</span>
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;