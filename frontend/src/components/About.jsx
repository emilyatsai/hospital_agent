import { Users, Target, Award, Heart } from 'lucide-react';

const About = () => {
  const stats = [
    { icon: Users, value: "500+", label: "Expert Doctors" },
    { icon: Heart, value: "50K+", label: "Patients Cared For" },
    { icon: Award, value: "25+", label: "Years of Excellence" },
    { icon: Target, value: "98%", label: "Patient Satisfaction" }
  ];

  const values = [
    {
      title: "Patient-Centered Care",
      description: "We put our patients at the heart of everything we do, ensuring personalized care and attention to individual needs."
    },
    {
      title: "Innovation & Technology",
      description: "We embrace cutting-edge medical technology and AI solutions to provide the best possible healthcare outcomes."
    },
    {
      title: "Compassion & Excellence",
      description: "Our dedicated team combines medical expertise with genuine compassion to deliver exceptional care."
    },
    {
      title: "Community Health",
      description: "We are committed to improving the health and well-being of our community through preventive care and education."
    }
  ];

  return (
    <section id="about" className="bg-gray-50 px-6 py-16 lg:px-8 lg:py-24">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left Content */}
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
                About Emily Multispeciality Hospital
              </h2>
              <div className="w-20 h-1 bg-primary-600 rounded-full mb-6"></div>
            </div>

            <p className="text-lg text-gray-600 leading-relaxed">
              For over two decades, Emily Multispeciality Hospital has been a beacon of excellence in healthcare,
              combining traditional medical wisdom with cutting-edge AI technology to deliver unparalleled patient care.
            </p>

            <p className="text-lg text-gray-600 leading-relaxed">
              Our commitment to innovation, compassion, and medical excellence has made us a trusted healthcare
              partner for families across the region. We continuously invest in the latest medical technologies
              and maintain the highest standards of patient safety and care quality.
            </p>

            <div className="grid grid-cols-2 gap-6 pt-4">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <stat.icon className="w-6 h-6 text-primary-600" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                  <div className="text-sm text-gray-600">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Right Content - Values */}
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-8">Our Core Values</h3>
            <div className="space-y-6">
              {values.map((value, index) => (
                <div key={index} className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">
                    {value.title}
                  </h4>
                  <p className="text-gray-600 leading-relaxed">
                    {value.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;