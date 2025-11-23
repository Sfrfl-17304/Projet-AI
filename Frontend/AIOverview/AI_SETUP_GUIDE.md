# SkillAtlas Frontend - Quick Setup Guide

Complete guide to setting up and running the SkillAtlas frontend application.

## 📦 Prerequisites

- Node.js 18+ and npm
- PostgreSQL database
- OpenAI API key (for AI features)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Optional: Replit account for authentication

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd Frontend/AIOverview
npm install
```

This will install:
- React 18 & React DOM
- TypeScript & Vite
- TanStack Query for state management
- shadcn/ui component library
- Express server dependencies
- Drizzle ORM for database
- OpenAI SDK
- And 60+ other packages

**Note**: First installation may take 3-5 minutes.

### Step 2: Configure Environment

Create a `.env` file in the `Frontend/AIOverview` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/skillatlas

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Replit Auth (if using Replit)
REPLIT_APP_NAME=your-replit-app-name

# Session Secret
SESSION_SECRET=your-secure-random-session-secret-here

# Application Settings
NODE_ENV=development
PORT=5000
VITE_API_URL=http://localhost:5000
```

**Important**: 
- Replace database credentials with your PostgreSQL connection
- Get OpenAI API key from https://platform.openai.com/api-keys
- Generate session secret: `openssl rand -hex 32`

### Step 3: Setup Database

Create the PostgreSQL database:

```bash
# Using psql
psql -U postgres
CREATE DATABASE skillatlas;
\q
```

Push the schema to database:

```bash
npm run db:push
```

This creates all 12 tables with proper relations.

### Step 4: Seed Database (Optional)

To add initial data (roles, skills, resources):

```bash
# Run the seed script
tsx server/run-seed.ts
```

This populates:
- 50+ career roles
- 100+ skills
- Learning resources
- Skill prerequisites

### Step 5: Start Development Server

```bash
npm run dev
```

This starts:
- Vite dev server on port 5173 (frontend)
- Express API server on port 5000 (backend)
- Hot module reload enabled

### Step 6: Open Application

Visit: **http://localhost:5173**

You should see the landing page!

---

## 🧪 Testing Features

### 1. Test Authentication

**Sign In:**
1. Click "Get Started" on landing page
2. If using Replit: authenticate with Replit account
3. If local dev: mock authentication will work
4. Should redirect to dashboard

### 2. Test CV Upload

**Upload a CV:**
```bash
# Create a test CV file
echo "Software Engineer

Skills:
- Python programming with 5 years experience
- React and TypeScript for frontend development
- PostgreSQL and MongoDB databases
- Docker and Kubernetes for DevOps
- Machine learning with TensorFlow

Experience:
- Built web applications
- Deployed scalable systems
" > test_cv.txt

# Convert to PDF (or use a real PDF)
# Upload through the Analysis page
```

**Steps:**
1. Navigate to Analysis page
2. Drag and drop or click to upload PDF
3. Wait for AI extraction (~3-5 seconds)
4. View extracted skills with categories

**Expected Response:**
- Technical skills: Python, React, TypeScript, PostgreSQL, etc.
- Soft skills: Leadership, Communication (if mentioned)
- Total skill count displayed
- Skills categorized

### 3. Test Career Exploration

**Browse Roles:**
1. Navigate to Careers page
2. See list of career roles with cards
3. Filter by category (sidebar)
4. Click on a role to see details
5. View required skills and descriptions

**Expected:**
- Multiple role cards displayed
- Categories: Engineering, Data, Design, etc.
- Each card shows: title, description, salary, demand

### 4. Test Skill Gap Analysis

**Analyze Gap:**
1. Upload a CV first (if not done)
2. On Analysis page, select a target role
3. Click "Analyze Gap"
4. View missing skills and match percentage

**Expected Response:**
```json
{
  "roleName": "Data Engineer",
  "userSkills": ["Python", "SQL", "Docker"],
  "requiredSkills": ["Python", "SQL", "Spark", "Kafka", "Airflow"],
  "missingSkills": ["Spark", "Kafka", "Airflow"],
  "matchPercentage": 40
}
```

### 5. Test Roadmap Generation

