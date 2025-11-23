import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Clock, CheckCircle, Circle, Lock, ExternalLink, BookOpen } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/use-toast";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Skeleton } from "@/components/ui/skeleton";
import { apiRequest, queryClient } from "@/lib/queryClient";
import { isUnauthorizedError } from "@/lib/authUtils";

export default function Roadmap() {
  const { user, isLoading: authLoading } = useAuth();
  const { toast } = useToast();
  const [selectedMilestone, setSelectedMilestone] = useState<any | null>(null);

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

  const { data: roadmap, isLoading } = useQuery({
    queryKey: ["/api/roadmap"],
    enabled: !!user,
  });

  const progressMutation = useMutation({
    mutationFn: async ({ skillId, status }: { skillId: string; status: string }) => {
      return await apiRequest("POST", "/api/skills/progress", { skillId, status });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/roadmap"] });
      toast({
        title: "Progress updated",
        description: "Your learning progress has been saved.",
      });
    },
    onError: (error: Error) => {
      if (isUnauthorizedError(error)) {
        toast({
          title: "Unauthorized",
          description: "You are logged out. Logging in again...",
          variant: "destructive",
        });
        setTimeout(() => {
          window.location.href = "/api/login";
        }, 500);
        return;
      }
      toast({
        title: "Error",
        description: "Failed to update progress. Please try again.",
        variant: "destructive",
      });
    },
  });

  if (authLoading || !user) {
    return <div className="p-8">Loading...</div>;
  }

  const calculateProgress = () => {
    if (!roadmap?.milestones) return 0;
    const total = roadmap.milestones.reduce((acc: number, m: any) => acc + m.skills.length, 0);
    const completed = roadmap.milestones.reduce(
      (acc: number, m: any) => acc + m.skills.filter((s: any) => s.status === "completed").length,
      0
    );
    return total > 0 ? Math.round((completed / total) * 100) : 0;
  };

  return (
    <div className="p-8 space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold" data-testid="text-page-title">
          {roadmap?.name || "Full-Stack Web Developer Path"}
        </h1>
        <p className="text-muted-foreground" data-testid="text-page-subtitle">
          Your personalized journey to becoming a professional web developer, from foundational concepts to advanced architecture.
        </p>
      </div>

      {/* Progress Overview */}
      {roadmap && (
        <Card data-testid="card-progress">
          <CardHeader>
            <div className="flex items-center justify-between gap-4">
              <div>
                <CardTitle>Overall Progress</CardTitle>
                <CardDescription data-testid="text-progress-percentage">{calculateProgress()}% Complete</CardDescription>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold" data-testid="text-estimated-duration">
                  {roadmap.estimatedDuration || 12} months
                </p>
                <p className="text-xs text-muted-foreground">Estimated duration</p>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <Progress value={calculateProgress()} className="h-2" data-testid="progress-bar" />
          </CardContent>
        </Card>
      )}

      {/* Timeline */}
      <div className="space-y-6">
        <h2 className="text-xl font-semibold" data-testid="text-timeline-title">Learning Timeline</h2>
        {isLoading ? (
          <div className="space-y-6">
            {[1, 2, 3].map((i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-6 w-1/3" />
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
                <CardContent>
                  <Skeleton className="h-32" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : roadmap?.milestones ? (
          <div className="space-y-6">
            {roadmap.milestones.map((milestone: any, idx: number) => (
              <Card key={idx} data-testid={`card-milestone-${idx}`}>
                <CardHeader>
                  <div className="flex items-start justify-between gap-4">
                    <div className="space-y-1 flex-1">
                      <CardTitle data-testid={`text-milestone-name-${idx}`}>{milestone.name}</CardTitle>
                      <CardDescription className="flex items-center gap-2">
                        <Clock className="w-4 h-4" />
                        <span data-testid={`text-milestone-duration-${idx}`}>
                          Time Estimate: {milestone.estimatedWeeks || 4} Weeks
                        </span>
                      </CardDescription>
                    </div>
                    <Badge variant="secondary" data-testid={`badge-milestone-phase-${idx}`}>
                      {milestone.phase || "Foundation"}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  {milestone.skills?.map((skill: any, skillIdx: number) => (
                    <div
                      key={skillIdx}
                      className={`flex items-start gap-3 p-3 border rounded-lg ${
                        skill.status === "completed" ? "bg-muted/50" : ""
                      }`}
                      data-testid={`skill-${idx}-${skillIdx}`}
                    >
                      <div className="flex-shrink-0 mt-0.5">
                        {skill.status === "completed" ? (
                          <CheckCircle className="w-5 h-5 text-primary" />
                        ) : skill.isLocked ? (
                          <Lock className="w-5 h-5 text-muted-foreground" />
                        ) : (
                          <Circle className="w-5 h-5 text-muted-foreground" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0 space-y-2">
                        <div>
                          <h4 className="font-medium text-sm" data-testid={`text-skill-name-${idx}-${skillIdx}`}>
                            {skill.name}
                          </h4>
                          <p className="text-xs text-muted-foreground" data-testid={`text-skill-description-${idx}-${skillIdx}`}>
                            {skill.description}
                          </p>
                        </div>
                        {skill.resources && skill.resources.length > 0 && (
                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => setSelectedMilestone(skill)}
                              data-testid={`button-view-resources-${idx}-${skillIdx}`}
                            >
                              <BookOpen className="w-3 h-3 mr-1" />
                              View Resources
                            </Button>
                          </div>
                        )}
                      </div>
                      {!skill.isLocked && (
                        <Button
                          size="sm"
                          variant={skill.status === "completed" ? "outline" : "default"}
                          onClick={() =>
                            progressMutation.mutate({
                              skillId: skill.id,
                              status: skill.status === "completed" ? "in_progress" : "completed",
                            })
                          }
                          data-testid={`button-toggle-status-${idx}-${skillIdx}`}
                        >
                          {skill.status === "completed" ? "Mark Incomplete" : "Mark Complete"}
                        </Button>
                      )}
                    </div>
                  ))}
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="p-12 text-center">
              <p className="text-muted-foreground" data-testid="text-no-roadmap">
                No roadmap generated yet. Complete your skill analysis and select a target role to get started.
              </p>
              <Button asChild className="mt-4" data-testid="button-get-started">
                <a href="/analysis">Get Started</a>
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
