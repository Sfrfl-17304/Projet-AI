import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search, Briefcase, DollarSign, TrendingUp, X } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/use-toast";
import { useQuery } from "@tanstack/react-query";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

export default function Careers() {
  const { user, isLoading: authLoading } = useAuth();
  const { toast } = useToast();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedRole, setSelectedRole] = useState<any | null>(null);

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

  const { data: roles, isLoading } = useQuery({
    queryKey: ["/api/roles"],
    enabled: !!user,
  });

  const { data: categories } = useQuery({
    queryKey: ["/api/roles/categories"],
    enabled: !!user,
  });

  if (authLoading || !user) {
    return <div className="p-8">Loading...</div>;
  }

  const filteredRoles = roles?.filter((role: any) => {
    const matchesSearch = role.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         role.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !selectedCategory || role.category === selectedCategory;
    return matchesSearch && matchesCategory;
  }) || [];

  return (
    <div className="p-8 space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold" data-testid="text-page-title">Career Explorer</h1>
        <p className="text-muted-foreground" data-testid="text-page-subtitle">
          Discover career paths that match your interests and skills
        </p>
      </div>

      {/* Search and Filters */}
      <Card data-testid="card-search">
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search for roles..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
                data-testid="input-search-roles"
              />
            </div>
            <div className="flex gap-2 flex-wrap">
              {categories?.map((category: string) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedCategory(selectedCategory === category ? null : category)}
                  data-testid={`filter-${category.toLowerCase().replace(/\s+/g, '-')}`}
                >
                  {category}
                  {selectedCategory === category && (
                    <X className="w-3 h-3 ml-2" />
                  )}
                </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Roles Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          <>
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-6 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
                <CardContent>
                  <Skeleton className="h-20" />
                </CardContent>
              </Card>
            ))}
          </>
        ) : filteredRoles.length > 0 ? (
          filteredRoles.map((role: any) => (
            <Card
              key={role.id}
              className="hover-elevate cursor-pointer transition-all"
              onClick={() => setSelectedRole(role)}
              data-testid={`card-role-${role.id}`}
            >
              <CardHeader>
                <div className="flex items-start justify-between gap-2">
                  <div className="space-y-1 flex-1">
                    <CardTitle className="text-lg">{role.name}</CardTitle>
                    <Badge variant="secondary" data-testid={`badge-category-${role.id}`}>
                      {role.category}
                    </Badge>
                  </div>
                  <Briefcase className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground line-clamp-3" data-testid={`text-description-${role.id}`}>
                  {role.description}
                </p>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  {role.averageSalary && (
                    <div className="flex items-center gap-1">
                      <DollarSign className="w-3 h-3" />
                      <span data-testid={`text-salary-${role.id}`}>{role.averageSalary}</span>
                    </div>
                  )}
                  {role.demandLevel && (
                    <div className="flex items-center gap-1">
                      <TrendingUp className="w-3 h-3" />
                      <span data-testid={`text-demand-${role.id}`}>{role.demandLevel}</span>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <div className="col-span-full text-center py-12" data-testid="text-no-results">
            <p className="text-muted-foreground">No roles found matching your criteria.</p>
          </div>
        )}
      </div>

      {/* Role Details Dialog */}
      <Dialog open={!!selectedRole} onOpenChange={() => setSelectedRole(null)}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto" data-testid="dialog-role-details">
          {selectedRole && (
            <>
              <DialogHeader>
                <DialogTitle data-testid="text-dialog-role-name">{selectedRole.name}</DialogTitle>
                <DialogDescription>
                  <Badge variant="secondary" data-testid="text-dialog-category">{selectedRole.category}</Badge>
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-6">
                <div>
                  <h3 className="font-medium mb-2">Description</h3>
                  <p className="text-sm text-muted-foreground" data-testid="text-dialog-description">
                    {selectedRole.description}
                  </p>
                </div>
                {selectedRole.responsibilities && (
                  <div>
                    <h3 className="font-medium mb-2">Key Responsibilities</h3>
                    <ul className="space-y-1">
                      {selectedRole.responsibilities.map((resp: string, idx: number) => (
                        <li key={idx} className="text-sm text-muted-foreground flex items-start gap-2" data-testid={`responsibility-${idx}`}>
                          <span className="text-primary mt-1">•</span>
                          <span>{resp}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                <div className="flex gap-3 pt-4">
                  <Button asChild className="flex-1" data-testid="button-view-roadmap">
                    <a href={`/roadmap?role=${selectedRole.id}`}>View Learning Roadmap</a>
                  </Button>
                  <Button variant="outline" asChild className="flex-1" data-testid="button-analyze-skills">
                    <a href={`/analysis?role=${selectedRole.id}`}>Analyze Skills</a>
                  </Button>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
