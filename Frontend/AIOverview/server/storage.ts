// Database storage implementation
import { config } from "dotenv";

// Load environment variables FIRST
config();

import {
  users,
  userCvs,
  roles,
  skills,
  roleSkills,
  userSkills,
  learningResources,
  roadmaps,
  userProgress,
  chatMessages,
  skillPrerequisites,
  type User,
  type UpsertUser,
  type UserCv,
  type InsertUserCv,
  type Role,
  type InsertRole,
  type Skill,
  type InsertSkill,
  type RoleSkill,
  type InsertRoleSkill,
  type UserSkill,
  type InsertUserSkill,
  type LearningResource,
  type InsertLearningResource,
  type Roadmap,
  type InsertRoadmap,
  type UserProgress,
  type InsertUserProgress,
  type ChatMessage,
  type InsertChatMessage,
} from "@shared/schema";
import { db } from "./db";
import { eq, and, desc, inArray } from "drizzle-orm";

export interface IStorage {
  // User operations
  getUser(id: string): Promise<User | undefined>;
  getUserByEmail(email: string): Promise<User | undefined>;
  upsertUser(user: UpsertUser): Promise<User>;

  // CV operations
  getUserLatestCv(userId: string): Promise<UserCv | undefined>;
  createUserCv(cv: InsertUserCv): Promise<UserCv>;

  // Role operations
  getAllRoles(): Promise<Role[]>;
  getRoleById(id: string): Promise<Role | undefined>;
  getRoleCategories(): Promise<string[]>;
  createRole(role: InsertRole): Promise<Role>;
  getRoleSkills(roleId: string): Promise<any[]>;

  // Skill operations
  getAllSkills(): Promise<Skill[]>;
  getSkillById(id: string): Promise<Skill | undefined>;
  getSkillsByNames(names: string[]): Promise<Skill[]>;
  createSkill(skill: InsertSkill): Promise<Skill>;

  // User Skills
  getUserSkills(userId: string): Promise<any[]>;
  createUserSkill(userSkill: InsertUserSkill): Promise<UserSkill>;

  // Roadmap operations
  getUserRoadmap(userId: string): Promise<Roadmap | undefined>;
  createRoadmap(roadmap: InsertRoadmap): Promise<Roadmap>;

  // Progress operations
  getUserProgress(userId: string): Promise<UserProgress[]>;
  createOrUpdateProgress(progress: InsertUserProgress): Promise<UserProgress>;

  // Chat operations
  getUserChatMessages(userId: string, limit?: number): Promise<ChatMessage[]>;
  createChatMessage(message: InsertChatMessage): Promise<ChatMessage>;

  // Stats
  getUserStats(userId: string): Promise<any>;
  getUserActivity(userId: string): Promise<any[]>;
}

