// OpenAI integration for CV parsing and chat - referenced from javascript_openai blueprint
import OpenAI from "openai";

// the newest OpenAI model is "gpt-5" which was released August 7, 2025. do not change this unless explicitly requested by the user
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function extractSkillsFromCV(cvText: string): Promise<{
  skills: string[];
  technicalSkills: string[];
  softSkills: string[];
  tools: string[];
}> {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-5",
      messages: [
        {
          role: "system",
          content: `You are an expert career advisor and skill extraction specialist. Extract all skills from the CV text provided. Categorize them into technical skills, soft skills, and tools/technologies. Return a JSON object with these categories. Be comprehensive and identify both explicitly mentioned and implied skills.

Format: {
  "skills": ["all skills combined"],
  "technicalSkills": ["programming languages, frameworks, databases, etc"],
  "softSkills": ["communication, leadership, problem-solving, etc"],
  "tools": ["specific tools, software, platforms"]
}`
        },
        {
          role: "user",
          content: `Extract all skills from this CV:\n\n${cvText}`
        }
      ],
      response_format: { type: "json_object" },
      max_completion_tokens: 2048,
    });

    const result = JSON.parse(response.choices[0].message.content || "{}");
    return {
      skills: result.skills || [],
      technicalSkills: result.technicalSkills || [],
      softSkills: result.softSkills || [],
      tools: result.tools || [],
    };
  } catch (error) {
    console.error("Error extracting skills from CV:", error);
    throw new Error("Failed to extract skills from CV");
  }
}

export async function generateRoadmap(params: {
  userSkills: string[];
  targetRole: string;
  missingSkills: string[];
  estimatedMonths?: number;
}): Promise<any> {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-5",
      messages: [
        {
          role: "system",
          content: `You are an expert career coach creating personalized learning roadmaps. Generate a detailed, time-sequenced learning path that takes the user from their current skill level to their target role. 

Structure the roadmap into phases (Foundation, Intermediate, Advanced) with specific milestones. Each milestone should contain:
- name: clear milestone name
- phase: Foundation/Intermediate/Advanced
- estimatedWeeks: realistic time estimate
- skills: array of skills to learn in this phase, each with:
  - name: skill name
  - description: what this skill involves
  - estimatedHours: hours to learn
  - isPrerequisite: boolean if needed for next skills
  - resources: learning resources (optional)

Return a JSON object with structure:
{
  "name": "Roadmap name",
  "estimatedDuration": total months,
  "milestones": [array of milestone objects]
}`
        },
        {
          role: "user",
          content: `Create a learning roadmap for:
- Current skills: ${params.userSkills.join(", ")}
- Target role: ${params.targetRole}
- Skills to acquire: ${params.missingSkills.join(", ")}
- Target duration: ${params.estimatedMonths || 12} months`
        }
      ],
      response_format: { type: "json_object" },
      max_completion_tokens: 4096,
    });

    const roadmap = JSON.parse(response.choices[0].message.content || "{}");
    return roadmap;
  } catch (error) {
    console.error("Error generating roadmap:", error);
    throw new Error("Failed to generate roadmap");
  }
}

export async function chatWithAssistant(params: {
  userMessage: string;
  conversationHistory: Array<{ role: string; content: string }>;
  userContext?: {
    skills?: string[];
    targetRole?: string;
  };
}): Promise<string> {
  try {
    const systemPrompt = `You are SkillAtlas Assistant, an AI career guidance expert. Help users explore career paths, understand skill requirements, and navigate their learning journey. Be encouraging, specific, and provide actionable advice.

${params.userContext?.skills ? `User's current skills: ${params.userContext.skills.join(", ")}` : ""}
${params.userContext?.targetRole ? `User's target role: ${params.userContext.targetRole}` : ""}

Keep responses concise, friendly, and focused on career development.`;

    const messages = [
      { role: "system", content: systemPrompt },
      ...params.conversationHistory.slice(-10), // Keep last 10 messages for context
      { role: "user", content: params.userMessage },
    ];

    const response = await openai.chat.completions.create({
      model: "gpt-5",
      messages: messages as any,
      max_completion_tokens: 1024,
    });

    return response.choices[0].message.content || "I apologize, but I couldn't generate a response. Please try again.";
  } catch (error) {
    console.error("Error in chat assistant:", error);
    throw new Error("Failed to get response from assistant");
  }
}
