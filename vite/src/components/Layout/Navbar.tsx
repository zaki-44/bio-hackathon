import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { LogOut, User, Home , Leaf } from "lucide-react";

export const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <nav className="bg-gradient-to-r from-green-700 to-emerald-700 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link
            to="/"
            className="flex items-center space-x-2 text-2xl font-bold"
          >
            {/* <Package className="w-8 h-8" /> */}
            <Leaf className=" w-8 h-8" />
            <span>BioSouk</span>
          </Link>

          <div className="flex items-center space-x-6">
            <Link
              to="/"
              className="flex items-center space-x-1 hover:text-green-200 transition"
            >
              <Home className="w-5 h-5" />
              <span>Home</span>
            </Link>

            {user ? (
              <>
                <Link
                  to="/products"
                  className="hover:text-green-200 transition"
                >
                  Products
                </Link>
                {user.user_type === "farmer" && (
                  <Link
                    to="/products/create"
                    className="hover:text-green-200 transition"
                  >
                    Add Product
                  </Link>
                )}
                {user.user_type === "admin" && (
                  <Link to="/admin" className="hover:text-green-200 transition">
                    Admin
                  </Link>
                )}
                <div className="flex items-center space-x-2">
                  <User className="w-5 h-5" />
                  <span>{user.username}</span>
                  <span className="px-2 py-1 bg-green-600 rounded text-sm">
                    {user.user_type}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 px-4 py-2 bg-red-500 hover:bg-red-600 rounded transition"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="hover:text-green-200 transition">
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-white text-green-700 rounded hover:bg-green-50 transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
