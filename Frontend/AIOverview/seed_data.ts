// Seed PostgreSQL with sample data
import { config } from "dotenv";
config();

import { db } from "./server/db";
import { roles, skills, roleSkills } from "./shared/schema";
import { eq } from "drizzle-orm";

const sampleRoles = [
  {
    id: "software_engineer",
    name: "Software Engineer",
    category: "Engineering",
    description: "Design, develop, and maintain software applications using modern technologies",
    responsibilities: ["Write clean code", "Design systems", "Test applications", "Collaborate with teams"],
    averageSalary: "$95,000",
    demandLevel: "High",
  },
  {
    id: "frontend_developer",
    name: "Frontend Developer",
    category: "Engineering",
    description: "Build user-facing web applications and interfaces with modern frameworks",
    responsibilities: ["Create UI components", "Optimize performance", "Ensure responsive design"],
    averageSalary: "$85,000",
    demandLevel: "High",
  },
  {
    id: "backend_developer",
    name: "Backend Developer",
    category: "Engineering",
    description: "Build server-side logic and database systems that power applications",
    responsibilities: ["Design APIs", "Manage databases", "Optimize server performance"],
    averageSalary: "$92,000",
    demandLevel: "High",
  },
  {
    id: "data_scientist",
    name: "Data Scientist",
    category: "Data & Analytics",
    description: "Analyze complex data and build predictive models using machine learning",
    responsibilities: ["Build ML models", "Analyze data", "Create visualizations"],
    averageSalary: "$120,000",
    demandLevel: "Very High",
  },
  {
    id: "devops_engineer",
    name: "DevOps Engineer",
    category: "Engineering",
    description: "Manage infrastructure and deployment pipelines for reliable software delivery",
    responsibilities: ["Automate deployments", "Monitor systems", "Manage cloud infrastructure"],
    averageSalary: "$105,000",
    demandLevel: "High",
  },
];

const sampleSkills = [
  { id: "python", name: "Python", category: "Programming Languages", difficultyLevel: "Intermediate", estimatedLearningTime: 60, description: "General-purpose programming language" },
  { id: "javascript", name: "JavaScript", category: "Programming Languages", difficultyLevel: "Intermediate", estimatedLearningTime: 50, description: "Essential web programming language" },
  { id: "react", name: "React", category: "Frontend Frameworks", difficultyLevel: "Intermediate", estimatedLearningTime: 40, description: "Popular UI library for building web apps" },
  { id: "nodejs", name: "Node.js", category: "Backend Frameworks", difficultyLevel: "Intermediate", estimatedLearningTime: 45, description: "JavaScript runtime for server-side development" },
  { id: "sql", name: "SQL", category: "Databases", difficultyLevel: "Beginner", estimatedLearningTime: 30, description: "Standard language for relational databases" },
  { id: "mongodb", name: "MongoDB", category: "Databases", difficultyLevel: "Intermediate", estimatedLearningTime: 35, description: "Popular NoSQL database" },
  { id: "git", name: "Git", category: "Tools", difficultyLevel: "Beginner", estimatedLearningTime: 20, description: "Version control system" },
  { id: "docker", name: "Docker", category: "DevOps", difficultyLevel: "Advanced", estimatedLearningTime: 40, description: "Containerization platform" },
  { id: "aws", name: "AWS", category: "Cloud Platforms", difficultyLevel: "Advanced", estimatedLearningTime: 60, description: "Amazon cloud services" },
  { id: "machine_learning", name: "Machine Learning", category: "Data Science", difficultyLevel: "Expert", estimatedLearningTime: 120, description: "AI and predictive modeling" },
  { id: "data_analysis", name: "Data Analysis", category: "Data Science", difficultyLevel: "Intermediate", estimatedLearningTime: 50, description: "Analyzing and interpreting data" },
  { id: "communication", name: "Communication", category: "Soft Skills", difficultyLevel: "Intermediate", estimatedLearningTime: 40, description: "Effective communication in teams" },
  { id: "problem_solving", name: "Problem Solving", category: "Soft Skills", difficultyLevel: "Intermediate", estimatedLearningTime: 40, description: "Analytical thinking and problem resolution" },
];

