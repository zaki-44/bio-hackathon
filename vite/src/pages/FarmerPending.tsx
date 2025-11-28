import { Link } from "react-router-dom";
import { Clock, CheckCircle, Mail } from "lucide-react";

export default function FarmerPending() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#EAFBF0] to-[#D1FAE5] px-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-2xl text-center">
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 bg-yellow-100 rounded-full flex items-center justify-center">
            <Clock className="w-10 h-10 text-yellow-600" />
          </div>
        </div>

        <h1 className="text-3xl font-bold text-gray-800 mb-4">
          Application Pending Review
        </h1>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
          <p className="text-gray-700 mb-4">
            Thank you for submitting your farmer application! Your registration
            is currently pending admin review.
          </p>
          <p className="text-gray-600 text-sm mb-4">
            Our admin team will review your organic certification document and
            application details. You will be notified via email once your
            application has been reviewed.
          </p>
          <div className="flex items-center justify-center gap-2 text-yellow-700">
            <Mail className="w-5 h-5" />
            <span className="text-sm">Check your email for updates</span>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center justify-center gap-2">
            <CheckCircle className="w-5 h-5 text-blue-600" />
            What happens next?
          </h3>
          <ul className="text-left text-gray-600 space-y-2 text-sm">
            <li>• Admin reviews your organic certification document</li>
            <li>• Your application details are verified</li>
            <li>• You'll receive an email notification with the decision</li>
            <li>• If approved, you can log in and start listing products</li>
          </ul>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/"
            className="px-6 py-3 bg-[#16A34A] text-white rounded-lg hover:bg-[#15803d] transition-colors"
          >
            Back to Home
          </Link>
          <Link
            to="/login"
            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Go to Login
          </Link>
        </div>
      </div>
    </div>
  );
}
