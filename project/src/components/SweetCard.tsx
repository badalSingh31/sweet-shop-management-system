import { useState } from 'react';
import { Sweet } from '../types';
import { ShoppingCart, Package, Edit, Trash2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

interface SweetCardProps {
  sweet: Sweet;
  onUpdate: () => void;
}

export function SweetCard({ sweet, onUpdate }: SweetCardProps) {
  const { isAdmin } = useAuth();
  const [purchasing, setPurchasing] = useState(false);
  const [quantity, setQuantity] = useState(1);
  const [showPurchase, setShowPurchase] = useState(false);
  const [restockQuantity, setRestockQuantity] = useState(10);
  const [showRestock, setShowRestock] = useState(false);

  const handlePurchase = async () => {
    if (quantity > sweet.quantity || quantity < 1) return;

    setPurchasing(true);
    try {
      const { error } = await supabase
        .from('purchases')
        .insert({
          user_id: (await supabase.auth.getUser()).data.user!.id,
          sweet_id: sweet.id,
          quantity,
          total_price: sweet.price * quantity,
        });

      if (error) throw error;

      await supabase
        .from('sweets')
        .update({ quantity: sweet.quantity - quantity })
        .eq('id', sweet.id);

      setShowPurchase(false);
      setQuantity(1);
      onUpdate();
    } catch (error: any) {
      alert('Purchase failed: ' + error.message);
    } finally {
      setPurchasing(false);
    }
  };

  const handleRestock = async () => {
    if (restockQuantity < 1) return;

    try {
      const { error } = await supabase
        .from('sweets')
        .update({ quantity: sweet.quantity + restockQuantity })
        .eq('id', sweet.id);

      if (error) throw error;

      setShowRestock(false);
      setRestockQuantity(10);
      onUpdate();
    } catch (error: any) {
      alert('Restock failed: ' + error.message);
    }
  };

  const handleDelete = async () => {
    if (!confirm(`Are you sure you want to delete "${sweet.name}"?`)) return;

    try {
      const { error } = await supabase.from('sweets').delete().eq('id', sweet.id);
      if (error) throw error;
      onUpdate();
    } catch (error: any) {
      alert('Delete failed: ' + error.message);
    }
  };

  return (
    <>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
        <div className="aspect-video bg-gradient-to-br from-orange-100 to-pink-100 relative overflow-hidden">
          {sweet.image_url ? (
            <img
              src={sweet.image_url}
              alt={sweet.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <Package className="w-16 h-16 text-orange-300" />
            </div>
          )}
          <div className="absolute top-3 right-3 bg-white px-3 py-1 rounded-full shadow-md">
            <span className="text-sm font-bold text-orange-500">${sweet.price.toFixed(2)}</span>
          </div>
        </div>

        <div className="p-5">
          <div className="flex items-start justify-between mb-2">
            <h3 className="text-xl font-bold text-gray-800 flex-1">{sweet.name}</h3>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-orange-100 text-orange-800 ml-2">
              {sweet.category}
            </span>
          </div>

          <p className="text-gray-600 text-sm mb-4 line-clamp-2">{sweet.description}</p>

          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <Package className="w-4 h-4 text-gray-500" />
              <span className={`text-sm font-semibold ${sweet.quantity === 0 ? 'text-red-500' : 'text-gray-700'}`}>
                {sweet.quantity === 0 ? 'Out of Stock' : `${sweet.quantity} in stock`}
              </span>
            </div>
          </div>

          <div className="space-y-2">
            <button
              onClick={() => setShowPurchase(true)}
              disabled={sweet.quantity === 0}
              className="w-full bg-gradient-to-r from-orange-400 to-pink-500 text-white font-semibold py-2.5 px-4 rounded-lg hover:from-orange-500 hover:to-pink-600 transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              <ShoppingCart className="w-4 h-4" />
              <span>Purchase</span>
            </button>

            {isAdmin && (
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => setShowRestock(true)}
                  className="bg-blue-500 text-white font-semibold py-2 px-3 rounded-lg hover:bg-blue-600 transition-all text-sm"
                >
                  <Package className="w-4 h-4 mx-auto" />
                </button>
                <button
                  className="bg-green-500 text-white font-semibold py-2 px-3 rounded-lg hover:bg-green-600 transition-all text-sm"
                >
                  <Edit className="w-4 h-4 mx-auto" />
                </button>
                <button
                  onClick={handleDelete}
                  className="bg-red-500 text-white font-semibold py-2 px-3 rounded-lg hover:bg-red-600 transition-all text-sm"
                >
                  <Trash2 className="w-4 h-4 mx-auto" />
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {showPurchase && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Purchase {sweet.name}</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Quantity (Max: {sweet.quantity})
                </label>
                <input
                  type="number"
                  min="1"
                  max={sweet.quantity}
                  value={quantity}
                  onChange={(e) => setQuantity(Number(e.target.value))}
                  className="w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-orange-400 focus:outline-none"
                />
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-gray-700">Total:</span>
                  <span className="text-2xl font-bold text-orange-500">
                    ${(sweet.price * quantity).toFixed(2)}
                  </span>
                </div>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowPurchase(false)}
                  className="flex-1 bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={handlePurchase}
                  disabled={purchasing || quantity > sweet.quantity || quantity < 1}
                  className="flex-1 bg-gradient-to-r from-orange-400 to-pink-500 text-white font-semibold py-2 px-4 rounded-lg hover:from-orange-500 hover:to-pink-600 transition-all disabled:opacity-50"
                >
                  {purchasing ? 'Processing...' : 'Confirm Purchase'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {showRestock && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Restock {sweet.name}</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Quantity to Add
                </label>
                <input
                  type="number"
                  min="1"
                  value={restockQuantity}
                  onChange={(e) => setRestockQuantity(Number(e.target.value))}
                  className="w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-400 focus:outline-none"
                />
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">Current Stock:</span>
                  <span className="font-semibold">{sweet.quantity}</span>
                </div>
                <div className="flex justify-between items-center text-sm mt-2">
                  <span className="text-gray-600">New Stock:</span>
                  <span className="font-bold text-blue-600">{sweet.quantity + restockQuantity}</span>
                </div>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowRestock(false)}
                  className="flex-1 bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={handleRestock}
                  disabled={restockQuantity < 1}
                  className="flex-1 bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-600 transition-all disabled:opacity-50"
                >
                  Confirm Restock
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
