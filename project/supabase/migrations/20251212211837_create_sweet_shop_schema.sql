/*
  # Sweet Shop Management System Database Schema

  ## Overview
  This migration sets up the complete database schema for a sweet shop management system
  with user authentication, role-based access control, inventory management, and purchase tracking.

  ## New Tables

  ### 1. `profiles`
  Extends Supabase auth.users with additional user information
  - `id` (uuid, primary key) - References auth.users(id)
  - `email` (text) - User's email address
  - `full_name` (text) - User's full name
  - `role` (text) - User role: 'user' or 'admin'
  - `created_at` (timestamptz) - Account creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### 2. `sweets`
  Stores information about sweets in inventory
  - `id` (uuid, primary key) - Unique identifier
  - `name` (text) - Sweet name
  - `description` (text) - Detailed description
  - `category` (text) - Category (e.g., 'chocolate', 'gummy', 'hard candy')
  - `price` (numeric) - Price per unit
  - `quantity` (integer) - Current stock quantity
  - `image_url` (text) - URL to product image
  - `created_at` (timestamptz) - Creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### 3. `purchases`
  Tracks all purchase transactions
  - `id` (uuid, primary key) - Unique identifier
  - `user_id` (uuid) - References profiles(id)
  - `sweet_id` (uuid) - References sweets(id)
  - `quantity` (integer) - Quantity purchased
  - `total_price` (numeric) - Total transaction price
  - `purchased_at` (timestamptz) - Purchase timestamp

  ## Security

  ### Row Level Security (RLS)
  All tables have RLS enabled with the following policies:

  #### Profiles Table:
  - Users can view their own profile
  - Users can update their own profile (except role)
  - Admins can view all profiles

  #### Sweets Table:
  - All authenticated users can view sweets
  - Only admins can insert, update, or delete sweets

  #### Purchases Table:
  - Users can view their own purchases
  - Users can create their own purchases
  - Admins can view all purchases

  ## Notes
  - Default role for new users is 'user'
  - All timestamps use timestamptz for timezone awareness
  - Prices use numeric(10,2) for precise decimal handling
  - Foreign key constraints ensure data integrity
*/

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email text NOT NULL,
  full_name text DEFAULT '',
  role text NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create sweets table
CREATE TABLE IF NOT EXISTS sweets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text DEFAULT '',
  category text NOT NULL,
  price numeric(10,2) NOT NULL CHECK (price >= 0),
  quantity integer NOT NULL DEFAULT 0 CHECK (quantity >= 0),
  image_url text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create purchases table
CREATE TABLE IF NOT EXISTS purchases (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  sweet_id uuid NOT NULL REFERENCES sweets(id) ON DELETE CASCADE,
  quantity integer NOT NULL CHECK (quantity > 0),
  total_price numeric(10,2) NOT NULL CHECK (total_price >= 0),
  purchased_at timestamptz DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sweets_category ON sweets(category);
CREATE INDEX IF NOT EXISTS idx_sweets_name ON sweets(name);
CREATE INDEX IF NOT EXISTS idx_purchases_user_id ON purchases(user_id);
CREATE INDEX IF NOT EXISTS idx_purchases_sweet_id ON purchases(sweet_id);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE sweets ENABLE ROW LEVEL SECURITY;
ALTER TABLE purchases ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id AND role = (SELECT role FROM profiles WHERE id = auth.uid()));

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Admins can view all profiles"
  ON profiles FOR SELECT
  TO authenticated
  USING ((SELECT role FROM profiles WHERE id = auth.uid()) = 'admin');

-- Sweets policies
CREATE POLICY "Anyone can view sweets"
  ON sweets FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Admins can insert sweets"
  ON sweets FOR INSERT
  TO authenticated
  WITH CHECK ((SELECT role FROM profiles WHERE id = auth.uid()) = 'admin');

CREATE POLICY "Admins can update sweets"
  ON sweets FOR UPDATE
  TO authenticated
  USING ((SELECT role FROM profiles WHERE id = auth.uid()) = 'admin')
  WITH CHECK ((SELECT role FROM profiles WHERE id = auth.uid()) = 'admin');

CREATE POLICY "Admins can delete sweets"
  ON sweets FOR DELETE
  TO authenticated
  USING ((SELECT role FROM profiles WHERE id = auth.uid()) = 'admin');

-- Purchases policies
CREATE POLICY "Users can view own purchases"
  ON purchases FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can create own purchases"
  ON purchases FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Admins can view all purchases"
  ON purchases FOR SELECT
  TO authenticated
  USING ((SELECT role FROM profiles WHERE id = auth.uid()) = 'admin');

-- Function to automatically create profile on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name)
  VALUES (new.id, new.email, COALESCE(new.raw_user_meta_data->>'full_name', ''));
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create profile on signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
DROP TRIGGER IF EXISTS set_updated_at_profiles ON profiles;
CREATE TRIGGER set_updated_at_profiles
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS set_updated_at_sweets ON sweets;
CREATE TRIGGER set_updated_at_sweets
  BEFORE UPDATE ON sweets
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- Insert some sample sweets data
INSERT INTO sweets (name, description, category, price, quantity, image_url) VALUES
  ('Milk Chocolate Bar', 'Smooth and creamy milk chocolate', 'chocolate', 2.99, 100, 'https://images.pexels.com/photos/65882/chocolate-dark-coffee-confiserie-65882.jpeg'),
  ('Gummy Bears', 'Colorful fruity gummy bears', 'gummy', 1.99, 150, 'https://images.pexels.com/photos/33454/people-child-baby-newborn.jpg'),
  ('Lollipops', 'Assorted flavored lollipops', 'hard candy', 0.99, 200, 'https://images.pexels.com/photos/3854816/pexels-photo-3854816.jpeg'),
  ('Dark Chocolate Truffles', 'Rich dark chocolate truffles with cocoa dusting', 'chocolate', 4.99, 75, 'https://images.pexels.com/photos/918327/pexels-photo-918327.jpeg'),
  ('Sour Worms', 'Tangy sour gummy worms', 'gummy', 2.49, 120, 'https://images.pexels.com/photos/3943757/pexels-photo-3943757.jpeg'),
  ('Peppermint Candy', 'Classic peppermint hard candy', 'hard candy', 1.49, 180, 'https://images.pexels.com/photos/4016173/pexels-photo-4016173.jpeg'),
  ('White Chocolate Bar', 'Sweet and smooth white chocolate', 'chocolate', 3.49, 90, 'https://images.pexels.com/photos/4110404/pexels-photo-4110404.jpeg'),
  ('Fruit Jellies', 'Soft fruit-flavored jellies', 'gummy', 2.99, 110, 'https://images.pexels.com/photos/4110256/pexels-photo-4110256.jpeg'),
  ('Butterscotch Discs', 'Traditional butterscotch hard candy', 'hard candy', 1.79, 160, 'https://images.pexels.com/photos/3668871/pexels-photo-3668871.jpeg'),
  ('Caramel Chocolates', 'Milk chocolate with gooey caramel center', 'chocolate', 3.99, 85, 'https://images.pexels.com/photos/3997609/pexels-photo-3997609.jpeg')
ON CONFLICT DO NOTHING;