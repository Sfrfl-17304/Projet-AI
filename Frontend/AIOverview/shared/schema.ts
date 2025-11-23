import { sql } from 'drizzle-orm';
import {
  index,
  jsonb,
  pgTable,
  timestamp,
  varchar,
  text,
  integer,
  boolean,
} from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// Session storage table (required for Replit Auth)
export const sessions = pgTable(
  "sessions",
  {
    sid: varchar("sid").primaryKey(),
    sess: jsonb("sess").notNull(),
    expire: timestamp("expire").notNull(),
  },
  (table) => [index("IDX_session_expire").on(table.expire)],
);

// User storage table (required for Replit Auth)
export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  email: varchar("email").unique(),
  firstName: varchar("first_name"),
  lastName: varchar("last_name"),
  profileImageUrl: varchar("profile_image_url"),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const usersRelations = relations(users, ({ many }) => ({
  cvs: many(userCvs),
  userSkills: many(userSkills),
  progress: many(userProgress),
  chatMessages: many(chatMessages),
  roadmaps: many(roadmaps),
}));

// User CVs
export const userCvs = pgTable("user_cvs", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").notNull().references(() => users.id, { onDelete: 'cascade' }),
  fileName: varchar("file_name").notNull(),
  fileContent: text("file_content").notNull(),
  uploadedAt: timestamp("uploaded_at").defaultNow(),
  extractedSkills: jsonb("extracted_skills"),
});

export const userCvsRelations = relations(userCvs, ({ one }) => ({
  user: one(users, {
    fields: [userCvs.userId],
    references: [users.id],
  }),
}));

