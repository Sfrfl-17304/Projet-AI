# SkillAtlas Frontend

AI-Driven Career Guidance and Learning Roadmap Platform - Frontend Application

## Features

- ✅ **React 18 + TypeScript** - Modern, type-safe frontend development
- ✅ **Vite Build System** - Lightning-fast HMR and optimized production builds
- ✅ **shadcn/ui Components** - Beautiful, accessible UI component library
- ✅ **TanStack Query** - Powerful server state management
- ✅ **Express Backend** - RESTful API with PostgreSQL integration
- ✅ **AI Integration** - OpenAI-powered skill extraction and chat assistant
- ✅ **Authentication** - Secure Replit Auth integration
- ✅ **Responsive Design** - Mobile-first, works on all devices
- ✅ **8 Complete Pages** - Dashboard, Analysis, Careers, Roadmap, Graph, Chat, Settings, Landing
- ✅ **14 API Endpoints** - Full-featured backend with database operations

## Project Structure

```
Frontend/AIOverview/
├── client/                    # React Application
│   ├── public/               # Static assets
│   └── src/
│       ├── pages/            # Application pages (8 pages)
│       │   ├── landing.tsx   # Marketing landing page
│       │   ├── dashboard.tsx # User dashboard with stats
│       │   ├── analysis.tsx  # CV analysis and skill gaps
│       │   ├── careers.tsx   # Career exploration
│       │   ├── roadmap.tsx   # Learning roadmap timeline
│       │   ├── graph.tsx     # Knowledge graph visualization
│       │   ├── chat.tsx      # AI chat assistant
│       │   └── settings.tsx  # User settings
│       ├── components/       # React components
│       │   ├── ui/          # shadcn/ui components (50+)
│       │   └── app-sidebar.tsx
│       ├── hooks/           # Custom React hooks
│       │   ├── useAuth.ts
│       │   ├── useToast.ts
│       │   └── use-mobile.tsx
│       ├── lib/             # Utilities
│       │   ├── queryClient.ts
│       │   ├── authUtils.ts
│       │   └── utils.ts
│       ├── App.tsx          # Main app component
│       ├── main.tsx         # Entry point
│       └── index.css        # Global styles
├── server/                  # Express Backend
│   ├── routes.ts           # API endpoint definitions
│   ├── storage.ts          # Database operations layer
│   ├── openai.ts           # AI service integration
│   ├── replitAuth.ts       # Authentication setup
│   ├── db.ts               # Database connection
│   ├── seed.ts             # Database seeding
│   └── app.ts              # Express app configuration
├── shared/
│   └── schema.ts           # Database schema (Drizzle ORM)
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite configuration
├── tailwind.config.ts      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
├── drizzle.config.ts       # Drizzle ORM configuration
├── .env.example            # Environment variables template
├── README.md               # This file
├── AI_SETUP_GUIDE.md       # Setup instructions
├── AI_MODULE_OVERVIEW.md   # Quick feature overview
├── AI_IMPLEMENTATION_SUMMARY.md  # Detailed implementation docs
└── design_guidelines.md    # UI/UX design system
```

## Prerequisites

- Node.js 18+ and npm
- PostgreSQL database
- OpenAI API key (for AI features)
- Modern web browser

## Setup Instructions

### 1. Install Dependencies

```bash
cd Frontend/AIOverview
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Important variables in `.env`:**
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/skillatlas

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# Session
SESSION_SECRET=generate-a-secure-random-string

# Application
NODE_ENV=development
PORT=5000
VITE_API_URL=http://localhost:5000
```

### 3. Setup Database

Create PostgreSQL database:
```bash
psql -U postgres
CREATE DATABASE skillatlas;
\q
```

Push schema:
```bash
npm run db:push
```

(Optional) Seed with initial data:
```bash
tsx server/run-seed.ts
```

### 4. Start Development Server

```bash
npm run dev
```

This starts:
- Vite dev server on `http://localhost:5173` (frontend)
- Express API server on `http://localhost:5000` (backend)

### 5. Access Application

Visit: **http://localhost:5173**

### 6. Access API Documentation

The API endpoints are documented in this README. For interactive testing, use tools like:
- Thunder Client (VS Code extension)
- Postman
- curl commands

---

## API Endpoints

### Authentication

- `GET /api/auth/user` - Get current authenticated user
  - Requires: Authentication
  - Returns: User object with profile information

### User Data

- `GET /api/user/stats` - Get user statistics
  - Requires: Authentication
  - Returns: `{ skillsLearned, timeInvested, roadmapsCompleted }`

- `GET /api/user/activity` - Get recent user activity
  - Requires: Authentication
  - Returns: Array of recent activities

### CV Management

- `POST /api/cv/upload` - Upload and analyze CV
  - Requires: Authentication
  - Content-Type: `multipart/form-data`
  - Body: `cv` (PDF file)
  - Returns: Extracted skills and CV data

- `GET /api/cv/latest` - Get user's latest CV
  - Requires: Authentication
  - Returns: CV object with extracted skills

