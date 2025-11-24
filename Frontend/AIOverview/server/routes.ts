import type { Express } from "express";
import { createServer, type Server } from "http";
import multer from "multer";
import * as pdfParse from "pdf-parse";
import bcrypt from "bcryptjs";
import { storage } from "./storage";
import { setupAuth, isAuthenticated } from "./auth";
import { extractSkillsFromCV, generateRoadmap, chatWithAssistant } from "./huggingface";
import { MongoClient } from 'mongodb';
import neo4j from 'neo4j-driver';

let mongoDb: any = null;
let neo4jDriver: any = null;

// Initialize external database connections
async function initExternalDbs() {
  try {
    if (process.env.MONGO_URL) {
      const mongoClient = new MongoClient(process.env.MONGO_URL);
      await mongoClient.connect();
      mongoDb = mongoClient.db(process.env.MONGO_DB_NAME || 'skillatlas');
      console.log('✅ MongoDB connected');
    }
    
    if (process.env.NEO4J_URL && process.env.NEO4J_USER && process.env.NEO4J_PASSWORD) {
      neo4jDriver = neo4j.driver(
        process.env.NEO4J_URL,
        neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASSWORD)
      );
      await neo4jDriver.verifyConnectivity();
      console.log('✅ Neo4j connected');
    }
  } catch (error) {
    console.warn('⚠️  External databases not connected:', error instanceof Error ? error.message : 'Unknown error');
  }
}

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    if (file.mimetype === "application/pdf") {
      cb(null, true);
    } else {
      cb(new Error("Only PDF files are allowed"));
    }
  },
});

// Helper: Get roles from MongoDB or PostgreSQL
async function getAllRolesWithData(): Promise<any[]> {
  try {
    if (mongoDb) {
      const roles = await mongoDb.collection('roles').find({}).toArray();
      if (roles && roles.length > 0) {
        return roles.map((r: any) => ({
          id: r.role_id || r.id || r._id.toString(),
          name: r.title || r.name,
          category: r.category,
          description: r.description,
          responsibilities: [],
          averageSalary: r.avg_salary ? `$${r.avg_salary.toLocaleString()}` : null,
          demandLevel: r.growth_rate > 20 ? 'High' : 'Medium',
        }));
      }
    }
    return await storage.getAllRoles();
  } catch (error) {
    console.error('Error fetching roles:', error);
    return await storage.getAllRoles();
  }
}

