import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, Compass, TrendingUp, MessageSquare, Network, BookOpen } from "lucide-react";

export default function Landing() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <Network className="w-8 h-8 text-primary" data-testid="logo-icon" />
              <span className="text-2xl font-semibold" data-testid="text-logo">SkillAtlas</span>
            </div>
            <div className="flex items-center gap-4">
              <a href="#how-it-works" className="text-sm font-medium hover-elevate px-3 py-2 rounded-md" data-testid="link-how-it-works">
                How It Works
              </a>
              <a href="#features" className="text-sm font-medium hover-elevate px-3 py-2 rounded-md" data-testid="link-features">
                Features
              </a>
              <Button asChild data-testid="button-login">
                <a href="/auth">Login</a>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h1 className="text-5xl font-bold tracking-tight" data-testid="text-hero-title">
                Map Your Future.
                <br />
                Discover Your Ideal Career with AI.
              </h1>
              <p className="text-xl text-muted-foreground leading-relaxed" data-testid="text-hero-subtitle">
                SkillAtlas analyzes your skills or interests to reveal personalized career paths and the steps to get there.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Button size="lg" asChild data-testid="button-get-started">
                  <a href="/auth">Get Started Free</a>
                </Button>
                <Button size="lg" variant="outline" asChild data-testid="button-learn-more">
                  <a href="#how-it-works">Learn More</a>
                </Button>
              </div>
              <p className="text-sm text-muted-foreground pt-2" data-testid="text-trust-indicator">
                Join thousands of students discovering their career paths
              </p>
            </div>
            <div className="relative">
              <Card className="p-6" data-testid="card-hero-preview">
                <CardHeader className="space-y-0 pb-2">
                  <CardTitle className="text-base font-medium">Your Skills vs Target Role</CardTitle>
                  <CardDescription>Data Engineer Analysis</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Python</span>
                      <span className="font-medium text-primary">Advanced</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">SQL</span>
                      <span className="font-medium text-primary">Advanced</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Apache Spark</span>
                      <span className="font-medium text-destructive">Missing</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Data Warehousing</span>
                      <span className="font-medium text-destructive">Missing</span>
                    </div>
                  </div>
                  <Button variant="outline" className="w-full" data-testid="button-preview-roadmap">
                    <TrendingUp className="w-4 h-4 mr-2" />
                    View Learning Roadmap
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-3xl font-semibold" data-testid="text-how-it-works-title">How It Works</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto" data-testid="text-how-it-works-subtitle">
              Three simple steps to discover your perfect career path
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <Card data-testid="card-step-1">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <FileText className="w-6 h-6 text-primary" />
                </div>
                <CardTitle>Upload Your CV</CardTitle>
                <CardDescription>
                  Or answer questions about your interests if you're just starting out
                </CardDescription>
              </CardHeader>
            </Card>
            <Card data-testid="card-step-2">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <Network className="w-6 h-6 text-primary" />
                </div>
                <CardTitle>AI Analysis</CardTitle>
                <CardDescription>
                  Our AI extracts your skills and matches them with thousands of career paths
                </CardDescription>
              </CardHeader>
            </Card>
            <Card data-testid="card-step-3">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <TrendingUp className="w-6 h-6 text-primary" />
                </div>
                <CardTitle>Get Your Roadmap</CardTitle>
                <CardDescription>
                  Receive a personalized learning path with time estimates and resources
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-3xl font-semibold" data-testid="text-features-title">Powerful Features</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto" data-testid="text-features-subtitle">
              Everything you need to navigate your career journey
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-12">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                <FileText className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold" data-testid="text-feature-skill-extraction">AI-Powered Skill Extraction</h3>
              <p className="text-muted-foreground leading-relaxed">
                Advanced NLP models automatically identify technical and soft skills from your CV with high accuracy.
              </p>
            </div>
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                <Network className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold" data-testid="text-feature-knowledge-graph">Knowledge Graph Visualization</h3>
              <p className="text-muted-foreground leading-relaxed">
                Interactive visualizations showing relationships between roles, skills, and career progression paths.
              </p>
            </div>
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                <MessageSquare className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold" data-testid="text-feature-ai-assistant">AI Career Assistant</h3>
              <p className="text-muted-foreground leading-relaxed">
                Chat with our RAG-powered assistant to get instant answers to your career questions.
              </p>
            </div>
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold" data-testid="text-feature-learning-roadmap">Personalized Learning Roadmaps</h3>
              <p className="text-muted-foreground leading-relaxed">
                Time-sequenced learning paths with realistic estimates and curated resources for each skill.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-3xl font-semibold" data-testid="text-use-cases-title">Who Is This For?</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-8">
            <Card data-testid="card-use-case-cv">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-primary" />
                  I Have a CV
                </CardTitle>
                <CardDescription className="leading-relaxed">
                  Perfect for students and early professionals with internships, projects, or coursework experience. Get precise skill gap analysis and targeted recommendations.
                </CardDescription>
              </CardHeader>
            </Card>
            <Card data-testid="card-use-case-beginner">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Compass className="w-5 h-5 text-primary" />
                  I'm Just Starting
                </CardTitle>
                <CardDescription className="leading-relaxed">
                  Ideal for beginners, career changers, or undecided students. Explore careers based on your interests and get beginner-friendly learning paths.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center space-y-6">
          <h2 className="text-4xl font-bold tracking-tight" data-testid="text-cta-title">
            Ready to Discover Your Path?
          </h2>
          <p className="text-xl text-muted-foreground" data-testid="text-cta-subtitle">
            Join thousands of students mapping their career journeys with AI-powered guidance.
          </p>
          <Button size="lg" asChild data-testid="button-cta-start">
            <a href="/auth">Get Started Free</a>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center text-sm text-muted-foreground">
          <p data-testid="text-footer">&copy; 2024 SkillAtlas. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