**Generate Roadmap:**
1. Navigate to Roadmap page
2. Click "Generate Roadmap"
3. Select target role
4. Specify timeline (e.g., 6 months)
5. Submit and wait (~5-7 seconds)
6. View generated roadmap with timeline

**Expected:**
- Timeline visualization
- Milestones organized by month
- Skills grouped by priority
- Learning resources for each skill
- Progress tracking interface

### 6. Test Chat Assistant

**Chat with AI:**
```bash
# Example questions:
- "What skills do I need for a Data Engineer role?"
- "How long will it take to learn React?"
- "What's the difference between Frontend and Backend development?"
- "Suggest a learning path for Machine Learning"
```

**Steps:**
1. Navigate to Chat page
2. Type a question
3. Press Enter or click Send
4. Wait for AI response (~2-4 seconds)
5. Continue conversation

**Expected:**
- Context-aware responses
- References to your skills (if CV uploaded)
- Actionable advice
- Conversation history maintained

### 7. Test Knowledge Graph

**View Graph:**
1. Navigate to Graph page
2. See interactive node visualization
3. Your skills highlighted in different color
4. Hover over nodes for details
5. Zoom and pan controls work

**Expected:**
- Nodes: Skills (circles), Roles (squares)
- Edges: Relationships between skills and roles
- Interactive controls
- Legend explaining node types

---

## 🔧 Configuration Options

### Option 1: Using OpenAI (Recommended for Development)

**Pros:**
- Easy setup
- High-quality AI responses
- Fast and reliable

**Cons:**
- Requires API key
- Small cost per request
- Needs internet connection

**Setup:**
```env
OPENAI_API_KEY=sk-your-key-here
```

### Option 2: Using Backend AI Module (Production)

**Pros:**
- No API costs
- Better privacy
- More control

**Cons:**
- More complex setup
- Requires backend AI module running

**Setup:**
1. Start backend AI module (see Backend/AI_SETUP_GUIDE.md)
2. Update API endpoints in `server/routes.ts` to point to backend
3. Replace `openai.ts` functions with API calls

Example:
```typescript
// Before (using OpenAI directly)
import { extractSkillsFromCV } from './openai';
const skills = await extractSkillsFromCV(cvText);

// After (using backend API)
const response = await fetch('http://localhost:8000/ai/extract-skills-text', {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ cv_text: cvText })
});
const skills = await response.json();
```

### Option 3: Mock Mode (Testing Without AI)

For testing UI without AI costs:

```typescript
// In server/openai.ts, add mock responses:
export async function extractSkillsFromCV(cvText: string) {
  // Return mock data instead of calling OpenAI
  return {
    skills: ["Python", "JavaScript", "SQL"],
    technicalSkills: ["Python", "JavaScript", "SQL"],
    softSkills: ["Communication", "Teamwork"]
  };
}
```

---

## 📊 Performance Benchmarks

### Development Mode
- Server start time: 1-2 seconds
- Hot reload: <100ms
- Page navigation: Instant
- API response time: 100ms - 2s

### Production Build
- Build time: 10-15 seconds
- Bundle size: ~500KB (gzipped)
- Initial page load: 500ms - 1s
- Time to interactive: 1-2s

### AI Operations
- CV skill extraction: 3-5 seconds
- Roadmap generation: 5-7 seconds
- Chat response: 2-4 seconds
- Graph data load: 500ms - 1s

---

## 🐛 Common Issues & Solutions

### Issue 1: "Cannot find module" errors

**Solution:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue 2: Database connection fails

**Solution:**
1. Check if PostgreSQL is running:
   ```bash
   # Linux/Mac
   sudo systemctl status postgresql
   
   # Windows
   sc query postgresql
   ```

2. Verify DATABASE_URL in `.env`
3. Test connection:
   ```bash
   psql -U your_username -d skillatlas
   ```

### Issue 3: OpenAI API errors

**Solution:**
1. Verify API key is correct
2. Check API key has credits: https://platform.openai.com/usage
3. Check rate limits
4. Try a different model in `server/openai.ts`:
   ```typescript
   model: "gpt-3.5-turbo" // instead of gpt-4
   ```

### Issue 4: Port already in use

