import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, TrendingUp, CheckCircle, Clock, Upload, Compass } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useQuery } from "@tanstack/react-query";
import { Skeleton } from "@/components/ui/skeleton";
import { useEffect } from "react";
import { useToast } from "@/hooks/use-toast";

export default function Dashboard() {
  const { user, isLoading: authLoading } = useAuth();
  const { toast } = useToast();

  // Redirect to home if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      toast({
        title: "Unauthorized",
        description: "You are logged out. Logging in again...",
        variant: "destructive",
      });
      setTimeout(() => {
        window.location.href = "/api/login";
      }, 500);
    }
  }, [user, authLoading, toast]);

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["/api/user/stats"],
    enabled: !!user,
  });

  const { data: recentActivity, isLoading: activityLoading } = useQuery({
    queryKey: ["/api/user/activity"],
    enabled: !!user,
  });

  if (authLoading) {
    return <div className="p-8">Loading...</div>;
  }

  if (!user) {
    return null;
  }

  const userName = user.firstName || user.email?.split('@')[0] || 'there';

  return (
    <div className="p-8 space-y-8">
      {/* Welcome Section */}
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold" data-testid="text-welcome">
          Welcome back, {userName}!
        </h1>
        <p className="text-muted-foreground" data-testid="text-welcome-subtitle">
          Your journey to the perfect career starts here.
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid md:grid-cols-3 gap-6">
        {statsLoading ? (
          <>
            <Card><CardContent className="p-6"><Skeleton className="h-20" /></CardContent></Card>
            <Card><CardContent className="p-6"><Skeleton className="h-20" /></CardContent></Card>
            <Card><CardContent className="p-6"><Skeleton className="h-20" /></CardContent></Card>
          </>
        ) : (
          <>
            <Card data-testid="card-stats-skills">
              <CardHeader className="flex flex-row items-center justify-between gap-2 space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Skills Identified</CardTitle>
                <CheckCircle className="w-4 h-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold" data-testid="text-stats-skills">{stats?.skillsIdentified || 0}</div>
                <p className="text-xs text-muted-foreground mt-1">From your CV analysis</p>
              </CardContent>
            </Card>
            <Card data-testid="card-stats-progress">
              <CardHeader className="flex flex-row items-center justify-between gap-2 space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Skills Completed</CardTitle>
                <TrendingUp className="w-4 h-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold" data-testid="text-stats-completed">{stats?.skillsCompleted || 0}</div>
                <p className="text-xs text-muted-foreground mt-1">On your learning path</p>
              </CardContent>
            </Card>
            <Card data-testid="card-stats-time">
              <CardHeader className="flex flex-row items-center justify-between gap-2 space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Learning Time</CardTitle>
                <Clock className="w-4 h-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold" data-testid="text-stats-time">{stats?.estimatedHours || 0}h</div>
                <p className="text-xs text-muted-foreground mt-1">Estimated remaining</p>
              </CardContent>
            </Card>
          </>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card data-testid="card-action-upload">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Upload className="w-5 h-5 text-primary" />
              </div>
              <div>
                <CardTitle>Analyze Your Skills</CardTitle>
                <CardDescription>Upload your CV to get started with AI-powered analysis</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <Button className="w-full" asChild data-testid="button-upload-cv">
              <a href="/analysis">
                <FileText className="w-4 h-4 mr-2" />
                Upload Resume
              </a>
            </Button>
          </CardContent>
        </Card>

        <Card data-testid="card-action-explore">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Compass className="w-5 h-5 text-primary" />
              </div>
              <div>
                <CardTitle>Explore Careers</CardTitle>
                <CardDescription>Discover career paths that match your interests and skills</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <Button variant="outline" className="w-full" asChild data-testid="button-explore-careers">
              <a href="/careers">
                <Compass className="w-4 h-4 mr-2" />
                Browse Roles
              </a>
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card data-testid="card-recent-activity">
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Your latest career exploration journey</CardDescription>
        </CardHeader>
        <CardContent>
          {activityLoading ? (
            <div className="space-y-3">
              <Skeleton className="h-12" />
              <Skeleton className="h-12" />
              <Skeleton className="h-12" />
            </div>
          ) : recentActivity && recentActivity.length > 0 ? (
            <div className="space-y-4">
              {recentActivity.map((activity: any, idx: number) => (
                <div key={idx} className="flex items-center gap-4 p-3 rounded-lg border" data-testid={`activity-${idx}`}>
                  <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <CheckCircle className="w-4 h-4 text-primary" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium">{activity.title}</p>
                    <p className="text-xs text-muted-foreground">{activity.timestamp}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-muted-foreground" data-testid="text-no-activity">
              <p>No recent activity yet. Start by uploading your CV or exploring careers!</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Next Steps */}
      <Card data-testid="card-next-steps">
        <CardHeader>
          <CardTitle>Next Steps</CardTitle>
          <CardDescription>Recommended actions to advance your career journey</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-3 p-3 rounded-lg border hover-elevate" data-testid="next-step-1">
            <div className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center flex-shrink-0 text-xs font-medium">
              1
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium">Complete your skill analysis</p>
              <p className="text-xs text-muted-foreground">Upload your CV to identify your strengths</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 rounded-lg border hover-elevate" data-testid="next-step-2">
            <div className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center flex-shrink-0 text-xs font-medium">
              2
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium">Choose your target role</p>
              <p className="text-xs text-muted-foreground">Browse our career catalog to find your path</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 rounded-lg border hover-elevate" data-testid="next-step-3">
            <div className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center flex-shrink-0 text-xs font-medium">
              3
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium">Get your personalized roadmap</p>
              <p className="text-xs text-muted-foreground">See exactly what to learn and when</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
