import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Package, Users, TrendingUp, Shield, Leaf, Sprout, Heart, Globe, CheckCircle } from 'lucide-react';

// Example products for display on home page - one of each type
const exampleProducts = [
  {
    id: 1,
    name: 'Organic Tomatoes',
    type: 'Vegetables',
    description: 'Fresh, juicy organic tomatoes grown without pesticides using sustainable farming methods.',
    location: 'Boumerdes , Algerie',
    farmer: 'Green Valley Farm',
    image: 'https://images.unsplash.com/photo-1621872320280-10fbec0c171c?w=900&auto=format&fit=crop&q=60'
  },
  {
    id: 2,
    name: 'Organic Strawberries',
    type: 'Fruits',
    description: 'Sweet, juicy organic strawberries grown using natural pest control methods. Packed with antioxidants.',
    location: 'Boufarik , Blida',
    farmer: 'Local Farmer',
    image: 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 3,
    name: 'Pure Forest Honey',
    type: 'Honey',
    description: 'Natural raw honey collected from forest hives. Unprocessed, rich in antioxidants and nutrients.',
    location: 'Tizi Ouzou, Algerie',
    farmer: 'Bee Nature Cooperative',
    image: 'https://images.unsplash.com/photo-1564550171000-626d4d651b9d?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  },
  {
    id: 4,
    name: 'Fresh Cow Milk Derivatives',
    type: 'Milk Derivatives',
    description: 'Locally produced dairy products including cheese and fermented milk. Made from fresh cow milk.',
    location: 'Setif, Algerie',
    farmer: 'Dairy Valley Farm',
    image: 'https://images.unsplash.com/photo-1654184750621-1110fe5afcdc?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2hlZXN8ZW58MHx8MHx8fDA%3D'
  }
];

export const Home = () => {
  const { user } = useAuth();

  return (
    <div className="relative min-h-[calc(100vh-200px)] rounded-lg overflow-hidden">
      {/* Background Image with Overlay */}
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1625246333195-78d9c38ad449?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80)',
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-green-900/75 via-green-800/65 to-green-900/75"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 p-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-green-900/95 to-emerald-600/95 backdrop-blur-sm text-white rounded-lg p-12 mb-8 text-center shadow-2xl">
        <h1 className="text-5xl font-bold mb-4">Welcome to BioSouk</h1>
        <p className="text-xl mb-8">Connect farmers, transporters, and buyers in one platform</p>
        {!user && (
          <div className="space-x-4">
            <Link
              to="/register"
              className="inline-block px-6 py-3 bg-white text-green-700 rounded-lg font-semibold hover:bg-green-50 transition"
            >
              Get Started
            </Link>
            <Link
              to="/login"
              className="inline-block px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-500 transition"
            >
              Login
            </Link>
          </div>
        )}
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white/95 backdrop-blur-sm p-6 rounded-lg shadow-md">
          <Package className="w-12 h-12 text-green-700 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Product Management</h3>
          <p className="text-gray-600">
            Farmers can easily list and manage their products with photos and details.
          </p>
        </div>

        <div className="bg-white/95 backdrop-blur-sm p-6 rounded-lg shadow-md">
          <Users className="w-12 h-12 text-green-700 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Farmer Applications</h3>
          <p className="text-gray-600">
            Apply to become a verified farmer and start selling your products.
          </p>
        </div>

        <div className="bg-white/95 backdrop-blur-sm p-6 rounded-lg shadow-md">
          <Shield className="w-12 h-12 text-green-700 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Secure Platform</h3>
          <p className="text-gray-600">
            Secure authentication and session management for all users.
          </p>
        </div>
      </div>

      {/* Bio Agriculture Benefits Section */}
      <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow-md p-8 mb-8">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Leaf className="w-12 h-12 text-green-700" />
          </div>
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Why Choose Bio Agriculture?</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Discover the benefits of sustainable, organic farming that nurtures both the environment and your health.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <Heart className="w-8 h-8 text-green-700" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Healthier Food</h3>
            <p className="text-gray-600 text-sm">
              Organic produce is free from harmful pesticides and chemicals, providing you with nutrient-rich, natural food.
            </p>
          </div>

          <div className="text-center">
            <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <Globe className="w-8 h-8 text-green-700" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Environmental Protection</h3>
            <p className="text-gray-600 text-sm">
              Bio agriculture preserves soil health, protects biodiversity, and reduces pollution for a sustainable future.
            </p>
          </div>

          <div className="text-center">
            <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <Sprout className="w-8 h-8 text-green-700" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Soil Regeneration</h3>
            <p className="text-gray-600 text-sm">
              Organic farming methods improve soil fertility naturally, ensuring long-term agricultural productivity.
            </p>
          </div>

          <div className="text-center">
            <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-8 h-8 text-green-700" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Certified Quality</h3>
            <p className="text-gray-600 text-sm">
              All products meet strict organic standards, verified by certified farmers and quality assurance processes.
            </p>
          </div>
        </div>
      </div>

      {/* Sustainable Practices Section */}
      <div className="bg-gradient-to-r from-green-700/95 to-emerald-700/95 backdrop-blur-sm rounded-lg shadow-md p-8 mb-8 text-white">
        <h2 className="text-3xl font-bold mb-6 text-center">Sustainable Farming Practices</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-3">Crop Rotation</h3>
            <p className="text-white/90">
              Our farmers use crop rotation techniques to maintain soil nutrients naturally, reducing the need for chemical fertilizers.
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-3">Natural Pest Control</h3>
            <p className="text-white/90">
              Biological pest management methods protect crops while preserving beneficial insects and ecosystem balance.
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-3">Water Conservation</h3>
            <p className="text-white/90">
              Efficient irrigation systems and water management practices ensure sustainable use of this precious resource.
            </p>
          </div>
        </div>
      </div>

      {/* Example Products Section */}
      <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow-md p-8 mb-8">
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Example Products</h2>
          <p className="text-gray-600">Discover fresh, organic produce from verified farmers</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {exampleProducts.map((product) => (
            <div key={product.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition border border-green-100">
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xl font-semibold text-gray-800">{product.name}</h3>
                  <span className="text-xs font-medium text-green-700 bg-green-50 px-2 py-1 rounded-full">
                    {product.type}
                  </span>
                </div>
                <p className="text-gray-600 text-sm mb-4 leading-relaxed">{product.description}</p>
                <div className="pt-3 border-t border-gray-100">
                  <p className="text-sm text-gray-500 mb-1">📍 {product.location}</p>
                  <p className="text-sm text-gray-500">By: {product.farmer}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      {user && (
        <div className="bg-white/95 backdrop-blur-sm p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">Quick Actions</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {user.user_type === 'farmer' && (
              <>
                <Link
                  to="/products/create"
                  className="p-4 border-2 border-green-700 rounded-lg hover:bg-green-50 transition text-center"
                >
                  <TrendingUp className="w-8 h-8 text-green-700 mx-auto mb-2" />
                  <span className="font-semibold">Add New Product</span>
                </Link>
              </>
            )}
            <Link
              to="/products"
              className="p-4 border-2 border-emerald-700 rounded-lg hover:bg-emerald-50 transition text-center"
            >
              <Package className="w-8 h-8 text-emerald-700 mx-auto mb-2" />
              <span className="font-semibold">Browse Products</span>
            </Link>
          </div>
        </div>
      )}
      </div>
    </div>
  );
};