**Solution:**
```bash
# Find process using port 5173 or 5000
# Linux/Mac
lsof -ti:5173 | xargs kill -9
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Issue 5: Vite build fails

**Solution:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

### Issue 6: Session authentication not working

**Solution:**
1. Generate new SESSION_SECRET
2. Clear browser cookies
3. Restart server
4. Try incognito mode

---

## 📝 Development Tips

### 1. Hot Reload

Vite provides instant hot reload:
- Edit React components → instant update
- Edit server files → auto restart (with nodemon)
- Edit CSS → instant update

### 2. Debug Mode

Enable verbose logging:
```typescript
// In server/app.ts
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});
```

### 3. React DevTools

Install React DevTools browser extension:
- Chrome: https://chrome.google.com/webstore
- Firefox: https://addons.mozilla.org/en-US/firefox/
- View component tree, props, and state

### 4. Database Inspection

Use Drizzle Studio:
```bash
npx drizzle-kit studio
```

Opens web interface to browse database tables.

### 5. API Testing

Use Thunder Client or Postman:
```bash
# Example: Test CV upload
POST http://localhost:5000/api/cv/upload
Headers:
  Content-Type: multipart/form-data
  Cookie: <session-cookie>
Body:
  cv: <file>
```

---

## 🎓 Next Steps

1. ✅ Verify all features work locally
2. ✅ Test with real CV files
3. ⬜ Integrate with backend AI module (Track 2)
4. ⬜ Connect to Neo4j knowledge graph (Track 1)
5. ⬜ Add more seed data (roles, skills)
6. ⬜ Customize UI/UX based on feedback
7. ⬜ Deploy to production
8. ⬜ Set up monitoring and analytics

---

## 📚 Additional Resources

- **React Documentation**: https://react.dev/
- **TypeScript**: https://www.typescriptlang.org/docs/
- **Vite**: https://vitejs.dev/guide/
- **shadcn/ui**: https://ui.shadcn.com/
- **TanStack Query**: https://tanstack.com/query/latest
- **Drizzle ORM**: https://orm.drizzle.team/
- **OpenAI API**: https://platform.openai.com/docs

---

## 🆘 Getting Help

1. Check error messages in browser console (F12)
2. Check server logs in terminal
3. Review documentation files:
   - [AI_IMPLEMENTATION_SUMMARY.md](./AI_IMPLEMENTATION_SUMMARY.md)
   - [AI_MODULE_OVERVIEW.md](./AI_MODULE_OVERVIEW.md)
   - [design_guidelines.md](./design_guidelines.md)
4. Check database with Drizzle Studio
5. Test API endpoints with curl or Postman

---

## ✅ Verification Checklist

- [ ] Node.js 18+ installed
- [ ] npm dependencies installed
- [ ] PostgreSQL running
- [ ] Database created and schema pushed
- [ ] .env file configured with all variables
- [ ] OpenAI API key valid
- [ ] Dev server starts without errors
- [ ] Can access http://localhost:5173
- [ ] Landing page loads correctly
- [ ] Can sign in (authentication works)
- [ ] Can navigate between pages
- [ ] Can upload CV
- [ ] Skills extracted from CV
- [ ] Careers page shows roles
- [ ] Roadmap can be generated
- [ ] Chat responds to messages
- [ ] Graph visualization displays

If all checked, you're ready to develop! 🚀

---

## 🚀 Production Deployment

### Build for Production

```bash
npm run build
```

This creates:
- `dist/` folder with optimized client bundle
- `dist/index.js` server file

### Environment Variables for Production

```env
NODE_ENV=production
DATABASE_URL=<production-postgresql-url>
OPENAI_API_KEY=<your-api-key>
SESSION_SECRET=<strong-secret-key>
ALLOWED_ORIGINS=https://yourdomain.com
```

### Start Production Server

```bash
npm start
```

### Deploy Options

1. **Replit**: Push to Replit and run
2. **Vercel**: Deploy with `vercel deploy`
3. **Heroku**: Use Heroku buildpack
4. **Docker**: Create Dockerfile and deploy
5. **VPS**: Run with PM2 or systemd

---

**Ready to build amazing career guidance experiences!** 🎉
