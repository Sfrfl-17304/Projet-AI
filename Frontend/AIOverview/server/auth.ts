// Custom authentication with PostgreSQL sessions
import session from "express-session";
import type { Express, RequestHandler } from "express";
import connectPg from "connect-pg-simple";

export function getSession() {
  const sessionTtl = 7 * 24 * 60 * 60 * 1000; // 1 week
  
  console.log("🗄️  Configuring PostgreSQL session store");
  
  const pgStore = connectPg(session);
  const sessionStore = new pgStore({
    conString: process.env.DATABASE_URL,
    createTableIfMissing: true,
    ttl: sessionTtl / 1000, // ttl is in seconds, not milliseconds
    tableName: "sessions",
  });
  
  return session({
    name: 'skillatlas.sid',
    secret: process.env.SESSION_SECRET!,
    store: sessionStore,
    resave: false,
    saveUninitialized: false,
    rolling: true, // Refresh session on each request
    cookie: {
      httpOnly: true,
      secure: false, // Set to false for development (http)
      sameSite: 'lax',
      maxAge: sessionTtl,
      path: '/',
      domain: undefined, // Let browser determine domain
    },
  });
}

export async function setupAuth(app: Express) {
  console.log("🔐 Setting up custom authentication");
  
  // Trust first proxy (for session cookies)
  app.set("trust proxy", 1);
  
  // Apply session middleware
  app.use(getSession());
  
  console.log("✅ Session middleware configured");
}

export const isAuthenticated: RequestHandler = async (req, res, next) => {
  const sessionData = (req as any).session;
  const sessionID = (req as any).sessionID;
  
  console.log("🔍 Auth check - SessionID:", sessionID, "| UserId:", sessionData?.userId);
  
  if (sessionData?.userId) {
    // Reconstruct user object for compatibility with existing routes
    (req as any).user = {
      claims: {
        sub: sessionData.userId,
        email: sessionData.email,
        first_name: sessionData.firstName,
        last_name: sessionData.lastName,
      }
    };
    console.log("✅ User authenticated:", sessionData.userId);
    return next();
  }
  
  console.log("❌ Not authenticated");
  return res.status(401).json({ message: "Unauthorized" });
};