- `GET /api/cv/analysis?role=<roleId>` - Analyze skill gap for role
  - Requires: Authentication
  - Query: `role` (role ID)
  - Returns: Gap analysis with missing skills and match percentage

### Career Roles

- `GET /api/roles` - Get all career roles
  - Requires: Authentication
  - Returns: Array of role objects

- `GET /api/roles/categories` - Get role categories
  - Requires: Authentication
  - Returns: Array of unique categories

### Learning Roadmap

- `GET /api/roadmap` - Get user's current roadmap
  - Requires: Authentication
  - Returns: Roadmap object with milestones

- `POST /api/roadmap/generate` - Generate new learning roadmap
  - Requires: Authentication
  - Body: `{ roleId, estimatedMonths }`
  - Returns: Generated roadmap with milestones

### Progress Tracking

- `POST /api/skills/progress` - Update skill learning progress
  - Requires: Authentication
  - Body: `{ skillId, status, notes }`
  - Status: `not_started`, `learning`, `completed`
  - Returns: Progress object

### Chat Assistant

- `GET /api/chat/messages` - Get conversation history
  - Requires: Authentication
  - Returns: Array of chat messages

- `POST /api/chat/send` - Send message to AI assistant
  - Requires: Authentication
  - Body: `{ content }`
  - Returns: AI assistant response message

### Knowledge Graph

- `GET /api/graph` - Get knowledge graph data
  - Requires: Authentication
  - Returns: Graph structure with nodes and edges

---

## Pages Overview

### 1. Landing Page (`/`)
- Hero section with value proposition
- Features showcase
- How it works section
- Testimonials
- Call-to-action buttons
- Sign in/up functionality

### 2. Dashboard (`/`)
- User statistics (skills learned, time invested)
- Recent activity timeline
- Quick action cards
- Skills in progress
- Roadmap overview

### 3. Analysis (`/analysis`)
- CV upload interface (drag-and-drop)
- Extracted skills display
- Skill gap visualization
- Target role selection
- Match percentage for roles

### 4. Careers (`/careers`)
- Career role catalog
- Category filtering
- Role cards with descriptions
- Skill requirements for each role
- Salary and demand information

### 5. Roadmap (`/roadmap`)
- Timeline visualization
- Milestone cards with skills
- Progress tracking
- Learning resources
- Estimated completion time

### 6. Knowledge Graph (`/graph`)
- Interactive node-based visualization
- Skills, roles, and relationships
- User skills highlighted
- Zoom and pan controls
- Node details panel

### 7. Chat Assistant (`/chat`)
- Conversational interface
- Message history
- Suggested questions
- Context-aware AI responses
- Career guidance and recommendations

### 8. Settings (`/settings`)
- User profile management
- Preferences configuration
- Account information
- Theme settings (if implemented)

---

## Usage Examples

### 1. Upload and Analyze CV

```bash
# Using curl
curl -X POST "http://localhost:5000/api/cv/upload" \
  -H "Cookie: <session-cookie>" \
  -F "cv=@path/to/resume.pdf"
```

**Response:**
```json
{
  "id": "cv-123",
  "fileName": "resume.pdf",
  "extractedSkills": {
    "skills": ["Python", "React", "SQL", "Docker"],
    "technicalSkills": ["Python", "React", "SQL", "Docker"],
    "softSkills": ["Leadership", "Communication"]
  },
  "uploadedAt": "2025-11-21T10:00:00Z"
}
```

### 2. Generate Learning Roadmap

```bash
curl -X POST "http://localhost:5000/api/roadmap/generate" \
  -H "Content-Type: application/json" \
  -H "Cookie: <session-cookie>" \
  -d '{
    "roleId": "role-data-engineer",
    "estimatedMonths": 6
  }'
```

**Response:**
```json
{
  "id": "roadmap-123",
  "name": "Data Engineer Learning Path",
  "estimatedDuration": 6,
  "milestones": [
    {
      "month": 1,
      "title": "Foundations",
      "skills": ["Python Basics", "SQL Fundamentals"]
    },
    {
      "month": 2,
      "title": "Data Processing",
      "skills": ["Pandas", "Data Cleaning"]
    }
  ]
}
```

### 3. Chat with AI Assistant

```bash
curl -X POST "http://localhost:5000/api/chat/send" \
  -H "Content-Type: application/json" \
  -H "Cookie: <session-cookie>" \
  -d '{
    "content": "What skills do I need for a Machine Learning Engineer role?"
  }'
```

**Response:**
```json
{
  "id": "msg-123",
  "role": "assistant",
  "content": "To become a Machine Learning Engineer, you'll need: 1) Programming (Python, R), 2) Math (Linear Algebra, Statistics), 3) ML Libraries (TensorFlow, PyTorch), 4) Data Processing (Pandas, NumPy), 5) Cloud Platforms (AWS, GCP)...",
  "createdAt": "2025-11-21T10:00:00Z"
}
```

---

## Database Schema

The application uses PostgreSQL with Drizzle ORM. Key tables:

