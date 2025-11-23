// Seed data for initial roles and skills
import { db } from "./db";
import { roles, skills, roleSkills } from "@shared/schema";
import { eq } from "drizzle-orm";

const seedRoles = [
  {
    name: "Data Engineer",
    category: "Data & Analytics",
    description: "Design and build systems for collecting, storing, and analyzing data at scale. Work with big data technologies and create data pipelines.",
    responsibilities: [
      "Design and implement scalable data pipelines",
      "Build and maintain data warehouses",
      "Optimize database performance",
      "Work with big data technologies like Spark and Hadoop",
      "Collaborate with data scientists and analysts"
    ],
    averageSalary: "$110,000 - $160,000",
    demandLevel: "Very High"
  },
  {
    name: "Full-Stack Web Developer",
    category: "Software Development",
    description: "Build complete web applications from frontend to backend. Work across the entire stack including databases, servers, and user interfaces.",
    responsibilities: [
      "Develop responsive web applications",
      "Build RESTful APIs and backend services",
      "Implement database schemas and queries",
      "Create intuitive user interfaces",
      "Deploy and maintain applications"
    ],
    averageSalary: "$90,000 - $140,000",
    demandLevel: "High"
  },
  {
    name: "Machine Learning Engineer",
    category: "AI & Machine Learning",
    description: "Design and implement machine learning models and systems. Build scalable ML infrastructure and deploy models to production.",
    responsibilities: [
      "Build and train machine learning models",
      "Implement ML pipelines and workflows",
      "Deploy models to production environments",
      "Optimize model performance and accuracy",
      "Research and implement new ML techniques"
    ],
    averageSalary: "$120,000 - $180,000",
    demandLevel: "Very High"
  },
  {
    name: "DevOps Engineer",
    category: "Infrastructure & Operations",
    description: "Bridge development and operations teams. Automate infrastructure, implement CI/CD pipelines, and ensure system reliability.",
    responsibilities: [
      "Automate deployment and infrastructure",
      "Implement CI/CD pipelines",
      "Monitor system performance and reliability",
      "Manage cloud infrastructure",
      "Ensure security and compliance"
    ],
    averageSalary: "$105,000 - $155,000",
    demandLevel: "High"
  },
  {
    name: "Mobile App Developer",
    category: "Software Development",
    description: "Create native or cross-platform mobile applications for iOS and Android. Focus on user experience and performance.",
    responsibilities: [
      "Develop mobile applications",
      "Implement responsive designs",
      "Integrate with backend APIs",
      "Optimize app performance",
      "Test across devices and platforms"
    ],
    averageSalary: "$95,000 - $145,000",
    demandLevel: "High"
  },
  {
    name: "Cloud Architect",
    category: "Infrastructure & Operations",
    description: "Design and implement cloud-based solutions. Define cloud strategy and ensure scalable, secure infrastructure.",
    responsibilities: [
      "Design cloud architecture solutions",
      "Implement security and compliance",
      "Optimize cloud costs",
      "Lead cloud migrations",
      "Ensure high availability and disaster recovery"
    ],
    averageSalary: "$130,000 - $190,000",
    demandLevel: "Very High"
  }
];