export class DatabaseStorage implements IStorage {
  // User operations
  async getUser(id: string): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user;
  }

  async getUserByEmail(email: string): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.email, email));
    return user;
  }

  async upsertUser(userData: UpsertUser): Promise<User> {
    const [user] = await db
      .insert(users)
      .values(userData)
      .onConflictDoUpdate({
        target: users.id,
        set: {
          ...userData,
          updatedAt: new Date(),
        },
      })
      .returning();
    return user;
  }

  // CV operations
  async getUserLatestCv(userId: string): Promise<UserCv | undefined> {
    const [cv] = await db
      .select()
      .from(userCvs)
      .where(eq(userCvs.userId, userId))
      .orderBy(desc(userCvs.uploadedAt))
      .limit(1);
    return cv;
  }

  async createUserCv(cvData: InsertUserCv): Promise<UserCv> {
    const [cv] = await db.insert(userCvs).values(cvData).returning();
    return cv;
  }

  // Role operations
  async getAllRoles(): Promise<Role[]> {
    return await db.select().from(roles);
  }

  async getRoleById(id: string): Promise<Role | undefined> {
    const [role] = await db.select().from(roles).where(eq(roles.id, id));
    return role;
  }

  async getRoleCategories(): Promise<string[]> {
    const result = await db.selectDistinct({ category: roles.category }).from(roles);
    return result.map(r => r.category);
  }

  async createRole(roleData: InsertRole): Promise<Role> {
    const [role] = await db.insert(roles).values(roleData).returning();
    return role;
  }

  async getRoleSkills(roleId: string): Promise<any[]> {
    return await db
      .select({
        skillId: skills.id,
        skillName: skills.name,
        category: skills.category,
        importance: roleSkills.importance,
        proficiencyLevel: roleSkills.proficiencyLevel,
      })
      .from(roleSkills)
      .innerJoin(skills, eq(roleSkills.skillId, skills.id))
      .where(eq(roleSkills.roleId, roleId));
  }

  // Skill operations
  async getAllSkills(): Promise<Skill[]> {
    return await db.select().from(skills);
  }

  async getSkillById(id: string): Promise<Skill | undefined> {
    const [skill] = await db.select().from(skills).where(eq(skills.id, id));
    return skill;
  }

  async getSkillsByNames(names: string[]): Promise<Skill[]> {
    if (names.length === 0) return [];
    return await db.select().from(skills).where(inArray(skills.name, names));
  }

  async createSkill(skillData: InsertSkill): Promise<Skill> {
    const [skill] = await db.insert(skills).values(skillData).returning();
    return skill;
  }

  // User Skills
  async getUserSkills(userId: string): Promise<any[]> {
    return await db
      .select({
        skillId: skills.id,
        skillName: skills.name,
        category: skills.category,
        proficiencyLevel: userSkills.proficiencyLevel,
        source: userSkills.source,
      })
      .from(userSkills)
      .innerJoin(skills, eq(userSkills.skillId, skills.id))
      .where(eq(userSkills.userId, userId));
  }

  async createUserSkill(userSkillData: InsertUserSkill): Promise<UserSkill> {
    const [userSkill] = await db.insert(userSkills).values(userSkillData).returning();
    return userSkill;
  }

  // Roadmap operations
  async getUserRoadmap(userId: string): Promise<Roadmap | undefined> {
    const [roadmap] = await db
      .select()
      .from(roadmaps)
      .where(eq(roadmaps.userId, userId))
      .orderBy(desc(roadmaps.createdAt))
      .limit(1);
    return roadmap;
  }

  async createRoadmap(roadmapData: InsertRoadmap): Promise<Roadmap> {
    const [roadmap] = await db.insert(roadmaps).values(roadmapData).returning();
    return roadmap;
  }

  // Progress operations
  async getUserProgress(userId: string): Promise<UserProgress[]> {
    return await db.select().from(userProgress).where(eq(userProgress.userId, userId));
  }

  async createOrUpdateProgress(progressData: InsertUserProgress): Promise<UserProgress> {
    const existing = await db
      .select()
      .from(userProgress)
      .where(
        and(
          eq(userProgress.userId, progressData.userId),
          eq(userProgress.skillId, progressData.skillId)
        )
      )
      .limit(1);

    if (existing.length > 0) {
      const [updated] = await db
        .update(userProgress)
        .set({
          status: progressData.status,
          completedAt: progressData.status === 'completed' ? new Date() : null,
          notes: progressData.notes,
        })
        .where(eq(userProgress.id, existing[0].id))
        .returning();
      return updated;
    } else {
      const [created] = await db.insert(userProgress).values(progressData).returning();
      return created;
    }
  }

  // Chat operations
  async getUserChatMessages(userId: string, limit: number = 50): Promise<ChatMessage[]> {
    return await db
      .select()
      .from(chatMessages)
      .where(eq(chatMessages.userId, userId))
      .orderBy(chatMessages.createdAt)
      .limit(limit);
  }

  async createChatMessage(messageData: InsertChatMessage): Promise<ChatMessage> {
    const [message] = await db.insert(chatMessages).values(messageData).returning();
    return message;
  }

  // Stats
  async getUserStats(userId: string): Promise<any> {
    const userSkillsList = await this.getUserSkills(userId);
    const progress = await this.getUserProgress(userId);
    const completedSkills = progress.filter(p => p.status === 'completed');

    return {
      skillsIdentified: userSkillsList.length,
      skillsCompleted: completedSkills.length,
      estimatedHours: 0, // Can be calculated based on roadmap
    };
  }

  async getUserActivity(userId: string): Promise<any[]> {
    const recentCvs = await db
      .select()
      .from(userCvs)
      .where(eq(userCvs.userId, userId))
      .orderBy(desc(userCvs.uploadedAt))
      .limit(5);

    return recentCvs.map(cv => ({
      title: `Uploaded CV: ${cv.fileName}`,
      timestamp: cv.uploadedAt?.toLocaleDateString() || 'Recently',
    }));
  }
}

console.log('📦 Storage mode: DATABASE');
export const storage: IStorage = new DatabaseStorage();


