import {
  Heart,
  Brain,
  Bone,
  Eye,
  Stethoscope,
  Microscope,
  Ambulance,
  Activity
} from 'lucide-react';

const Services = () => {
  const services = [
    {
      icon: Heart,
      title: "Cardiology",
      description: "Advanced cardiac care with AI-assisted diagnosis and minimally invasive procedures.",
      features: ["ECG Monitoring", "Cardiac Surgery", "Heart Health Screening"]
    },
    {
      icon: Brain,
      title: "Neurology",
      description: "Comprehensive neurological care using cutting-edge technology and AI diagnostics.",
      features: ["Brain Imaging", "Stroke Treatment", "Neurological Surgery"]
    },
    {
      icon: Bone,
      title: "Orthopedics",
      description: "Expert orthopedic care for bones, joints, and musculoskeletal conditions.",
      features: ["Joint Replacement", "Sports Medicine", "Fracture Care"]
    },
    {
      icon: Eye,
      title: "Ophthalmology",
      description: "Complete eye care services from routine exams to advanced surgical procedures.",
      features: ["Vision Correction", "Cataract Surgery", "Retinal Treatment"]
    },
    {
      icon: Stethoscope,
      title: "Internal Medicine",
      description: "Comprehensive primary care and internal medicine services for all ages.",
      features: ["Preventive Care", "Chronic Disease Management", "Health Screenings"]
    },
    {
      icon: Microscope,
      title: "Laboratory Services",
      description: "State-of-the-art laboratory with AI-powered analysis and rapid results.",
      features: ["Blood Tests", "Pathology", "Molecular Diagnostics"]
    },
    {
      icon: Ambulance,
      title: "Emergency Care",
      description: "24/7 emergency services with rapid response and critical care capabilities.",
      features: ["Trauma Care", "Critical Care", "Emergency Surgery"]
    },
    {
      icon: Activity,
      title: "AI Health Monitoring",
      description: "Personalized health monitoring using AI algorithms and wearable technology.",
      features: ["Vital Signs Tracking", "Predictive Analytics", "Remote Monitoring"]
    }
  ];

  return (
    <section id="services" className="bg-white px-6 py-16 lg:px-8 lg:py-24">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Our Medical Services
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            We offer comprehensive healthcare services powered by advanced AI technology
            and delivered by our expert medical professionals.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {services.map((service, index) => (
            <div
              key={index}
              className="bg-gray-50 rounded-xl p-6 hover:shadow-lg transition-shadow duration-300 border border-gray-100"
            >
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <service.icon className="w-6 h-6 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                {service.title}
              </h3>
              <p className="text-gray-600 mb-4 text-sm leading-relaxed">
                {service.description}
              </p>
              <ul className="space-y-1">
                {service.features.map((feature, idx) => (
                  <li key={idx} className="text-sm text-gray-500 flex items-center">
                    <div className="w-1.5 h-1.5 bg-primary-400 rounded-full mr-2"></div>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <button className="bg-primary-600 hover:bg-primary-700 text-white font-medium px-6 py-3 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl">
            View All Services
          </button>
        </div>
      </div>
    </section>
  );
};

export default Services;