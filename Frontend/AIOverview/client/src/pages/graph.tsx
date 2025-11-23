import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ZoomIn, ZoomOut, Maximize2, Network as NetworkIcon } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/use-toast";
import { useQuery } from "@tanstack/react-query";

export default function Graph() {
  const { user, isLoading: authLoading } = useAuth();
  const { toast } = useToast();
  const [zoom, setZoom] = useState(100);

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

  const { data: graphData, isLoading } = useQuery({
    queryKey: ["/api/graph"],
    enabled: !!user,
  });

  if (authLoading || !user) {
    return <div className="p-8">Loading...</div>;
  }

  return (
    <div className="p-8 space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold" data-testid="text-page-title">Knowledge Graph</h1>
        <p className="text-muted-foreground" data-testid="text-page-subtitle">
          Interactive visualization of skills, roles, and their relationships
        </p>
      </div>

      {/* Controls */}
      <Card data-testid="card-controls">
        <CardContent className="p-4">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <Button
                size="icon"
                variant="outline"
                onClick={() => setZoom(Math.max(25, zoom - 25))}
                data-testid="button-zoom-out"
              >
                <ZoomOut className="w-4 h-4" />
              </Button>
              <span className="text-sm font-medium min-w-[4rem] text-center" data-testid="text-zoom-level">
                {zoom}%
              </span>
              <Button
                size="icon"
                variant="outline"
                onClick={() => setZoom(Math.min(200, zoom + 25))}
                data-testid="button-zoom-in"
              >
                <ZoomIn className="w-4 h-4" />
              </Button>
              <Button
                size="icon"
                variant="outline"
                onClick={() => setZoom(100)}
                data-testid="button-reset-zoom"
              >
                <Maximize2 className="w-4 h-4" />
              </Button>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-primary" />
                <span className="text-sm">Roles</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-chart-2" />
                <span className="text-sm">Skills</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-chart-3" />
                <span className="text-sm">Tools</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Graph Canvas */}
      <Card data-testid="card-graph">
        <CardHeader>
          <CardTitle>Skill Relationships</CardTitle>
          <CardDescription>Visualize how your skills connect to your target career path</CardDescription>
        </CardHeader>
        <CardContent>
          <div
            className="border-2 border-dashed rounded-lg flex items-center justify-center bg-muted/10"
            style={{ minHeight: "500px", transform: `scale(${zoom / 100})`, transformOrigin: "center center" }}
            data-testid="graph-canvas"
          >
            {isLoading ? (
              <div className="text-center space-y-3">
                <NetworkIcon className="w-12 h-12 mx-auto text-muted-foreground animate-pulse" />
                <p className="text-muted-foreground">Loading knowledge graph...</p>
              </div>
            ) : graphData ? (
              <div className="text-center space-y-3">
                <NetworkIcon className="w-12 h-12 mx-auto text-primary" />
                <p className="text-muted-foreground">Interactive graph will be rendered here</p>
              </div>
            ) : (
              <div className="text-center space-y-3 p-8">
                <NetworkIcon className="w-12 h-12 mx-auto text-muted-foreground" />
                <div className="space-y-2">
                  <p className="font-medium">No graph data available</p>
                  <p className="text-sm text-muted-foreground">
                    Complete your skill analysis and select a target role to generate your knowledge graph
                  </p>
                </div>
                <Button asChild data-testid="button-get-started">
                  <a href="/analysis">Get Started</a>
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Legend */}
      <div className="grid md:grid-cols-3 gap-6">
        <Card data-testid="card-legend-roles">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-primary" />
              Career Roles
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Larger nodes representing different career paths and their requirements
            </p>
          </CardContent>
        </Card>
        <Card data-testid="card-legend-skills">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-chart-2" />
              Skills
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Medium nodes showing technical and soft skills connected to roles
            </p>
          </CardContent>
        </Card>
        <Card data-testid="card-legend-tools">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-chart-3" />
              Tools & Technologies
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Smaller nodes representing specific tools, frameworks, and technologies
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
