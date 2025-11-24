import { config } from "dotenv";

// Load environment variables FIRST
config();

import bcrypt from "bcryptjs";
import { db } from "./server/db";
import { users } from "./shared/schema";

async function populateUsers() {
  if (!db) {
    console.error("❌ Database connection not available");
    return;
  }

  console.log("🔐 Creating sample users...");

  const sampleUsers = [
    {
      email: "demo@skillatlas.com",
      password: "demo123",
      firstName: "Demo",
      lastName: "User",
    },
    {
      email: "alice@example.com",
      password: "password123",
      firstName: "Alice",
      lastName: "Johnson",
    },
    {
      email: "bob@example.com",
      password: "password123",
      firstName: "Bob",
      lastName: "Smith",
    },
  ];

  for (const userData of sampleUsers) {
    try {
      // Hash password
      const hashedPassword = await bcrypt.hash(userData.password, 10);

      // Insert user
      await db.insert(users).values({
        email: userData.email,
        password: hashedPassword,
        firstName: userData.firstName,
        lastName: userData.lastName,
      }).onConflictDoNothing();

      console.log(`✅ Created user: ${userData.email}`);
    } catch (error) {
      console.error(`❌ Failed to create ${userData.email}:`, error);
    }
  }

  console.log("\n✅ Sample users created successfully!");
  console.log("\nYou can login with:");
  console.log("  Email: demo@skillatlas.com");
  console.log("  Password: demo123");
}

populateUsers()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Error:", error);
    process.exit(1);
  });
