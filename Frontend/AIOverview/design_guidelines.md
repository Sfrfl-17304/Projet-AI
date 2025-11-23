# SkillAtlas Design Guidelines

## Design Approach

**Selected Approach:** Design System + Professional Dashboard Hybrid

Drawing from Linear's clean typography, Notion's information architecture, and modern SaaS dashboards (Stripe, Vercel). This platform prioritizes clarity, data visualization, and professional credibility over visual flair.

**Core Principles:**
- Information hierarchy over decoration
- Data-driven insights presented clearly
- Professional credibility through polish
- Efficient navigation for power users

---

## Typography System

**Font Stack:** 
- Primary: Inter (Google Fonts) - headers, body, UI
- Monospace: JetBrains Mono - code snippets, technical details

**Hierarchy:**
- Hero Headlines: text-5xl to text-6xl, font-bold, tracking-tight
- Section Titles: text-3xl, font-semibold
- Card Headers: text-xl, font-semibold
- Body Text: text-base, font-normal, leading-relaxed
- Secondary/Meta: text-sm, font-medium
- Captions: text-xs, font-normal

---

## Layout System

**Spacing Primitives:** Tailwind units of 2, 4, 6, 8, 12, 16
- Component padding: p-4 to p-6
- Section spacing: py-12 to py-16
- Card gaps: gap-4 to gap-6
- Container margins: mx-auto with max-w-7xl

**Grid System:**
- Dashboard: Sidebar (w-64) + Main Content (flex-1)
- Card Grids: grid-cols-1 md:grid-cols-2 lg:grid-cols-3
- Two-column splits: grid-cols-1 lg:grid-cols-2 with gap-8

---

## Component Library

### Navigation
**Sidebar (Dashboard Pages):**
- Fixed left sidebar, full height
- Logo at top with h-16
- Navigation groups with section headers
- Icon + text menu items (Heroicons)
- Active state: slightly offset background
- Bottom section for user profile

**Top Navigation (Marketing Pages):**
- Horizontal nav with max-w-7xl container
- Logo left, links center, CTA buttons right
- Sticky positioning on scroll

### Hero Section
**Landing Page Hero:**
- Full-width section with pt-20 pb-16
- Two-column layout: Left (content) + Right (visual)
- Left: Headline (text-5xl), subheadline (text-xl), CTA buttons (primary + secondary)
- Right: Hero illustration/screenshot showing platform interface
- Include trust indicators below CTAs: "Used by X students" with small logos

**Image Specification:** Professional dashboard screenshot or abstract illustration showing knowledge graph connections. Should communicate "intelligent, data-driven platform."

### Dashboard Cards
**Standard Card Pattern:**
- Rounded corners (rounded-lg)
- Border with subtle shadow
- Padding p-6
- Header with icon + title + action button
- Content area with appropriate spacing
- Footer with metadata or actions when needed

**Skill Gap Card:**
- Table format with columns: Skill Name, Your Level, Required Level, Status
- Progress indicators using width-based bars
- Color-coded status badges
- Compact row spacing (py-2)

### Data Visualization
**Knowledge Graph:**
- Full-width container with min-h-96
- Interactive canvas area
- Legend in top-right corner
- Zoom controls bottom-right
- Node types: Roles (larger), Skills (medium), Tools (smaller)
- Connection lines showing relationships

**Roadmap Timeline:**
- Vertical timeline on left (4-6 month markers)
- Skill cards positioned along timeline
- Connecting lines between prerequisites
- Each card: skill name, estimated hours, resources link

### Forms & Inputs
**CV Upload Area:**
- Dashed border drag-drop zone
- Center-aligned icon, text, and browse button
- File type and size restrictions below
- Preview area showing uploaded file name

**Interest Questionnaire:**
- Card-based multi-step form
- Progress indicator at top
- Radio/checkbox groups with generous spacing
- Navigation: Back + Continue buttons bottom-right

