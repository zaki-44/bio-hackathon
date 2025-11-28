import { useState, useEffect } from "react";
import { farmerAPI } from "../services/api";
import {
  CheckCircle,
  XCircle,
  Clock,
  BarChart3,
  FileText,
  Eye,
} from "lucide-react";

export const Admin = () => {
  const [applications, setApplications] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [processing, setProcessing] = useState<number | null>(null);

  useEffect(() => {
    loadApplications();
    loadStats();
  }, [statusFilter]);

  const loadApplications = async () => {
    try {
      setLoading(true);
      const result = await farmerAPI.getApplications(statusFilter || undefined);
      setApplications(result.applications || []);
      console.log("Applications loaded:", result);
    } catch (error: any) {
      console.error("Failed to load applications:", error);
      alert(
        `Failed to load applications: ${
          error.message || "Unknown error"
        }\n\nMake sure you are logged in as admin.`
      );
      setApplications([]);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const result = await farmerAPI.getStats();
      setStats(result.stats);
    } catch (error: any) {
      console.error("Failed to load stats:", error);
      console.error("Error details:", error.message);
    }
  };

  const handleApprove = async (id: number) => {
    setProcessing(id);
    try {
      await farmerAPI.approveApplication(id);
      await loadApplications();
      await loadStats();
      alert("Application approved successfully!");
    } catch (error: any) {
      console.error("Approval error:", error);
      alert(
        error.message ||
          "Failed to approve application. Please check the console for details."
      );
    } finally {
      setProcessing(null);
    }
  };

  const handleDeny = async (id: number) => {
    const reason = prompt("Enter reason for denial (optional):");
    if (reason === null) return; // User cancelled

    setProcessing(id);
    try {
      await farmerAPI.denyApplication(id, reason || undefined);
      await loadApplications();
      await loadStats();
      alert("Application denied successfully!");
    } catch (error: any) {
      console.error("Denial error:", error);
      alert(
        error.message ||
          "Failed to deny application. Please check the console for details."
      );
    } finally {
      setProcessing(null);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "approved":
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case "denied":
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-yellow-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "approved":
        return "bg-green-100 text-green-800";
      case "denied":
        return "bg-red-100 text-red-800";
      default:
        return "bg-yellow-100 text-yellow-800";
    }
  };

  // Check if user is admin
  if (user?.user_type !== "admin") {
    return (
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8 text-center">
        <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Access Denied</h2>
        <p className="text-gray-600">
          You must be logged in as an admin to access this page.
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Current user type: {user?.user_type || "Not logged in"}
        </p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Admin Dashboard</h2>
      {user && (
        <p className="text-sm text-gray-600 mb-4">
          Logged in as: <span className="font-semibold">{user.username}</span> (
          {user.user_type})
        </p>
      )}

      {/* Stats */}
      {stats && (
        <div className="grid md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total</p>
                <p className="text-2xl font-bold text-gray-800">
                  {stats.total}
                </p>
              </div>
              <BarChart3 className="w-8 h-8 text-green-700" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Pending</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {stats.pending}
                </p>
              </div>
              <Clock className="w-8 h-8 text-yellow-600" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Approved</p>
                <p className="text-2xl font-bold text-green-600">
                  {stats.approved}
                </p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Denied</p>
                <p className="text-2xl font-bold text-red-600">
                  {stats.denied}
                </p>
              </div>
              <XCircle className="w-8 h-8 text-red-600" />
            </div>
          </div>
        </div>
      )}

      {/* Filter */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-700 focus:border-transparent"
        >
          <option value="">All Applications</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="denied">Denied</option>
        </select>
      </div>

      {/* Applications List */}
      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Loading applications...</p>
        </div>
      ) : applications.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow-md">
          <p className="text-gray-600">No applications found.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {applications.map((app) => (
            <div key={app.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    {getStatusIcon(app.status)}
                    <h3 className="text-xl font-semibold text-gray-800">
                      {app.farm_name}
                    </h3>
                    <span
                      className={`px-2 py-1 rounded text-sm ${getStatusColor(
                        app.status
                      )}`}
                    >
                      {app.status}
                    </span>
                  </div>
                  <p className="text-gray-600">Username: {app.username}</p>
                  <p className="text-gray-600">Email: {app.email}</p>
                  <p className="text-gray-600">Location: {app.location}</p>
                  {app.phone && (
                    <p className="text-gray-600">Phone: {app.phone}</p>
                  )}
                  {app.description && (
                    <p className="text-gray-600 mt-2">{app.description}</p>
                  )}
                  {app.denial_reason && (
                    <p className="text-red-600 mt-2">
                      Reason: {app.denial_reason}
                    </p>
                  )}
                  {app.certification_url && (
                    <div className="mt-3">
                      <a
                        href={`http://localhost:5000${app.certification_url}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
                      >
                        <FileText className="w-4 h-4" />
                        <span>View Certification</span>
                        <Eye className="w-4 h-4" />
                      </a>
                    </div>
                  )}
                  <p className="text-sm text-gray-500 mt-2">
                    Applied: {new Date(app.created_at).toLocaleDateString()}
                  </p>
                </div>
                {app.status === "pending" && (
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleApprove(app.id)}
                      disabled={processing === app.id}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50"
                    >
                      {processing === app.id ? "Processing..." : "Approve"}
                    </button>
                    <button
                      onClick={() => handleDeny(app.id)}
                      disabled={processing === app.id}
                      className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition disabled:opacity-50"
                    >
                      {processing === app.id ? "Processing..." : "Deny"}
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
