#!/bin/bash

# Emily Hospital Frontend - Environment Setup Script

echo "🔧 Setting up Emily Hospital Frontend Environment"
echo "=================================================="
echo ""

# Check if .env.local already exists
if [ -f ".env.local" ]; then
    echo "⚠️  .env.local file already exists!"
    echo "Do you want to overwrite it? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

echo "📝 Creating .env.local file..."
cat > .env.local << 'EOF'
# Supabase Configuration for Emily Hospital
# Get these values from https://supabase.com dashboard > Settings > API

# Replace with your actual Supabase project URL
VITE_SUPABASE_URL=https://your-project-id.supabase.co

# Replace with your actual Supabase anon key
VITE_SUPABASE_ANON_KEY=your-anon-key-here-replace-with-actual-key

# Example of what real values look like:
# VITE_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
# VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
EOF

echo "✅ .env.local file created successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://supabase.com and create a new project"
echo "2. Go to Settings → API in your Supabase dashboard"
echo "3. Copy your Project URL and replace VITE_SUPABASE_URL"
echo "4. Copy your anon/public key and replace VITE_SUPABASE_ANON_KEY"
echo "5. Restart your development server: npm run dev"
echo ""
echo "🚀 Happy coding!"