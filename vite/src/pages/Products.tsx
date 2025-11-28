import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productAPI } from '../services/api';
import { Search, Package, Plus } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export const Products = () => {
  const { user } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await productAPI.search(searchQuery);
      setProducts(result.products);
    } catch (err: any) {
      setError(err.message || 'Search failed');
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Products</h2>
        {user?.user_type === 'farmer' && (
          <Link
            to="/products/create"
            className="flex items-center space-x-2 px-4 py-2 bg-green-700 text-white rounded-lg hover:bg-green-800 transition"
          >
            <Plus className="w-5 h-5" />
            <span>Add Product</span>
          </Link>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex space-x-2">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Search for products..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-700 focus:border-transparent"
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-6 py-2 bg-gradient-to-r from-green-700 to-emerald-700 text-white rounded-lg hover:from-green-800 hover:to-emerald-800 transition disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {products.length === 0 && !loading && searchQuery && (
        <div className="text-center py-12 bg-white rounded-lg shadow-md">
          <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No products found. Try a different search term.</p>
        </div>
      )}

      {!searchQuery && (
        <div className="text-center py-12 bg-white rounded-lg shadow-md">
          <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">Enter a search query to find products.</p>
        </div>
      )}

      <div className="grid md:grid-cols-3 gap-6">
        {products.map((product) => (
          <div key={product.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
            {product.photo_url && (
              <img
                src={`http://localhost:5000${product.photo_url}`}
                alt={product.name}
                className="w-full h-48 object-cover"
              />
            )}
            <div className="p-4">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{product.name}</h3>
              {product.description && (
                <p className="text-gray-600 text-sm mb-2 line-clamp-2">{product.description}</p>
              )}
              <div className="flex items-center justify-between mt-4">
                <span className="text-2xl font-bold text-green-700">
                  ${product.price}
                </span>
                <span className="text-gray-600">
                  {product.quantity} {product.unit}
                </span>
              </div>
              {product.location && (
                <p className="text-sm text-gray-500 mt-2">📍 {product.location}</p>
              )}
              {product.farmer_username && (
                <p className="text-sm text-gray-500 mt-1">By: {product.farmer_username}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

