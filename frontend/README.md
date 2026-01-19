# Emily Multispeciality Hospital Frontend

A modern React application for the Emily Multispeciality Hospital with AI-powered healthcare features.

## Features

- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Authentication**: Supabase-powered user authentication
- **Modern UI**: Clean, professional healthcare interface
- **Routing**: React Router for seamless navigation
- **Real-time Updates**: Live authentication state management

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **Supabase** - Authentication and backend services
- **React Router** - Client-side routing
- **Lucide React** - Beautiful icons

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Configuration

**Quick Setup (Recommended):**

Run the automated setup script:

```bash
# On macOS/Linux
./setup-env.sh

# On Windows
setup-env.bat
```

This will create a `.env.local` file with placeholder values that you can then customize.

**Manual Setup:**

If you prefer to create the file manually:

```bash
# Create the environment file
touch .env.local
```

Then add your Supabase configuration to `.env.local`:

```env
# Supabase Configuration
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here-replace-with-actual-key
```

**Example with real values:**
```env
VITE_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY0MzI1NzYwMCwiZXhwIjoxOTU4ODMzNjAwfQ.sample-jwt-token-here
```

### 3. Supabase Setup

#### Step 1: Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Fill in your project details:
   - **Name**: Emily Hospital
   - **Database Password**: Choose a strong password
   - **Region**: Select the closest region to your users

#### Step 2: Get API Credentials
1. Go to **Settings** → **API** in your Supabase dashboard
2. Copy the **Project URL** (something like `https://abcdefghijklmnop.supabase.co`)
3. Copy the **anon/public** key (starts with `eyJ...`)

#### Step 3: Configure Environment Variables
Add these values to your `.env.local` file:

```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

#### Step 4: Configure Authentication (Optional)
In your Supabase dashboard:
- Go to **Authentication** → **Settings**
- Configure email templates if needed
- Set up any additional auth providers (Google, GitHub, etc.)

#### Step 5: Database Setup (for production)
When you're ready to deploy:
- Go to **Settings** → **Database**
- Note the connection details for your backend
- Set up Row Level Security (RLS) policies for your tables

### 4. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### 5. Test Your Setup

**Before configuring Supabase:**
- The app will show a "Authentication is not configured" error
- You can still explore the UI and navigation

**After configuring Supabase:**
- Try registering a new account on the login page
- Check your email for verification
- Try logging in with the new account
- The authentication should work seamlessly

**Troubleshooting:**
- If you still see connection errors, double-check your Supabase URL and key
- Make sure your Supabase project is active and not paused
- Restart the development server after updating environment variables

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Header.jsx      # Navigation header
│   │   ├── Hero.jsx        # Landing page hero section
│   │   ├── LoginPage.jsx   # Authentication page
│   │   └── ...             # Other components
│   ├── contexts/           # React contexts
│   │   └── AuthContext.jsx # Authentication context
│   ├── lib/               # Utility libraries
│   │   └── supabase.js    # Supabase client configuration
│   ├── App.jsx            # Main application component
│   └── main.jsx           # Application entry point
├── public/                # Static assets
└── index.html            # HTML template
```

## Authentication Flow

### User Registration
1. User fills registration form with email, password, and profile info
2. Supabase sends confirmation email
3. User clicks email link to verify account
4. Account is activated and user can sign in

### User Login
1. User enters email and password
2. Supabase validates credentials
3. JWT token is issued for authenticated requests
4. User is redirected to dashboard

### Protected Routes
- Dashboard and user-specific pages require authentication
- Unauthenticated users are redirected to login page
- Authentication state is managed globally via React Context

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Deployment

### Vercel Deployment

1. Connect your GitHub repository to Vercel
2. Add environment variables in Vercel dashboard:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
3. Deploy automatically on push to main branch

### Manual Deployment

```bash
npm run build
# Deploy the dist/ folder to your hosting service
```

## Key Components

### Authentication Components
- **LoginPage**: Complete login/register form with validation
- **AuthContext**: Global authentication state management
- **Protected Routes**: Route guards for authenticated users

### UI Components
- **Header**: Navigation with auth-aware menu
- **Hero**: Landing page with dynamic CTAs
- **Services**: Healthcare services showcase
- **About**: Hospital information section
- **Contact**: Contact form and information

## API Integration

The frontend is designed to work with the FastAPI backend. Authentication tokens from Supabase can be used to authenticate requests to the backend API.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.