const seedSkills = [
  // Programming Languages
  { name: "Python", category: "Programming Language", difficultyLevel: "Beginner", estimatedLearningTime: 80, description: "General-purpose programming language" },
  { name: "JavaScript", category: "Programming Language", difficultyLevel: "Beginner", estimatedLearningTime: 60, description: "Web programming language" },
  { name: "TypeScript", category: "Programming Language", difficultyLevel: "Intermediate", estimatedLearningTime: 40, description: "Typed superset of JavaScript" },
  { name: "Java", category: "Programming Language", difficultyLevel: "Intermediate", estimatedLearningTime: 100, description: "Enterprise programming language" },
  { name: "Go", category: "Programming Language", difficultyLevel: "Intermediate", estimatedLearningTime: 60, description: "Modern systems programming language" },
  
  // Databases
  { name: "SQL", category: "Database", difficultyLevel: "Beginner", estimatedLearningTime: 40, description: "Database query language" },
  { name: "PostgreSQL", category: "Database", difficultyLevel: "Intermediate", estimatedLearningTime: 60, description: "Advanced relational database" },
  { name: "MongoDB", category: "Database", difficultyLevel: "Intermediate", estimatedLearningTime: 50, description: "NoSQL document database" },
  { name: "Redis", category: "Database", difficultyLevel: "Intermediate", estimatedLearningTime: 30, description: "In-memory data store" },
  
  // Web Development
  { name: "React", category: "Frontend Framework", difficultyLevel: "Intermediate", estimatedLearningTime: 80, description: "JavaScript UI library" },
  { name: "Node.js", category: "Backend Framework", difficultyLevel: "Intermediate", estimatedLearningTime: 70, description: "JavaScript runtime" },
  { name: "HTML & CSS", category: "Frontend", difficultyLevel: "Beginner", estimatedLearningTime: 50, description: "Web markup and styling" },
  { name: "REST APIs", category: "Backend", difficultyLevel: "Intermediate", estimatedLearningTime: 40, description: "Web service architecture" },
  
  // Data Engineering
  { name: "Apache Spark", category: "Big Data", difficultyLevel: "Advanced", estimatedLearningTime: 120, description: "Distributed data processing" },
  { name: "Apache Kafka", category: "Big Data", difficultyLevel: "Advanced", estimatedLearningTime: 100, description: "Event streaming platform" },
  { name: "Data Warehousing", category: "Data Engineering", difficultyLevel: "Advanced", estimatedLearningTime: 100, description: "Data warehouse concepts" },
  { name: "ETL Pipelines", category: "Data Engineering", difficultyLevel: "Intermediate", estimatedLearningTime: 80, description: "Data pipeline development" },
  { name: "AWS/GCP", category: "Cloud Platform", difficultyLevel: "Intermediate", estimatedLearningTime: 90, description: "Cloud services" },
  
  // Machine Learning
  { name: "Machine Learning", category: "AI/ML", difficultyLevel: "Advanced", estimatedLearningTime: 150, description: "ML algorithms and theory" },
  { name: "TensorFlow", category: "AI/ML", difficultyLevel: "Advanced", estimatedLearningTime: 120, description: "ML framework" },
  { name: "PyTorch", category: "AI/ML", difficultyLevel: "Advanced", estimatedLearningTime: 120, description: "ML framework" },
  { name: "Data Analysis", category: "Data Science", difficultyLevel: "Intermediate", estimatedLearningTime: 80, description: "Statistical analysis" },
  
  // DevOps
  { name: "Docker", category: "DevOps", difficultyLevel: "Intermediate", estimatedLearningTime: 60, description: "Containerization platform" },
  { name: "Kubernetes", category: "DevOps", difficultyLevel: "Advanced", estimatedLearningTime: 100, description: "Container orchestration" },
  { name: "CI/CD", category: "DevOps", difficultyLevel: "Intermediate", estimatedLearningTime: 70, description: "Continuous integration/deployment" },
  { name: "Terraform", category: "DevOps", difficultyLevel: "Intermediate", estimatedLearningTime: 60, description: "Infrastructure as code" },
  
  // Mobile
  { name: "React Native", category: "Mobile Development", difficultyLevel: "Intermediate", estimatedLearningTime: 80, description: "Cross-platform mobile framework" },
  { name: "Swift", category: "Mobile Development", difficultyLevel: "Intermediate", estimatedLearningTime: 90, description: "iOS development language" },
  { name: "Kotlin", category: "Mobile Development", difficultyLevel: "Intermediate", estimatedLearningTime: 80, description: "Android development language" },
  
  // Soft Skills
  { name: "Problem Solving", category: "Soft Skill", difficultyLevel: "Intermediate", estimatedLearningTime: 200, description: "Analytical thinking" },
  { name: "Communication", category: "Soft Skill", difficultyLevel: "Beginner", estimatedLearningTime: 150, description: "Team collaboration" },
  { name: "Git", category: "Version Control", difficultyLevel: "Beginner", estimatedLearningTime: 30, description: "Version control system" },
];

