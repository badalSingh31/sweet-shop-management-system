export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'user' | 'admin';
  created_at: string;
}

export interface Sweet {
  id: string;
  name: string;
  description: string;
  category: string;
  price: number;
  quantity: number;
  image_url: string;
  created_at: string;
  updated_at: string;
}

export interface Purchase {
  id: string;
  user_id: string;
  sweet_id: string;
  quantity: number;
  total_price: number;
  purchased_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
