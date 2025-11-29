import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { orderAPI } from '../services/order';
import { Trash2, ShoppingBag, ArrowRight, CheckCircle } from 'lucide-react';

export const Cart = () => {
    const { cart, removeFromCart, updateCartItem, clearCart, getCartTotal } = useCart();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const handleCheckout = async () => {
        setLoading(true);
        setError('');

        try {
            await orderAPI.create(cart);
            setSuccess(true);
            clearCart();
            // Optional: Redirect after a delay
            setTimeout(() => {
                navigate('/products');
            }, 3000);
        } catch (err: any) {
            setError(err.message || 'Checkout failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <div className="max-w-2xl mx-auto px-4 py-16 text-center">
                <div className="bg-green-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
                    <CheckCircle className="w-10 h-10 text-green-600" />
                </div>
                <h2 className="text-3xl font-bold text-gray-800 mb-4">Order Placed Successfully!</h2>
                <p className="text-gray-600 mb-8">
                    Thank you for your purchase. Your order has been received and is being processed.
                </p>
                <Link
                    to="/products"
                    className="inline-flex items-center gap-2 px-6 py-3 bg-green-700 text-white rounded-lg hover:bg-green-800 transition"
                >
                    Continue Shopping
                    <ArrowRight className="w-4 h-4" />
                </Link>
            </div>
        );
    }

    if (cart.length === 0) {
        return (
            <div className="max-w-2xl mx-auto px-4 py-16 text-center">
                <div className="bg-gray-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
                    <ShoppingBag className="w-10 h-10 text-gray-400" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Your Cart is Empty</h2>
                <p className="text-gray-600 mb-8">
                    Looks like you haven't added any products to your cart yet.
                </p>
                <Link
                    to="/products"
                    className="inline-flex items-center gap-2 px-6 py-3 bg-green-700 text-white rounded-lg hover:bg-green-800 transition"
                >
                    Browse Products
                    <ArrowRight className="w-4 h-4" />
                </Link>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-8 flex items-center gap-3">
                <ShoppingBag className="w-8 h-8 text-green-700" />
                Your Cart
            </h1>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                    {error}
                </div>
            )}

            <div className="grid md:grid-cols-3 gap-8">
                {/* Cart Items */}
                <div className="md:col-span-2 space-y-4">
                    {cart.map((item) => (
                        <div key={item.id} className="bg-white rounded-lg shadow-md p-4 flex gap-4">
                            {item.photo_url ? (
                                <img
                                    src={`http://localhost:5000${item.photo_url}`}
                                    alt={item.name}
                                    className="w-24 h-24 object-cover rounded-md"
                                />
                            ) : (
                                <div className="w-24 h-24 bg-gray-100 rounded-md flex items-center justify-center">
                                    <ShoppingBag className="w-8 h-8 text-gray-400" />
                                </div>
                            )}

                            <div className="flex-1">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="text-lg font-semibold text-gray-800">{item.name}</h3>
                                        <p className="text-sm text-gray-500">
                                            Sold by: {item.farmer_username || 'Unknown Farmer'}
                                        </p>
                                    </div>
                                    <button
                                        onClick={() => removeFromCart(item.id)}
                                        className="text-red-500 hover:text-red-700 p-1"
                                        title="Remove item"
                                    >
                                        <Trash2 className="w-5 h-5" />
                                    </button>
                                </div>

                                <div className="flex justify-between items-end mt-4">
                                    <div className="flex items-center gap-3">
                                        <button
                                            onClick={() => updateCartItem(item.id, Math.max(1, item.quantity - 1))}
                                            className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded hover:bg-gray-50"
                                        >
                                            -
                                        </button>
                                        <span className="w-8 text-center font-medium">{item.quantity}</span>
                                        <button
                                            onClick={() => updateCartItem(item.id, item.quantity + 1)}
                                            className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded hover:bg-gray-50"
                                        >
                                            +
                                        </button>
                                        <span className="text-gray-500 text-sm ml-2">{item.unit}</span>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-lg font-bold text-green-700">
                                            {(item.price * item.quantity).toFixed(2)} DA
                                        </p>
                                        <p className="text-sm text-gray-500">
                                            {item.price} DA / {item.unit}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Order Summary */}
                <div className="md:col-span-1">
                    <div className="bg-white rounded-lg shadow-md p-6 sticky top-24">
                        <h2 className="text-xl font-bold text-gray-800 mb-4">Order Summary</h2>

                        <div className="space-y-3 mb-6">
                            <div className="flex justify-between text-gray-600">
                                <span>Subtotal</span>
                                <span>{getCartTotal().toFixed(2)} DA</span>
                            </div>
                            <div className="flex justify-between text-gray-600">
                                <span>Shipping</span>
                                <span className="text-green-600">Free</span>
                            </div>
                            <div className="border-t pt-3 flex justify-between font-bold text-lg text-gray-800">
                                <span>Total</span>
                                <span>{getCartTotal().toFixed(2)} DA</span>
                            </div>
                        </div>

                        <button
                            onClick={handleCheckout}
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-green-700 to-emerald-700 text-white py-3 rounded-lg font-semibold hover:from-green-800 hover:to-emerald-800 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                'Processing...'
                            ) : (
                                <>
                                    Checkout
                                    <ArrowRight className="w-5 h-5" />
                                </>
                            )}
                        </button>

                        <p className="text-xs text-gray-500 mt-4 text-center">
                            By proceeding, you agree to our Terms of Service and Privacy Policy.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};
