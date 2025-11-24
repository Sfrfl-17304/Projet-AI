// Hugging Face integration for CV parsing, roadmap generation, and chat
import { HfInference } from '@huggingface/inference';

// Initialize Hugging Face client
let hf: HfInference | null = null;

function getHuggingFace() {
  if (!process.env.HUGGINGFACE_API_KEY) {
    throw new Error('HUGGINGFACE_API_KEY is not configured');
  }
  if (!hf) {
    hf = new HfInference(process.env.HUGGINGFACE_API_KEY);
  }
  return hf;
}

// Default models to use (can be customized)
const MODELS = {
  // For text generation and analysis
  TEXT_GENERATION: 'mistralai/Mixtral-8x7B-Instruct-v0.1',
  // Alternative: 'meta-llama/Llama-2-70b-chat-hf', 'tiiuae/falcon-180B-chat'
};

/**
 * Extract skills from CV text using Hugging Face
 */
export async function extractSkillsFromCV(cvText: string): Promise<{
  skills: string[];
  technicalSkills: string[];
  softSkills: string[];
  tools: string[];
}> {
  try {
    const client = getHuggingFace();
    
    const prompt = `You are an expert career advisor and skill extraction specialist. Extract all skills from the CV text provided. Categorize them into technical skills, soft skills, and tools/technologies. Return ONLY a JSON object with these categories. Be comprehensive and identify both explicitly mentioned and implied skills.

Format your response as a valid JSON object:
{
  "skills": ["all skills combined"],
  "technicalSkills": ["programming languages, frameworks, databases, etc"],
  "softSkills": ["communication, leadership, problem-solving, etc"],
  "tools": ["specific tools, software, platforms"]
}

CV Text:
${cvText.substring(0, 3000)}

JSON Response:`;

    const response = await client.textGeneration({
      model: MODELS.TEXT_GENERATION,
      inputs: prompt,
      parameters: {
        max_new_tokens: 500,
        temperature: 0.3,
        top_p: 0.9,
        return_full_text: false,
      },
    });

    // Extract JSON from response
    const text = response.generated_text;
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      const result = JSON.parse(jsonMatch[0]);
      return {
        skills: result.skills || [],
        technicalSkills: result.technicalSkills || result.technical_skills || [],
        softSkills: result.softSkills || result.soft_skills || [],
        tools: result.tools || [],
      };
    }
    
    // Fallback if JSON parsing fails
    console.warn("Failed to parse JSON from Hugging Face response, using fallback");
    return {
      skills: ["JavaScript", "React", "Python", "Communication", "Problem-solving"],
      technicalSkills: ["JavaScript", "React", "Python", "Node.js", "SQL"],
      softSkills: ["Communication", "Problem-solving", "Teamwork", "Leadership"],
      tools: ["VS Code", "Git", "Docker"],
    };
  } catch (error) {
    console.error("Error extracting skills from CV:", error);
    throw new Error("Failed to extract skills from CV");
  }
}

/**
 * Generate a learning roadmap using Hugging Face
 */
export async function generateRoadmap(params: {
  userSkills: string[];
  targetRole: string;
  missingSkills: string[];
  estimatedMonths?: number;
}): Promise<any> {
  try {
    const client = getHuggingFace();
    
    const prompt = `You are an expert career coach creating personalized learning roadmaps. Generate a detailed, time-sequenced learning path that takes the user from their current skill level to their target role.

Structure the roadmap into phases (Foundation, Intermediate, Advanced) with specific milestones. Return ONLY a JSON object.

Format your response as a valid JSON object:
{
  "name": "Roadmap name",
  "estimatedDuration": total months (number),
  "milestones": [
    {
      "name": "milestone name",
      "phase": "Foundation/Intermediate/Advanced",
      "estimatedWeeks": number,
      "skills": [
        {
          "name": "skill name",
          "description": "what this skill involves",
          "estimatedHours": number,
          "isPrerequisite": boolean,
          "resources": []
        }
      ]
    }
  ]
}

Current skills: ${params.userSkills.join(", ")}
Target role: ${params.targetRole}
Skills to acquire: ${params.missingSkills.join(", ")}
Target duration: ${params.estimatedMonths || 12} months

JSON Response:`;

    const response = await client.textGeneration({
      model: MODELS.TEXT_GENERATION,
      inputs: prompt,
      parameters: {
        max_new_tokens: 1500,
        temperature: 0.4,
        top_p: 0.9,
        return_full_text: false,
      },
    });

    // Extract JSON from response
    const text = response.generated_text;
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      const roadmap = JSON.parse(jsonMatch[0]);
      return roadmap;
    }
    
    // Fallback roadmap
    console.warn("Failed to parse JSON from Hugging Face response, using fallback roadmap");
    return {
      name: `Roadmap to ${params.targetRole}`,
      estimatedDuration: params.estimatedMonths || 12,
      milestones: [
        {
          name: "Foundation Phase",
          phase: "Foundation",
          estimatedWeeks: 12,
          skills: params.missingSkills.slice(0, 3).map(skill => ({
            name: skill,
            description: `Learn ${skill} fundamentals`,
            estimatedHours: 40,
            isPrerequisite: true,
            resources: []
          }))
        }
      ]
    };
  } catch (error) {
    console.error("Error generating roadmap:", error);
    throw new Error("Failed to generate roadmap");
  }
}

/**
 * Chat assistant using Hugging Face
 */
export async function chatWithAssistant(params: {
  userMessage: string;
  conversationHistory: Array<{ role: string; content: string }>;
  userContext?: {
    skills?: string[];
    targetRole?: string;
  };
}): Promise<string> {
  try {
    const client = getHuggingFace();
    
    // Build context
    let contextStr = "You are SkillAtlas Assistant, an AI career guidance expert. Help users explore career paths, understand skill requirements, and navigate their learning journey. Be encouraging, specific, and provide actionable advice.\n\n";
    
    if (params.userContext?.skills) {
      contextStr += `User's current skills: ${params.userContext.skills.join(", ")}\n`;
    }
    if (params.userContext?.targetRole) {
      contextStr += `User's target role: ${params.userContext.targetRole}\n`;
    }
    contextStr += "\nKeep responses concise, friendly, and focused on career development.\n\n";
    
    // Add conversation history
    const history = params.conversationHistory.slice(-6).map(msg => 
      `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`
    ).join('\n');
    
    const prompt = `${contextStr}${history}\nUser: ${params.userMessage}\nAssistant:`;

    const response = await client.textGeneration({
      model: MODELS.TEXT_GENERATION,
      inputs: prompt,
      parameters: {
        max_new_tokens: 300,
        temperature: 0.7,
        top_p: 0.9,
        return_full_text: false,
      },
    });

    return response.generated_text.trim() || "I apologize, but I couldn't generate a response. Please try again.";
  } catch (error) {
    console.error("Error in chat assistant:", error);
    throw new Error("Failed to get response from assistant");
  }
}
