import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { productAPI, ratingAPI } from "../services/api";
import { useCart } from "../contexts/CartContext";
import { useAuth } from "../contexts/AuthContext";
import {
  Package,
  Star,
  ShoppingCart,
  Heart,
  ArrowLeft,
  MapPin,
  User,
  Calendar,
  CheckCircle,
  XCircle,
} from "lucide-react";

export const ProductDetail = () => {
  const { productId } = useParams<{ productId: string }>();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { user } = useAuth();
  const [product, setProduct] = useState<any>(null);
  const [farmerRating, setFarmerRating] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [addingToCart, setAddingToCart] = useState(false);
  const [buying, setBuying] = useState(false);

  useEffect(() => {
    if (productId) {
      loadProduct();
    }
  }, [productId]);

  const loadProduct = async () => {
    try {
      setLoading(true);
      setError("");
      const result = await productAPI.getById(parseInt(productId!));
      setProduct(result.product);

      // Load farmer rating if farmer_id exists
      if (result.product.farmer_id) {
        try {
          const ratingResult = await ratingAPI.getRating(
            result.product.farmer_id
          );
          setFarmerRating(ratingResult);
        } catch (err) {
          console.error("Failed to load farmer rating:", err);
        }
      }
    } catch (err: any) {
      setError(err.message || "Failed to load product");
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    if (!user) {
      navigate("/login");
      return;
    }

    setAddingToCart(true);
    try {
      // Add product to cart with specified quantity
      for (let i = 0; i < quantity; i++) {
        addToCart(product);
      }
      // Show success message (you can use a toast library here)
      alert("Product added to cart!");
    } catch (err: any) {
      alert(err.message || "Failed to add to cart");
    } finally {
      setAddingToCart(false);
    }
  };

  const handleBuyNow = async () => {
    if (!user) {
      navigate("/login");
      return;
    }

    setBuying(true);
    try {
      // Add to cart first
      for (let i = 0; i < quantity; i++) {
        addToCart(product);
      }
      // Navigate to checkout/cart page
      navigate("/cart");
    } catch (err: any) {
      alert(err.message || "Failed to proceed to checkout");
    } finally {
      setBuying(false);
    }
  };

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
      );
    }

    if (hasHalfStar && fullStars < 5) {
      stars.push(
        <Star
          key="half"
          className="w-5 h-5 fill-yellow-400 text-yellow-400 opacity-50"
        />
      );
    }

    for (let i = fullStars + (hasHalfStar ? 1 : 0); i < 5; i++) {
      stars.push(<Star key={i} className="w-5 h-5 text-gray-300" />);
    }

    return stars;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-700 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading product...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error || "Product not found"}
        </div>
        <Link
          to="/products"
          className="inline-flex items-center gap-2 text-green-700 hover:text-green-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Products
        </Link>
      </div>
    );
  }

  const imageUrl = product.photo_url
    ? `http://localhost:5000${product.photo_url}`
    : null;

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Back Button */}
      <Link
        to="/products"
        className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Products
      </Link>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Product Image */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt={product.name}
              className="w-full h-96 object-cover"
              onError={(e) => {
                (e.target as HTMLImageElement).style.display = "none";
                (
                  e.target as HTMLImageElement
                ).nextElementSibling?.classList.remove("hidden");
              }}
            />
          ) : null}
          <div
            className={`w-full h-96 flex items-center justify-center bg-gray-100 ${imageUrl ? "hidden" : ""
              }`}
          >
            <Package className="w-32 h-32 text-gray-400" />
          </div>
        </div>

        {/* Product Details */}
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              {product.name}
            </h1>
            {product.category && (
              <span className="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm mb-4">
                {product.category}
              </span>
            )}
          </div>

          {/* Price */}
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-bold text-green-700">
              {product.price} DA
            </span>
            <span className="text-gray-600">per {product.unit}</span>
          </div>

          {/* Availability */}
          <div className="flex items-center gap-2">
            {product.is_available ? (
              <>
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="text-green-600 font-medium">In Stock</span>
              </>
            ) : (
              <>
                <XCircle className="w-5 h-5 text-red-600" />
                <span className="text-red-600 font-medium">Out of Stock</span>
              </>
            )}
            <span className="text-gray-600">
              ({product.quantity} {product.unit} available)
            </span>
          </div>

          {/* Description */}
          {product.description && (
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                Description
              </h3>
              <p className="text-gray-600">{product.description}</p>
            </div>
          )}

          {/* Location */}
          {product.location && (
            <div className="flex items-center gap-2 text-gray-600">
              <MapPin className="w-5 h-5" />
              <span>{product.location}</span>
            </div>
          )}

          {/* Farmer Information with Rating */}
          {product.farmer && (
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <User className="w-5 h-5 text-gray-600" />
                  <span className="font-semibold text-gray-800">
                    {product.farmer_username || product.farmer.username}
                  </span>
                </div>
                {product.farmer.average_rating !== null && (
                  <div className="flex items-center gap-2">
                    <div className="flex items-center">
                      {renderStars(product.farmer.average_rating)}
                    </div>
                    <span className="text-sm font-medium text-gray-700">
                      {product.farmer.average_rating.toFixed(1)}
                    </span>
                    {product.farmer.rating_count > 0 && (
                      <span className="text-sm text-gray-500">
                        ({product.farmer.rating_count}{" "}
                        {product.farmer.rating_count === 1
                          ? "rating"
                          : "ratings"}
                        )
                      </span>
                    )}
                  </div>
                )}
              </div>
              {farmerRating && farmerRating.total_ratings > 0 && (
                <div className="mt-2 text-sm text-gray-600">
                  <p>
                    Average rating: {farmerRating.average_rating?.toFixed(1)}{" "}
                    stars from {farmerRating.total_ratings}{" "}
                    {farmerRating.total_ratings === 1 ? "review" : "reviews"}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Quantity Selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quantity
            </label>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                -
              </button>
              <input
                type="number"
                min="1"
                max={product.quantity}
                value={quantity}
                onChange={(e) =>
                  setQuantity(
                    Math.max(
                      1,
                      Math.min(product.quantity, parseInt(e.target.value) || 1)
                    )
                  )
                }
                className="w-20 px-3 py-2 border border-gray-300 rounded-lg text-center"
              />
              <button
                onClick={() =>
                  setQuantity(Math.min(product.quantity, quantity + 1))
                }
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                +
              </button>
              <span className="text-gray-600">{product.unit}</span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={handleAddToCart}
              disabled={!product.is_available || addingToCart}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-green-700 text-white rounded-lg hover:bg-green-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ShoppingCart className="w-5 h-5" />
              {addingToCart ? "Adding..." : "Add to Cart"}
            </button>
            <button
              onClick={handleBuyNow}
              disabled={!product.is_available || buying}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-green-700 to-emerald-700 text-white rounded-lg hover:from-green-800 hover:to-emerald-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {buying ? "Processing..." : "Buy Now"}
            </button>
          </div>

          {/* Created Date */}
          {product.created_at && (
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <Calendar className="w-4 h-4" />
              <span>
                Listed on {new Date(product.created_at).toLocaleDateString()}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
