# SkillAtlas - API Keys and Configuration Guide

This document lists all required API keys and configuration for the SkillAtlas application.

## Required API Keys

### 1. Hugging Face API Key (REQUIRED)
**Purpose:** Powers all AI features including CV parsing, skill extraction, roadmap generation, and chat assistant.

**How to get it:**
1. Go to [https://huggingface.co](https://huggingface.co)
2. Create a free account or sign in
3. Go to Settings → Access Tokens
4. Click "New token"
5. Give it a name (e.g., "SkillAtlas")
6. Select "Read" access
7. Copy the generated token

**Add to `.env` file:**
```env
HUGGINGFACE_API_KEY=hf_your_actual_api_key_here
```

**Models used:**
- Text Generation: `mistralai/Mixtral-8x7B-Instruct-v0.1`
- You can customize models in `server/huggingface.ts`

**Free tier:** Yes, with rate limits. For production, consider upgrading to PRO.

---

### 2. Database Configuration (REQUIRED)
**Purpose:** PostgreSQL database for user accounts, sessions, skills, and roadmaps.

**Configuration (already set up in docker-compose.yaml):**
```env
DATABASE_URL=postgresql://skillatlas:skillatlas123@localhost:5432/skillatlas
```

**To start database:**
```bash
docker-compose up -d
```

---

### 3. Session Secret (REQUIRED)
**Purpose:** Secures user sessions and cookies.

**Add to `.env` file:**
```env
SESSION_SECRET=your-random-secret-key-min-32-chars
```

**Generate a secure secret:**
```bash
# On Windows PowerShell:
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# On Linux/Mac:
openssl rand -base64 32
```

---

### 4. MongoDB Configuration (OPTIONAL)
**Purpose:** Stores skills data and learning resources.

**Configuration:**
```env
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=skillatlas
```

**Note:** Already configured in docker-compose.yaml

---

### 5. Neo4j Configuration (OPTIONAL)
**Purpose:** Knowledge graph for skill relationships and prerequisites.

**Configuration:**
```env
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=skillatlas123
```

**Note:** Already configured in docker-compose.yaml

---

## Complete .env File Template

Create a `.env` file in `Frontend/AIOverview/` with these contents:

```env
# Database Configuration (REQUIRED)
DATABASE_URL=postgresql://skillatlas:skillatlas123@localhost:5432/skillatlas
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=skillatlas

# Neo4j Configuration
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=skillatlas123

# Hugging Face Configuration (REQUIRED)
HUGGINGFACE_API_KEY=your-huggingface-api-key-here

# Session Secret (REQUIRED - Generate a random string)
SESSION_SECRET=your-random-secret-key-at-least-32-characters-long

# Application Settings
NODE_ENV=development
PORT=5000
VITE_API_URL=http://localhost:5000
```

---

## Setup Steps

1. **Install Dependencies:**
   ```bash
   cd Frontend/AIOverview
   npm install
   ```

2. **Start Docker Services:**
   ```bash
   cd ../../  # Go to project root
   docker-compose up -d
   ```

3. **Configure Environment:**
   - Copy the `.env` template above
   - Add your Hugging Face API key
   - Generate and add a SESSION_SECRET

4. **Initialize Database:**
   ```bash
   cd Frontend/AIOverview
   npx drizzle-kit push
   npx tsx populate_users.ts  # Optional: Create test users
   ```

5. **Start Development Server:**
   ```bash
   npx tsx server/index-dev.ts
   ```

6. **Access Application:**
   - Open http://localhost:5000
   - Register a new account or use test account:
     - Email: demo@skillatlas.com
     - Password: demo123

---

## Cost Breakdown

### Free Tier Available:
- **Hugging Face:** Free with rate limits (3,000 requests/month)
- **PostgreSQL:** Free (self-hosted via Docker)
- **MongoDB:** Free (self-hosted via Docker)
- **Neo4j:** Free (self-hosted via Docker)

### Production Considerations:
- **Hugging Face PRO:** $9/month for higher rate limits
- **Managed Databases:** Consider cloud hosting for production
  - Railway, Render, or Supabase for PostgreSQL
  - MongoDB Atlas for MongoDB
  - Neo4j Aura for Neo4j

---

## Troubleshooting

### Issue: "HUGGINGFACE_API_KEY is not configured"
- Ensure your `.env` file has `HUGGINGFACE_API_KEY` set
- Restart the server after updating `.env`

### Issue: Database connection errors
- Run `docker-compose up -d` to start databases
- Check `docker ps` to ensure containers are running
- Verify DATABASE_URL in `.env` matches docker-compose.yaml

### Issue: Rate limiting from Hugging Face
- You're hitting free tier limits
- Consider upgrading to PRO tier
- Implement caching for AI responses

---

## Alternative AI Models

You can switch models in `server/huggingface.ts`:

```typescript
const MODELS = {
  TEXT_GENERATION: 'mistralai/Mixtral-8x7B-Instruct-v0.1',
  // Alternatives:
  // 'meta-llama/Llama-2-70b-chat-hf'
  // 'tiiuae/falcon-180B-chat'
  // 'mistralai/Mistral-7B-Instruct-v0.2'
};
```

---

## Security Notes

- **Never commit `.env` file to version control**
- Use strong SESSION_SECRET in production
- Change default database passwords in production
- Use HTTPS in production (set NODE_ENV=production)
- Rotate API keys regularly

---

## Need Help?

Check the application logs for detailed error messages:
```bash
cd Frontend/AIOverview
npx tsx server/index-dev.ts
```