// Career Roles
export const roles = pgTable("roles", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  name: varchar("name").notNull().unique(),
  category: varchar("category").notNull(),
  description: text("description").notNull(),
  responsibilities: jsonb("responsibilities").notNull(),
  averageSalary: varchar("average_salary"),
  demandLevel: varchar("demand_level"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const rolesRelations = relations(roles, ({ many }) => ({
  roleSkills: many(roleSkills),
  roadmaps: many(roadmaps),
}));

// Skills
export const skills = pgTable("skills", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  name: varchar("name").notNull().unique(),
  category: varchar("category").notNull(),
  difficultyLevel: varchar("difficulty_level"),
  estimatedLearningTime: integer("estimated_learning_time"),
  description: text("description"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const skillsRelations = relations(skills, ({ many }) => ({
  roleSkills: many(roleSkills),
  userSkills: many(userSkills),
  learningResources: many(learningResources),
  prerequisites: many(skillPrerequisites, { relationName: "skill" }),
  dependents: many(skillPrerequisites, { relationName: "prerequisite" }),
}));

// Role Skills (many-to-many)
export const roleSkills = pgTable("role_skills", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  roleId: varchar("role_id").notNull().references(() => roles.id, { onDelete: 'cascade' }),
  skillId: varchar("skill_id").notNull().references(() => skills.id, { onDelete: 'cascade' }),
  importance: varchar("importance").notNull(),
  proficiencyLevel: varchar("proficiency_level"),
});

export const roleSkillsRelations = relations(roleSkills, ({ one }) => ({
  role: one(roles, {
    fields: [roleSkills.roleId],
    references: [roles.id],
  }),
  skill: one(skills, {
    fields: [roleSkills.skillId],
    references: [skills.id],
  }),
}));

// User Skills (many-to-many)
export const userSkills = pgTable("user_skills", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").notNull().references(() => users.id, { onDelete: 'cascade' }),
  skillId: varchar("skill_id").notNull().references(() => skills.id, { onDelete: 'cascade' }),
  proficiencyLevel: varchar("proficiency_level"),
  source: varchar("source"),
  addedAt: timestamp("added_at").defaultNow(),
});

export const userSkillsRelations = relations(userSkills, ({ one }) => ({
  user: one(users, {
    fields: [userSkills.userId],
    references: [users.id],
  }),
  skill: one(skills, {
    fields: [userSkills.skillId],
    references: [skills.id],
  }),
}));

// Skill Prerequisites (self-referencing)
export const skillPrerequisites = pgTable("skill_prerequisites", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  skillId: varchar("skill_id").notNull().references(() => skills.id, { onDelete: 'cascade' }),
  prerequisiteId: varchar("prerequisite_id").notNull().references(() => skills.id, { onDelete: 'cascade' }),
});

export const skillPrerequisitesRelations = relations(skillPrerequisites, ({ one }) => ({
  skill: one(skills, {
    fields: [skillPrerequisites.skillId],
    references: [skills.id],
    relationName: "skill",
  }),
  prerequisite: one(skills, {
    fields: [skillPrerequisites.prerequisiteId],
    references: [skills.id],
    relationName: "prerequisite",
  }),
}));

// Learning Resources
export const learningResources = pgTable("learning_resources", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  skillId: varchar("skill_id").notNull().references(() => skills.id, { onDelete: 'cascade' }),
  title: varchar("title").notNull(),
  type: varchar("type").notNull(),
  url: text("url"),
  description: text("description"),
  difficulty: varchar("difficulty"),
  duration: varchar("duration"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const learningResourcesRelations = relations(learningResources, ({ one }) => ({
  skill: one(skills, {
    fields: [learningResources.skillId],
    references: [skills.id],
  }),
}));

// User Roadmaps
export const roadmaps = pgTable("roadmaps", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").notNull().references(() => users.id, { onDelete: 'cascade' }),
  roleId: varchar("role_id").notNull().references(() => roles.id, { onDelete: 'cascade' }),
  name: varchar("name").notNull(),
  estimatedDuration: integer("estimated_duration"),
  milestones: jsonb("milestones").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const roadmapsRelations = relations(roadmaps, ({ one }) => ({
  user: one(users, {
    fields: [roadmaps.userId],
    references: [users.id],
  }),
  role: one(roles, {
    fields: [roadmaps.roleId],
    references: [roles.id],
  }),
}));

// User Progress
export const userProgress = pgTable("user_progress", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").notNull().references(() => users.id, { onDelete: 'cascade' }),
  skillId: varchar("skill_id").notNull().references(() => skills.id, { onDelete: 'cascade' }),
  status: varchar("status").notNull(),
  completedAt: timestamp("completed_at"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const userProgressRelations = relations(userProgress, ({ one }) => ({
  user: one(users, {
    fields: [userProgress.userId],
    references: [users.id],
  }),
  skill: one(skills, {
    fields: [userProgress.skillId],
    references: [skills.id],
  }),
}));

// Chat Messages
export const chatMessages = pgTable("chat_messages", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").notNull().references(() => users.id, { onDelete: 'cascade' }),
  role: varchar("role").notNull(),
  content: text("content").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const chatMessagesRelations = relations(chatMessages, ({ one }) => ({
  user: one(users, {
    fields: [chatMessages.userId],
    references: [users.id],
  }),
}));

// Zod schemas and types
export type UpsertUser = typeof users.$inferInsert;
export type User = typeof users.$inferSelect;

export const insertUserCvSchema = createInsertSchema(userCvs).omit({ id: true, uploadedAt: true });
export type InsertUserCv = z.infer<typeof insertUserCvSchema>;
export type UserCv = typeof userCvs.$inferSelect;

export const insertRoleSchema = createInsertSchema(roles).omit({ id: true, createdAt: true });
export type InsertRole = z.infer<typeof insertRoleSchema>;
export type Role = typeof roles.$inferSelect;

export const insertSkillSchema = createInsertSchema(skills).omit({ id: true, createdAt: true });
export type InsertSkill = z.infer<typeof insertSkillSchema>;
export type Skill = typeof skills.$inferSelect;

export const insertRoleSkillSchema = createInsertSchema(roleSkills).omit({ id: true });
export type InsertRoleSkill = z.infer<typeof insertRoleSkillSchema>;
export type RoleSkill = typeof roleSkills.$inferSelect;

export const insertUserSkillSchema = createInsertSchema(userSkills).omit({ id: true, addedAt: true });
export type InsertUserSkill = z.infer<typeof insertUserSkillSchema>;
export type UserSkill = typeof userSkills.$inferSelect;

export const insertLearningResourceSchema = createInsertSchema(learningResources).omit({ id: true, createdAt: true });
export type InsertLearningResource = z.infer<typeof insertLearningResourceSchema>;
export type LearningResource = typeof learningResources.$inferSelect;

export const insertRoadmapSchema = createInsertSchema(roadmaps).omit({ id: true, createdAt: true, updatedAt: true });
export type InsertRoadmap = z.infer<typeof insertRoadmapSchema>;
export type Roadmap = typeof roadmaps.$inferSelect;

export const insertUserProgressSchema = createInsertSchema(userProgress).omit({ id: true, createdAt: true });
export type InsertUserProgress = z.infer<typeof insertUserProgressSchema>;
export type UserProgress = typeof userProgress.$inferSelect;

export const insertChatMessageSchema = createInsertSchema(chatMessages).omit({ id: true, createdAt: true });
export type InsertChatMessage = z.infer<typeof insertChatMessageSchema>;
export type ChatMessage = typeof chatMessages.$inferSelect;