const roleSkillsMapping = [
  // Software Engineer
  { roleId: "software_engineer", skillId: "python", importance: "critical", proficiencyLevel: "Advanced" },
  { roleId: "software_engineer", skillId: "javascript", importance: "high", proficiencyLevel: "Advanced" },
  { roleId: "software_engineer", skillId: "git", importance: "critical", proficiencyLevel: "Intermediate" },
  { roleId: "software_engineer", skillId: "sql", importance: "high", proficiencyLevel: "Intermediate" },
  
  // Frontend Developer
  { roleId: "frontend_developer", skillId: "javascript", importance: "critical", proficiencyLevel: "Expert" },
  { roleId: "frontend_developer", skillId: "react", importance: "critical", proficiencyLevel: "Advanced" },
  { roleId: "frontend_developer", skillId: "git", importance: "high", proficiencyLevel: "Intermediate" },
  
  // Backend Developer
  { roleId: "backend_developer", skillId: "python", importance: "critical", proficiencyLevel: "Advanced" },
  { roleId: "backend_developer", skillId: "nodejs", importance: "high", proficiencyLevel: "Advanced" },
  { roleId: "backend_developer", skillId: "sql", importance: "critical", proficiencyLevel: "Advanced" },
  { roleId: "backend_developer", skillId: "mongodb", importance: "high", proficiencyLevel: "Intermediate" },
  { roleId: "backend_developer", skillId: "git", importance: "critical", proficiencyLevel: "Intermediate" },
  
  // Data Scientist
  { roleId: "data_scientist", skillId: "python", importance: "critical", proficiencyLevel: "Expert" },
  { roleId: "data_scientist", skillId: "machine_learning", importance: "critical", proficiencyLevel: "Expert" },
  { roleId: "data_scientist", skillId: "data_analysis", importance: "critical", proficiencyLevel: "Advanced" },
  { roleId: "data_scientist", skillId: "sql", importance: "high", proficiencyLevel: "Intermediate" },
  
  // DevOps Engineer
  { roleId: "devops_engineer", skillId: "docker", importance: "critical", proficiencyLevel: "Advanced" },
  { roleId: "devops_engineer", skillId: "aws", importance: "critical", proficiencyLevel: "Advanced" },
  { roleId: "devops_engineer", skillId: "git", importance: "high", proficiencyLevel: "Advanced" },
  { roleId: "devops_engineer", skillId: "python", importance: "high", proficiencyLevel: "Intermediate" },
];

async function seedDatabase() {
  console.log("🌱 Seeding PostgreSQL database...\n");

  try {
    // Insert roles
    console.log("Inserting roles...");
    for (const role of sampleRoles) {
      try {
        await db.insert(roles).values(role).onConflictDoNothing();
        console.log(`✅ Role: ${role.name}`);
      } catch (error) {
        console.log(`⚠️  Role ${role.name} already exists`);
      }
    }

    // Insert skills
    console.log("\nInserting skills...");
    for (const skill of sampleSkills) {
      try {
        await db.insert(skills).values(skill).onConflictDoNothing();
        console.log(`✅ Skill: ${skill.name}`);
      } catch (error) {
        console.log(`⚠️  Skill ${skill.name} already exists`);
      }
    }

    // Insert role-skill relationships
    console.log("\nCreating role-skill relationships...");
    for (const mapping of roleSkillsMapping) {
      try {
        await db.insert(roleSkills).values(mapping).onConflictDoNothing();
      } catch (error) {
        // Ignore duplicate errors
      }
    }
    console.log(`✅ ${roleSkillsMapping.length} relationships created`);

    console.log("\n🎉 Database seeding complete!");
    console.log("\nSummary:");
    console.log(`  - ${sampleRoles.length} roles`);
    console.log(`  - ${sampleSkills.length} skills`);
    console.log(`  - ${roleSkillsMapping.length} role-skill relationships`);

  } catch (error) {
    console.error("❌ Error seeding database:", error);
    throw error;
  }

  process.exit(0);
}

seedDatabase();