const roleSkillMappings = {
  "Data Engineer": [
    { skill: "Python", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "SQL", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Apache Spark", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Apache Kafka", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Data Warehousing", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "ETL Pipelines", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "AWS/GCP", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "PostgreSQL", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Problem Solving", importance: "Important", proficiencyLevel: "Advanced" },
  ],
  "Full-Stack Web Developer": [
    { skill: "JavaScript", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "TypeScript", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "React", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Node.js", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "HTML & CSS", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "REST APIs", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "SQL", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Git", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Problem Solving", importance: "Important", proficiencyLevel: "Intermediate" },
  ],
  "Machine Learning Engineer": [
    { skill: "Python", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Machine Learning", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "TensorFlow", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "PyTorch", importance: "Important", proficiencyLevel: "Advanced" },
    { skill: "Data Analysis", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "SQL", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Problem Solving", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Git", importance: "Important", proficiencyLevel: "Intermediate" },
  ],
  "DevOps Engineer": [
    { skill: "Docker", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Kubernetes", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "CI/CD", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Terraform", importance: "Important", proficiencyLevel: "Advanced" },
    { skill: "AWS/GCP", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Python", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Git", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Problem Solving", importance: "Important", proficiencyLevel: "Advanced" },
  ],
  "Mobile App Developer": [
    { skill: "React Native", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "JavaScript", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "TypeScript", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Swift", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Kotlin", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "REST APIs", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Git", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Problem Solving", importance: "Important", proficiencyLevel: "Intermediate" },
  ],
  "Cloud Architect": [
    { skill: "AWS/GCP", importance: "Critical", proficiencyLevel: "Expert" },
    { skill: "Docker", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Kubernetes", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "Terraform", importance: "Critical", proficiencyLevel: "Advanced" },
    { skill: "CI/CD", importance: "Important", proficiencyLevel: "Advanced" },
    { skill: "Python", importance: "Important", proficiencyLevel: "Intermediate" },
    { skill: "Problem Solving", importance: "Critical", proficiencyLevel: "Expert" },
    { skill: "Communication", importance: "Critical", proficiencyLevel: "Advanced" },
  ],
};

export async function seedDatabase() {
  console.log("Starting database seeding...");

  // Check if already seeded
  const existingRoles = await db.select().from(roles).limit(1);
  if (existingRoles.length > 0) {
    console.log("Database already seeded, skipping...");
    return;
  }

  // Insert skills
  console.log("Inserting skills...");
  const insertedSkills = await db.insert(skills).values(seedSkills).returning();
  const skillMap = new Map(insertedSkills.map(s => [s.name, s.id]));

  // Insert roles
  console.log("Inserting roles...");
  const insertedRoles = await db.insert(roles).values(seedRoles).returning();
  const roleMap = new Map(insertedRoles.map(r => [r.name, r.id]));

  // Insert role-skill mappings
  console.log("Creating role-skill relationships...");
  for (const [roleName, skillMappings] of Object.entries(roleSkillMappings)) {
    const roleId = roleMap.get(roleName);
    if (!roleId) continue;

    for (const mapping of skillMappings) {
      const skillId = skillMap.get(mapping.skill);
      if (!skillId) continue;

      await db.insert(roleSkills).values({
        roleId,
        skillId,
        importance: mapping.importance,
        proficiencyLevel: mapping.proficiencyLevel,
      });
    }
  }

  console.log("Database seeding completed!");
}
