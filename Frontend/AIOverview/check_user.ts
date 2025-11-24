import { db } from "./server/db";
import { users } from "./shared/schema";
import { eq } from "drizzle-orm";

async function checkUser() {
  try {
    const userId = "ab40220c-cbb3-4a4d-8038-e521af44de2c";
    const [user] = await db.select().from(users).where(eq(users.id, userId));
    
    if (user) {
      console.log("✅ User found:");
      console.log("  ID:", user.id);
      console.log("  Email:", user.email);
      console.log("  Password hash length:", user.password?.length);
      console.log("  Password starts with:", user.password?.substring(0, 7));
      console.log("  Created at:", user.createdAt);
    } else {
      console.log("❌ User not found");
    }
    
    // Also check all users
    const allUsers = await db.select({
      id: users.id,
      email: users.email,
      createdAt: users.createdAt
    }).from(users);
    
    console.log("\nAll users in database:", allUsers.length);
    allUsers.forEach(u => {
      console.log(`  - ${u.email} (${u.id.substring(0, 8)}...)`);
    });
    
    process.exit(0);
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

checkUser();
