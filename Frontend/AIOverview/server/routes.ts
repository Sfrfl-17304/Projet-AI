import type { Express } from "express";
import { createServer, type Server } from "http";
import multer from "multer";
import * as pdfParse from "pdf-parse";
import { storage } from "./storage";
import { setupAuth, isAuthenticated } from "./replitAuth";
import { extractSkillsFromCV, generateRoadmap, chatWithAssistant } from "./openai";

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB limit
  fileFilter: (req, file, cb) => {
    if (file.mimetype === "application/pdf") {
      cb(null, true);
    } else {
      cb(new Error("Only PDF files are allowed"));
    }
  },
});

export async function registerRoutes(app: Express): Promise<Server> {
  // Setup authentication
  await setupAuth(app);

  // Auth routes
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

  // User stats
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

  // User activity
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

  // CV upload and analysis
  app.post("/api/cv/upload", isAuthenticated, upload.single("cv"), async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const file = req.file;

      if (!file) {
        return res.status(400).json({ message: "No file uploaded" });
      }

      // Parse PDF
      const pdfData = await pdfParse(file.buffer);
      const cvText = pdfData.text;

      // Extract skills using OpenAI
      const extractedSkills = await extractSkillsFromCV(cvText);

      // Save CV to database
      const cv = await storage.createUserCv({
        userId,
        fileName: file.originalname,
        fileContent: cvText,
        extractedSkills,
      });

      // Create user skills from extracted skills
      const existingSkills = await storage.getSkillsByNames(extractedSkills.skills);
      const skillMap = new Map(existingSkills.map(s => [s.name, s.id]));

      // Create skills that don't exist
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

      // Link skills to user
      for (const skillName of extractedSkills.skills) {
        const skillId = skillMap.get(skillName);
        if (skillId) {
          await storage.createUserSkill({
            userId,
            skillId,
            proficiencyLevel: "Intermediate",
            source: "cv_extraction",
          });
        }
      }

      res.json(cv);
    } catch (error) {
      console.error("Error uploading CV:", error);
      res.status(500).json({ message: "Failed to upload CV" });
    }
  });

  // Get latest CV
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

  // Get CV analysis for a role
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

  // Roles endpoints
  app.get("/api/roles", isAuthenticated, async (req: any, res) => {
    try {
      const roles = await storage.getAllRoles();
      res.json(roles);
    } catch (error) {
      console.error("Error fetching roles:", error);
      res.status(500).json({ message: "Failed to fetch roles" });
    }
  });

  app.get("/api/roles/categories", isAuthenticated, async (req: any, res) => {
    try {
      const categories = await storage.getRoleCategories();
      res.json(categories);
    } catch (error) {
      console.error("Error fetching categories:", error);
      res.status(500).json({ message: "Failed to fetch categories" });
    }
  });

  // Roadmap endpoints
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

      // Generate roadmap using OpenAI
      const roadmapData = await generateRoadmap({
        userSkills: userSkillNames,
        targetRole: role.name,
        missingSkills,
        estimatedMonths: estimatedMonths || 12,
      });

      // Save roadmap to database
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

  // Progress tracking
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

  // Chat endpoints
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

      // Save user message
      await storage.createChatMessage({
        userId,
        role: "user",
        content,
      });

      // Get conversation history
      const history = await storage.getUserChatMessages(userId, 20);
      const conversationHistory = history.map(m => ({
        role: m.role,
        content: m.content,
      }));

      // Get user context
      const userSkillsList = await storage.getUserSkills(userId);
      const roadmap = await storage.getUserRoadmap(userId);

      // Get AI response
      const aiResponse = await chatWithAssistant({
        userMessage: content,
        conversationHistory,
        userContext: {
          skills: userSkillsList.map(s => s.skillName),
          targetRole: roadmap ? (await storage.getRoleById(roadmap.roleId))?.name : undefined,
        },
      });

      // Save AI response
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

  // Knowledge graph endpoint
  app.get("/api/graph", isAuthenticated, async (req: any, res) => {
    try {
      const userId = req.user.claims.sub;
      const userSkillsList = await storage.getUserSkills(userId);
      const allRoles = await storage.getAllRoles();

      // Build graph data structure
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
