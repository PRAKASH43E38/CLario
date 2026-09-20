import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const Profile: React.FC = () => {
  const navigate = useNavigate();
  const { refreshUser } = useAuth();
  const [formData, setFormData] = useState({
    name: 'Alex Learner',
    age_range: '20-24',
    education_level: 'Undergraduate',
    domain: 'Computer Science',
    prior_learning: 'Basic Python & Algebra',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await api.put('/onboarding/profile', formData);
      await refreshUser();
      navigate('/mindset');
    } catch (err) {
      console.error('Failed to save profile:', err);
      setError('Could not save profile details. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="bg-white p-10 rounded-3xl border-2 border-gray-200 shadow-xl max-w-lg w-full">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-green-500 text-white font-black text-xl flex items-center justify-center">
            1
          </div>
          <div>
            <h1 className="text-2xl font-black text-gray-900">Basic Learner Profile</h1>
            <p className="text-xs font-bold text-gray-400 uppercase">Step 1 of 2</p>
          </div>
        </div>

        {error && <div className="p-3 mb-6 bg-red-50 text-red-600 rounded-xl text-sm font-bold">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Your Full Name</label>
            <input
              type="text"
              name="name"
              required
              value={formData.name}
              onChange={handleChange}
              className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Age Range</label>
              <select
                name="age_range"
                value={formData.age_range}
                onChange={handleChange}
                className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none"
              >
                <option value="under_18">Under 18</option>
                <option value="18-24">18 - 24</option>
                <option value="25-34">25 - 34</option>
                <option value="35_plus">35+</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Education Level</label>
              <select
                name="education_level"
                value={formData.education_level}
                onChange={handleChange}
                className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none"
              >
                <option value="High School">High School</option>
                <option value="Undergraduate">Undergraduate</option>
                <option value="Postgraduate">Postgraduate</option>
                <option value="Self-Taught">Self-Taught</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Domain / Field of Study</label>
            <input
              type="text"
              name="domain"
              required
              value={formData.domain}
              onChange={handleChange}
              placeholder="e.g. Computer Science, Physics, Business"
              className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Prior Learning / Experience</label>
            <textarea
              name="prior_learning"
              value={formData.prior_learning}
              onChange={handleChange}
              placeholder="What topics or skills are you already familiar with?"
              className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none min-h-24"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-500 hover:bg-green-600 disabled:opacity-50 text-white font-extrabold text-lg py-4 rounded-2xl border-b-4 border-green-700 active:border-b-0 active:translate-y-1 transition-all cursor-pointer shadow-md mt-4"
          >
            {loading ? 'Saving...' : 'Next: 5 Mindset Questions →'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Profile;
