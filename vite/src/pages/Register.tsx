import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { UserPlus, Upload, FileText, CheckCircle } from 'lucide-react';

export const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    user_type: 'user' as 'farmer' | 'transporter' | 'user',
    certification: null as File | null,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [certificateUploaded, setCertificateUploaded] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type (PDF)
      if (file.type !== 'application/pdf') {
        setError('Please upload a PDF file');
        return;
      }
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError('File size must be less than 5MB');
        return;
      }
      setFormData({ ...formData, certification: file });
      setCertificateUploaded(true);
      setError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    // Validate farmer certification
    if (formData.user_type === 'farmer' && !formData.certification) {
      setError('Please upload your organic certification document');
      return;
    }
    
    setLoading(true);

    try {
      if (formData.user_type === 'farmer') {
        // For farmers, register with certification file
        await register(
          formData.username,
          formData.email,
          formData.password,
          formData.user_type,
          formData.certification || undefined
        );
        // Show success message and redirect to pending page
        alert('Your farmer application has been submitted! Please wait for admin approval.');
        navigate('/farmer-pending');
      } else {
        // For other user types, register normally
        await register(formData.username, formData.email, formData.password, formData.user_type);
        navigate('/');
      }
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8">
      <div className="text-center mb-6">
        <UserPlus className="w-12 h-12 text-green-700 mx-auto mb-4" />
        <h2 className="text-3xl font-bold text-gray-800">Create Account</h2>
        <p className="text-gray-600 mt-2">Join our platform today</p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Username
          </label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-700 focus:border-transparent"
            placeholder="Choose a username"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-700 focus:border-transparent"
            placeholder="your@email.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-700 focus:border-transparent"
            placeholder="Create a password"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            User Type
          </label>
          <select
            name="user_type"
            value={formData.user_type}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-700 focus:border-transparent"
          >
            <option value="user">User</option>
            <option value="farmer">Farmer</option>
            <option value="transporter">Transporter</option>
          </select>
        </div>

        {/* Certification Upload - Only shown for farmers */}
        {formData.user_type === 'farmer' && (
          <div className="border-t border-gray-200 pt-4 mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Organic Certification Document <span className="text-red-500">*</span>
            </label>
            <div className="bg-green-50 border-2 border-dashed border-green-300 rounded-lg p-6">
              <div className="flex flex-col items-center">
                <Upload className="w-10 h-10 text-green-700 mb-3" />
                <h4 className="mb-2 text-gray-800 font-medium">Upload Organic Certificate</h4>
                <p className="text-sm text-gray-600 mb-4 text-center">
                  Please upload your organic farming certification (PDF, max 5MB)
                </p>
                
                <label className="cursor-pointer">
                  <input
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                  <div className="flex items-center gap-2 px-6 py-3 bg-green-700 text-white rounded-lg hover:bg-green-800 transition-colors">
                    <FileText className="w-5 h-5" />
                    <span>{certificateUploaded ? 'Change Certificate' : 'Choose File'}</span>
                  </div>
                </label>

                {certificateUploaded && formData.certification && (
                  <div className="mt-4 flex items-center gap-2 text-green-700">
                    <CheckCircle className="w-5 h-5" />
                    <span className="text-sm font-medium">{formData.certification.name}</span>
                  </div>
                )}
              </div>
            </div>
            <p className="mt-2 text-xs text-gray-500">
              Your registration will be pending until an admin verifies your organic certificate.
            </p>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-green-700 to-emerald-700 text-white py-3 rounded-lg font-semibold hover:from-green-800 hover:to-emerald-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating account...' : 'Register'}
        </button>
      </form>

      <p className="mt-6 text-center text-gray-600">
        Already have an account?{' '}
        <Link to="/login" className="text-green-700 hover:text-green-800 font-semibold">
          Login here
        </Link>
      </p>
    </div>
  );
};

