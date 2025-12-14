import { useAuth } from '../contexts/AuthContext';
import { LogOut, Candy, Shield, User } from 'lucide-react';

export function Header() {
  const { user, signOut, isAdmin } = useAuth();

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-pink-500 rounded-full flex items-center justify-center shadow-lg">
              <Candy className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Sweet Shop</h1>
              <p className="text-sm text-gray-600">Management System</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-semibold text-gray-800">{user?.full_name || user?.email}</p>
              <div className="flex items-center justify-end space-x-1 text-xs text-gray-600">
                {isAdmin ? (
                  <>
                    <Shield className="w-3 h-3" />
                    <span>Administrator</span>
                  </>
                ) : (
                  <>
                    <User className="w-3 h-3" />
                    <span>User</span>
                  </>
                )}
              </div>
            </div>

            <button
              onClick={() => signOut()}
              className="flex items-center space-x-2 bg-gradient-to-r from-orange-400 to-pink-500 text-white px-4 py-2 rounded-lg hover:from-orange-500 hover:to-pink-600 transition-all shadow-md hover:shadow-lg font-semibold"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