### Chat Assistant
**Fixed Bottom-Right Widget:**
- Circular launcher button (w-14 h-14) with chat icon
- Expands to w-96 h-[600px] chat panel
- Header with close button
- Message list with alternating user/AI messages
- Input field with send button at bottom
- Suggested questions as clickable chips

### Tables
**Skills & Requirements Tables:**
- Compact header with borders
- Alternating row backgrounds for scannability
- Icon columns for status indicators
- Action column on right for buttons/links
- Responsive: stack on mobile with card layout

### Buttons & CTAs
**Button Hierarchy:**
- Primary CTA: Larger size (px-6 py-3), bold text, prominent
- Secondary: Ghost style with border
- Tertiary: Text-only with icon
- Icon buttons: Square aspect ratio, p-2
- Rounded corners: rounded-md for buttons

**Blurred Backgrounds (Hero CTAs):**
- backdrop-blur-md with semi-transparent background
- Ensures readability over images
- Subtle shadow for depth

---

## Marketing Landing Page Structure

**Complete Section Breakdown (7 sections):**

1. **Hero** - Two-column with headline, subheadline, dual CTAs, trust indicators, dashboard screenshot
2. **How It Works** - Three-column grid showing: CV Upload → Analysis → Roadmap with icons and brief descriptions
3. **Features** - Two-column alternating layout: Skill Extraction, Knowledge Graph, AI Assistant, Learning Roadmaps (4 features total, each with description + illustration)
4. **Use Cases** - Two-column grid cards for "With CV" and "Beginners" paths
5. **Platform Preview** - Full-width screenshot gallery showing dashboard, graphs, and chat
6. **Testimonials** - Three-column grid with student quotes, photos, and role goals
7. **Final CTA** - Centered section with headline, supporting text, email signup or "Get Started" button

---

## Dashboard Application Structure

**Main Dashboard Views:**

1. **Home/Overview** - Welcome card, recent activity, quick stats (skills learned, time invested), next steps
2. **Skill Analysis** - Uploaded CV summary, extracted skills list, skill gap table, recommended actions
3. **Career Explorer** - Role catalog cards, filter sidebar, detailed role view with requirements
4. **Learning Roadmap** - Timeline visualization, milestone cards, progress tracking, resource links
5. **Knowledge Graph** - Interactive visualization, search/filter, node details panel
6. **Chat Assistant** - Conversation history, saved responses, suggested questions
7. **Profile Settings** - User info, preferences, progress export

---

## Icons & Assets

**Icon Library:** Heroicons (via CDN)
- Use outline style for navigation and general UI
- Use solid style for active states and primary actions
- Consistent sizing: w-5 h-5 for inline, w-6 h-6 for buttons

**Illustrations:** Use placeholders for:
- Knowledge graph connections (abstract node network)
- Learning roadmap journey (path/steps illustration)
- AI assistant (robot/chat icon)
- Career paths (branching tree structure)

---

## Images Section

**Hero Image:** Professional dashboard screenshot showing the SkillAtlas interface with visible skill gap analysis table and knowledge graph preview. Should communicate sophistication and data-driven insights. Dimensions: 1200x800px minimum.

**Feature Section Images:** 
- Screenshot of CV upload interface
- Knowledge graph visualization in action
- Roadmap timeline with multiple skills
- Chat assistant conversation example

**Testimonial Section:** Student headshots (3 diverse individuals), professional but approachable style, circular crop (w-16 h-16).

---

## Responsive Behavior

**Breakpoints:**
- Mobile (base): Single column, stacked layout, collapsible sidebar
- Tablet (md: 768px): Two columns where appropriate, visible sidebar on toggle
- Desktop (lg: 1024px): Full multi-column layouts, persistent sidebar
- Wide (xl: 1280px): Max container width, optimal reading lengths

**Mobile Adaptations:**
- Sidebar converts to slide-out drawer
- Tables convert to card-based stacks
- Graph visualizations adapt to portrait orientation
- Chat widget becomes full-screen overlay

---

This design creates a professional, trustworthy platform that balances data density with usability, ensuring students receive clear guidance through visual hierarchy and intuitive navigation.