import { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import { supabase } from '../lib/supabase';
import { Sweet } from '../types';
import { useAuth } from '../contexts/AuthContext';
import { Header } from './Header';
import { SearchFilters } from './SearchFilters';
import { SweetCard } from './SweetCard';
import { AddSweetModal } from './AddSweetModal';

export function Dashboard() {
  const { isAdmin } = useAuth();
  const [sweets, setSweets] = useState<Sweet[]>([]);
  const [filteredSweets, setFilteredSweets] = useState<Sweet[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);

  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  const categories = Array.from(new Set(sweets.map((s) => s.category)));

  useEffect(() => {
    fetchSweets();
  }, []);

  useEffect(() => {
    filterSweets();
  }, [sweets, searchTerm, selectedCategory, minPrice, maxPrice]);

  const fetchSweets = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('sweets')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) throw error;
      setSweets(data || []);
    } catch (error: any) {
      console.error('Error fetching sweets:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterSweets = () => {
    let filtered = [...sweets];

    if (searchTerm) {
      filtered = filtered.filter((sweet) =>
        sweet.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (selectedCategory) {
      filtered = filtered.filter((sweet) => sweet.category === selectedCategory);
    }

    if (minPrice) {
      filtered = filtered.filter((sweet) => sweet.price >= parseFloat(minPrice));
    }

    if (maxPrice) {
      filtered = filtered.filter((sweet) => sweet.price <= parseFloat(maxPrice));
    }

    setFilteredSweets(filtered);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-orange-50 to-amber-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold text-gray-800">Our Sweet Collection</h2>
            <p className="text-gray-600 mt-1">
              Discover and purchase delicious sweets
            </p>
          </div>

          {isAdmin && (
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center space-x-2 bg-gradient-to-r from-orange-400 to-pink-500 text-white font-semibold px-6 py-3 rounded-lg hover:from-orange-500 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl"
            >
              <Plus className="w-5 h-5" />
              <span>Add Sweet</span>
            </button>
          )}
        </div>

        <SearchFilters
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          selectedCategory={selectedCategory}
          setSelectedCategory={setSelectedCategory}
          minPrice={minPrice}
          setMinPrice={setMinPrice}
          maxPrice={maxPrice}
          setMaxPrice={setMaxPrice}
          categories={categories}
        />

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-orange-500 mx-auto"></div>
            <p className="mt-4 text-gray-600 font-medium">Loading sweets...</p>
          </div>
        ) : filteredSweets.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-xl shadow-md">
            <p className="text-xl text-gray-600">No sweets found matching your criteria</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredSweets.map((sweet) => (
              <SweetCard key={sweet.id} sweet={sweet} onUpdate={fetchSweets} />
            ))}
          </div>
        )}
      </main>

      {showAddModal && (
        <AddSweetModal
          onClose={() => setShowAddModal(false)}
          onSuccess={fetchSweets}
        />
      )}
    </div>
  );
}
