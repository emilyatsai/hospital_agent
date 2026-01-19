# Environment Setup Instructions

## Creating .env.local File

Run this command in your terminal to create the environment file:

```bash
cd frontend
touch .env.local
```

Then copy and paste this content into `.env.local`:

```
# Supabase Configuration
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here-replace-with-actual-key
```

## Getting Supabase Credentials

1. Go to https://supabase.com
2. Create a new project or use existing one
3. Go to Settings → API
4. Copy the Project URL and anon key
5. Replace the placeholder values above

## Example with Real Values

```
VITE_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY0MzI1NzYwMCwiZXhwIjoxOTU4ODMzNjAwfQ.sample-jwt-token-here
```

## Testing

After setting up the environment file:
1. Restart your development server: `npm run dev`
2. The authentication should now work with Supabase