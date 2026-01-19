@echo off
REM Emily Hospital Frontend - Environment Setup Script (Windows)

echo 🔧 Setting up Emily Hospital Frontend Environment
echo ==================================================
echo.

REM Check if .env.local already exists
if exist ".env.local" (
    echo ⚠️  .env.local file already exists!
    set /p response="Do you want to overwrite it? (y/N): "
    if /i not "!response!"=="y" if /i not "!response!"=="Y" (
        echo Setup cancelled.
        pause
        exit /b 0
    )
)

echo 📝 Creating .env.local file...

(
echo # Supabase Configuration for Emily Hospital
echo # Get these values from https://supabase.com dashboard ^> Settings ^> API
echo.
echo # Replace with your actual Supabase project URL
echo VITE_SUPABASE_URL=https://your-project-id.supabase.co
echo.
echo # Replace with your actual Supabase anon key
echo VITE_SUPABASE_ANON_KEY=your-anon-key-here-replace-with-actual-key
echo.
echo # Example of what real values look like:
echo # VITE_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
echo # VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
) > .env.local

echo ✅ .env.local file created successfully!
echo.
echo 📋 Next Steps:
echo 1. Go to https://supabase.com and create a new project
echo 2. Go to Settings → API in your Supabase dashboard
echo 3. Copy your Project URL and replace VITE_SUPABASE_URL
echo 4. Copy your anon/public key and replace VITE_SUPABASE_ANON_KEY
echo 5. Restart your development server: npm run dev
echo.
echo 🚀 Happy coding!
pause