export async function registerRoutes(app: Express): Promise<Server> {
  await initExternalDbs();
  await setupAuth(app);

  // ============== AUTHENTICATION ENDPOINTS ==============
  
  app.post("/api/register", async (req: any, res) => {
    try {
      const { email, password, firstName, lastName } = req.body;

      if (!email || !password) {
        return res.status(400).json({ message: "Email and password are required" });
      }

      const existingUser = await storage.getUserByEmail(email);
      if (existingUser) {
        return res.status(400).json({ message: "User already exists" });
      }

      const hashedPassword = await bcrypt.hash(password, 10);
      const user = await storage.upsertUser({
        email,
        password: hashedPassword,
        firstName: firstName || null,
        lastName: lastName || null,
      });

      req.session.userId = user.id;
      req.session.email = user.email;
      req.session.firstName = user.firstName;
      req.session.lastName = user.lastName;

      await new Promise((resolve, reject) => {
        req.session.save((err: any) => {
          if (err) reject(err);
          else resolve(true);
        });
      });

      res.json({ 
        id: user.id, 
        email: user.email, 
        firstName: user.firstName, 
        lastName: user.lastName 
      });
    } catch (error) {
      console.error("Registration error:", error);
      res.status(500).json({ message: "Registration failed" });
    }
  });

  app.post("/api/login", async (req: any, res) => {
    try {
      const { email, password } = req.body;

      if (!email || !password) {
        return res.status(400).json({ message: "Email and password are required" });
      }

      const user = await storage.getUserByEmail(email);
      
      if (!user || !user.password) {
        return res.status(401).json({ message: "Invalid credentials" });
      }

      const isValid = await bcrypt.compare(password, user.password);
      
      if (!isValid) {
        return res.status(401).json({ message: "Invalid credentials" });
      }

      req.session.userId = user.id;
      req.session.email = user.email;
      req.session.firstName = user.firstName;
      req.session.lastName = user.lastName;

      await new Promise((resolve, reject) => {
        req.session.save((err: any) => {
          if (err) reject(err);
          else resolve(true);
        });
      });

      res.json({ 
        id: user.id, 
        email: user.email, 
        firstName: user.firstName, 
        lastName: user.lastName 
      });
    } catch (error) {
      console.error("Login error:", error);
      res.status(500).json({ message: "Login failed" });
    }
  });

  app.post("/api/logout", (req: any, res) => {
    req.session.destroy((err: any) => {
      if (err) {
        console.error("Logout error:", err);
        return res.status(500).json({ message: "Logout failed" });
      }
      res.json({ message: "Logged out successfully" });
    });
  });

  app.get("/api/auth/user", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const user = await storage.getUser(userId);
      res.json(user);
    } catch (error) {
      console.error("Error fetching user:", error);
      res.status(500).json({ message: "Failed to fetch user" });
    }
  });

  // ============== USER DATA ENDPOINTS ==============

  app.get("/api/user/stats", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const stats = await storage.getUserStats(userId);
      res.json(stats);
    } catch (error) {
      console.error("Error fetching user stats:", error);
      res.status(500).json({ message: "Failed to fetch stats" });
    }
  });

  app.get("/api/user/activity", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const activity = await storage.getUserActivity(userId);
      res.json(activity);
    } catch (error) {
      console.error("Error fetching user activity:", error);
      res.status(500).json({ message: "Failed to fetch activity" });
    }
  });

  // ============== CV/ANALYSIS ENDPOINTS ==============

  app.post("/api/cv/upload", isAuthenticated, upload.single("cv"), async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const file = req.file;

      if (!file) {
        return res.status(400).json({ message: "No file uploaded" });
      }

      const pdfData = await (pdfParse as any)(file.buffer);
      const cvText = pdfData.text;

      const extractedSkills = await extractSkillsFromCV(cvText);

      const cv = await storage.createUserCv({
        userId,
        fileName: file.originalname,
        fileContent: cvText,
        extractedSkills,
      });

      const existingSkills = await storage.getSkillsByNames(extractedSkills.skills);
      const skillMap = new Map(existingSkills.map(s => [s.name, s.id]));

      for (const skillName of extractedSkills.technicalSkills) {
        if (!skillMap.has(skillName)) {
          const newSkill = await storage.createSkill({
            name: skillName,
            category: "Technical",
            difficultyLevel: "Intermediate",
            estimatedLearningTime: 40,
            description: `Technical skill: ${skillName}`,
          });
          skillMap.set(skillName, newSkill.id);
        }
      }

      for (const skillName of extractedSkills.skills) {
        const skillId = skillMap.get(skillName);
        if (skillId) {
          try {
            await storage.createUserSkill({
              userId,
              skillId,
              proficiencyLevel: "Intermediate",
              source: "cv_extraction",
            });
          } catch (err) {
            // Ignore duplicate key errors
          }
        }
      }

      res.json(cv);
    } catch (error) {
      console.error("Error uploading CV:", error);
      res.status(500).json({ message: "Failed to upload CV" });
    }
  });

  app.get("/api/cv/latest", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const cv = await storage.getUserLatestCv(userId);
      res.json(cv || null);
    } catch (error) {
      console.error("Error fetching CV:", error);
      res.status(500).json({ message: "Failed to fetch CV" });
    }
  });

  app.get("/api/cv/analysis", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const roleId = req.query.role as string;

      if (!roleId) {
        return res.status(400).json({ message: "Role ID is required" });
      }

      const role = await storage.getRoleById(roleId);
      if (!role) {
        return res.status(404).json({ message: "Role not found" });
      }

      const userSkillsList = await storage.getUserSkills(userId);
      const roleSkillsList = await storage.getRoleSkills(roleId);

      const userSkillNames = new Set(userSkillsList.map(s => s.skillName));
      const requiredSkillNames = roleSkillsList.map(s => s.skillName);
      const missingSkills = requiredSkillNames.filter(s => !userSkillNames.has(s));

      res.json({
        roleName: role.name,
        userSkills: Array.from(userSkillNames),
        requiredSkills: requiredSkillNames,
        missingSkills,
        matchPercentage: Math.round(((requiredSkillNames.length - missingSkills.length) / requiredSkillNames.length) * 100),
      });
    } catch (error) {
      console.error("Error analyzing CV:", error);
      res.status(500).json({ message: "Failed to analyze CV" });
    }
  });

  // ============== ROLE ENDPOINTS ==============

  app.get("/api/roles", isAuthenticated, async (req: any, res) => {
    try {
      const roles = await getAllRolesWithData();
      res.json(roles);
    } catch (error) {
      console.error("Error fetching roles:", error);
      res.status(500).json({ message: "Failed to fetch roles" });
    }
  });

  app.get("/api/roles/:id", isAuthenticated, async (req: any, res) => {
    try {
      const roleId = req.params.id;
      
      if (mongoDb) {
        const role = await mongoDb.collection('roles').findOne({ role_id: roleId });
        if (role) {
          const skillIds = role.required_skills?.map((s: any) => s.skill_id) || [];
          const skills = await mongoDb.collection('skills').find({ skill_id: { $in: skillIds } }).toArray();
          
          return res.json({
            id: role.role_id,
            name: role.title,
            category: role.category,
            description: role.description,
            responsibilities: skills.map((s: any) => s.name),
            averageSalary: role.avg_salary ? `$${role.avg_salary.toLocaleString()}` : null,
            demandLevel: role.growth_rate > 20 ? 'High' : 'Medium',
          });
        }
      }
      
      const role = await storage.getRoleById(roleId);
      if (!role) {
        return res.status(404).json({ message: "Role not found" });
      }
      res.json(role);
    } catch (error) {
      console.error("Error fetching role:", error);
      res.status(500).json({ message: "Failed to fetch role" });
    }
  });

  app.get("/api/roles/categories", isAuthenticated, async (req: any, res) => {
    try {
      if (mongoDb) {
        const categories = await mongoDb.collection('roles').distinct('category');
        return res.json(categories);
      }
      const categories = await storage.getRoleCategories();
      res.json(categories);
    } catch (error) {
      console.error("Error fetching categories:", error);
      res.status(500).json({ message: "Failed to fetch categories" });
    }
  });

  // ============== ROADMAP ENDPOINTS ==============

  app.get("/api/roadmap", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const roadmap = await storage.getUserRoadmap(userId);
      res.json(roadmap || null);
    } catch (error) {
      console.error("Error fetching roadmap:", error);
      res.status(500).json({ message: "Failed to fetch roadmap" });
    }
  });

  app.post("/api/roadmap/generate", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const { roleId, estimatedMonths } = req.body;

      if (!roleId) {
        return res.status(400).json({ message: "Role ID is required" });
      }

      const role = await storage.getRoleById(roleId);
      if (!role) {
        return res.status(404).json({ message: "Role not found" });
      }

      const userSkillsList = await storage.getUserSkills(userId);
      const roleSkillsList = await storage.getRoleSkills(roleId);

      const userSkillNames = userSkillsList.map(s => s.skillName);
      const requiredSkillNames = roleSkillsList.map(s => s.skillName);
      const missingSkills = requiredSkillNames.filter(s => !userSkillNames.includes(s));

      const roadmapData = await generateRoadmap({
        userSkills: userSkillNames,
        targetRole: role.name,
        missingSkills,
        estimatedMonths: estimatedMonths || 12,
      });

      const roadmap = await storage.createRoadmap({
        userId,
        roleId,
        name: roadmapData.name || `${role.name} Learning Path`,
        estimatedDuration: roadmapData.estimatedDuration || estimatedMonths || 12,
        milestones: roadmapData.milestones || [],
      });

      res.json(roadmap);
    } catch (error) {
      console.error("Error generating roadmap:", error);
      res.status(500).json({ message: "Failed to generate roadmap" });
    }
  });

  // ============== PROGRESS TRACKING ENDPOINTS ==============

  app.post("/api/skills/progress", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const { skillId, status, notes } = req.body;

      if (!skillId || !status) {
        return res.status(400).json({ message: "Skill ID and status are required" });
      }

      const progress = await storage.createOrUpdateProgress({
        userId,
        skillId,
        status,
        notes: notes || null,
        completedAt: status === 'completed' ? new Date() : null,
      });

      res.json(progress);
    } catch (error) {
      console.error("Error updating progress:", error);
      res.status(500).json({ message: "Failed to update progress" });
    }
  });

  // ============== CHAT ENDPOINTS ==============

  app.get("/api/chat/messages", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const messages = await storage.getUserChatMessages(userId);
      res.json(messages);
    } catch (error) {
      console.error("Error fetching messages:", error);
      res.status(500).json({ message: "Failed to fetch messages" });
    }
  });

  app.post("/api/chat/send", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const { content } = req.body;

      if (!content) {
        return res.status(400).json({ message: "Message content is required" });
      }

      await storage.createChatMessage({
        userId,
        role: "user",
        content,
      });

      const history = await storage.getUserChatMessages(userId, 20);
      const conversationHistory = history.map(m => ({
        role: m.role,
        content: m.content,
      }));

      const userSkillsList = await storage.getUserSkills(userId);
      const roadmap = await storage.getUserRoadmap(userId);

      const aiResponse = await chatWithAssistant({
        userMessage: content,
        conversationHistory,
        userContext: {
          skills: userSkillsList.map(s => s.skillName),
          targetRole: roadmap ? (await storage.getRoleById(roadmap.roleId))?.name : undefined,
        },
      });

      const assistantMessage = await storage.createChatMessage({
        userId,
        role: "assistant",
        content: aiResponse,
      });

      res.json(assistantMessage);
    } catch (error) {
      console.error("Error sending message:", error);
      res.status(500).json({ message: "Failed to send message" });
    }
  });

  // ============== KNOWLEDGE GRAPH ENDPOINTS ==============

  app.get("/api/graph", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      
      if (neo4jDriver) {
        const session = neo4jDriver.session();
        try {
          const result = await session.run(`
            MATCH (r:Role)-[req:REQUIRES]->(s:Skill)
            RETURN r.title as role, s.name as skill, req.priority as priority
            LIMIT 50
          `);
          
          const nodes: any[] = [];
          const edges: any[] = [];
          const nodeIds = new Set();
          
          result.records.forEach((record: any) => {
            const role = record.get('role');
            const skill = record.get('skill');
            const priority = record.get('priority');
            
            if (!nodeIds.has(role)) {
              nodes.push({ id: role, name: role, type: 'role' });
              nodeIds.add(role);
            }
            if (!nodeIds.has(skill)) {
              nodes.push({ id: skill, name: skill, type: 'skill' });
              nodeIds.add(skill);
            }
            edges.push({ from: role, to: skill, label: priority });
          });
          
          await session.close();
          return res.json({ nodes, edges });
        } catch (error) {
          await session.close();
          throw error;
        }
      }
      
      // Fallback to PostgreSQL
      const userSkillsList = await storage.getUserSkills(userId);
      const allRoles = await storage.getAllRoles();

      const graphData = {
        nodes: [
          ...userSkillsList.map(s => ({
            id: s.skillId,
            name: s.skillName,
            type: "skill",
            userHas: true,
          })),
          ...allRoles.slice(0, 5).map(r => ({
            id: r.id,
            name: r.name,
            type: "role",
          })),
        ],
        edges: [],
      };

      res.json(graphData);
    } catch (error) {
      console.error("Error fetching graph:", error);
      res.status(500).json({ message: "Failed to fetch graph" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}