- **users** - User accounts
- **userCvs** - Uploaded CVs with extracted skills
- **roles** - Career roles with descriptions
- **skills** - Skill catalog
- **roleSkills** - Required skills for roles (many-to-many)
- **userSkills** - User's acquired skills (many-to-many)
- **skillPrerequisites** - Skill dependencies
- **learningResources** - Learning materials
- **roadmaps** - User learning roadmaps
- **userProgress** - Progress tracking
- **chatMessages** - Chat history
- **sessions** - Session management

See `shared/schema.ts` for complete schema definitions.

---

## Scripts

```bash
# Development
npm run dev              # Start dev server (frontend + backend)

# Build
npm run build            # Build for production
npm run start            # Start production server

# Type Checking
npm run check            # TypeScript type check

# Database
npm run db:push          # Push schema to database
npx drizzle-kit studio   # Open database UI
```

---

## Technology Stack

### Frontend
- **React** 18.3 - UI library
- **TypeScript** 5.6 - Type safety
- **Vite** 5.4 - Build tool
- **Wouter** 3.3 - Routing
- **TanStack Query** 5.60 - Server state
- **shadcn/ui** - Component library
- **Tailwind CSS** 3.4 - Styling
- **Framer Motion** 11.13 - Animations
- **Recharts** 2.15 - Data visualization

### Backend
- **Express** 4.21 - Web framework
- **Drizzle ORM** - Database ORM
- **PostgreSQL** - Database
- **OpenAI** 6.9 - AI integration
- **Replit Auth** - Authentication
- **Multer** - File uploads
- **pdf-parse** - PDF processing

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `SESSION_SECRET` | Session encryption secret | Yes | - |
| `NODE_ENV` | Environment mode | No | development |
| `PORT` | Server port | No | 5000 |
| `VITE_API_URL` | API base URL for frontend | No | http://localhost:5000 |
| `REPLIT_APP_NAME` | Replit app name (if using Replit) | No | - |

---

## Next Steps for Integration

### AI Module Integration (Track 2)

Replace OpenAI direct calls with backend AI module:

1. **Update CV Extraction**:
   ```typescript
   // In server/routes.ts
   // Replace: const extractedSkills = await extractSkillsFromCV(cvText);
   // With: API call to backend /ai/extract-skills-text
   ```

2. **Update Roadmap Generation**:
   ```typescript
   // Replace: const roadmapData = await generateRoadmap({...});
   // With: API call to backend /ai/generate-roadmap
   ```

3. **Update Chat Assistant**:
   ```typescript
   // Replace: const aiResponse = await chatWithAssistant({...});
   // With: API call to backend /ai/chat
   ```

### Neo4j Integration (Track 1)

1. Add Neo4j driver to `server/db.ts`
2. Replace PostgreSQL role and skill queries with graph queries
3. Enhance knowledge graph visualization with graph data
4. Use graph algorithms for optimal learning paths

---

## Security Notes

- ⚠️ Use strong SESSION_SECRET in production
- ⚠️ Enable HTTPS in production
- ⚠️ Implement rate limiting for API endpoints
- ⚠️ Validate and sanitize all user inputs
- ⚠️ Store sensitive data in environment variables
- ⚠️ Use secure session configuration
- ⚠️ Implement CORS properly for production

---

## Team Responsibilities

- **Track 1 (Data/Neo4j)**: Replace PostgreSQL with Neo4j for graph operations
- **Track 2 (AI/NLP)**: Integrate backend AI module endpoints
- **Track 3 (Backend)**: Maintain Express APIs and database operations
- **Track 4 (Frontend)**: Enhance UI/UX and user experience

---

## Troubleshooting

**Port already in use:**
```bash
# Kill process on port 5173 or 5000
lsof -ti:5173 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

**Database connection fails:**
- Check PostgreSQL is running
- Verify DATABASE_URL is correct
- Test connection with psql

**OpenAI API errors:**
- Verify API key is valid
- Check API credits and rate limits
- Try using gpt-3.5-turbo instead of gpt-4

**Module not found:**
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## License

UIR - 4th Year AI Course Project

## Contributors

- Ramou Nassim (120068) - Frontend Development & Integration
- Hanae OUAZZANI-AMRI (119276) - Data & Knowledge Graph (Track 1)
- Oubahmane Mohamed Omar (120119) - AI/NLP and RAG (Track 2)
- Akoujan Ali (118588) - Backend APIs Integration (Track 3)

---

## Additional Documentation

- [AI_SETUP_GUIDE.md](./AI_SETUP_GUIDE.md) - Detailed setup instructions
- [AI_MODULE_OVERVIEW.md](./AI_MODULE_OVERVIEW.md) - Quick feature overview
- [AI_IMPLEMENTATION_SUMMARY.md](./AI_IMPLEMENTATION_SUMMARY.md) - Complete implementation details
- [design_guidelines.md](./design_guidelines.md) - UI/UX design system

---

**Ready to build the future of career guidance!** 🚀
