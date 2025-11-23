import { useState, useCallback, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileText, Loader2, CheckCircle, X, Search } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/use-toast";
import { useMutation, useQuery } from "@tanstack/react-query";
import { apiRequest, queryClient } from "@/lib/queryClient";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { isUnauthorizedError } from "@/lib/authUtils";

export default function Analysis() {
  const { user, isLoading: authLoading } = useAuth();
  const { toast } = useToast();
  const [file, setFile] = useState<File | null>(null);
  const [selectedRole, setSelectedRole] = useState<string>("");
  const [isDragging, setIsDragging] = useState(false);

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

  const { data: userCv, isLoading: cvLoading } = useQuery({
    queryKey: ["/api/cv/latest"],
    enabled: !!user,
  });

  const { data: roles } = useQuery({
    queryKey: ["/api/roles"],
    enabled: !!user,
  });

  const { data: analysis, isLoading: analysisLoading } = useQuery({
    queryKey: ["/api/cv/analysis", selectedRole],
    enabled: !!user && !!userCv && !!selectedRole,
  });

  const uploadMutation = useMutation({
    mutationFn: async (formData: FormData) => {
      return await apiRequest("POST", "/api/cv/upload", formData);
    },
    onSuccess: () => {
      toast({
        title: "Success",
        description: "Your CV has been uploaded and analyzed successfully!",
      });
      queryClient.invalidateQueries({ queryKey: ["/api/cv/latest"] });
      setFile(null);
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
        description: error.message || "Failed to upload CV. Please try again.",
        variant: "destructive",
      });
    },
  });

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
    } else {
      toast({
        title: "Invalid file",
        description: "Please upload a PDF file",
        variant: "destructive",
      });
    }
  }, [toast]);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
    } else {
      toast({
        title: "Invalid file",
        description: "Please upload a PDF file",
        variant: "destructive",
      });
    }
  }, [toast]);

  const handleUpload = useCallback(() => {
    if (!file) return;
    const formData = new FormData();
    formData.append("cv", file);
    uploadMutation.mutate(formData);
  }, [file, uploadMutation]);

  if (authLoading || !user) {
    return <div className="p-8">Loading...</div>;
  }

  return (
    <div className="p-8 space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold" data-testid="text-page-title">Analyze Your Skills for a New Career</h1>
        <p className="text-muted-foreground" data-testid="text-page-subtitle">
          Upload your resume to see how your skills align with your career goals.
        </p>
      </div>

      {/* Upload Section */}
      <Card data-testid="card-upload">
        <CardContent className="p-6">
          <div
            className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
              isDragging ? "border-primary bg-primary/5" : "border-border"
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            data-testid="dropzone-upload"
          >
            <div className="flex flex-col items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                <Upload className="w-8 h-8 text-primary" />
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-medium" data-testid="text-upload-title">Upload Your Resume to Begin</h3>
                <p className="text-sm text-muted-foreground" data-testid="text-upload-subtitle">
                  Drag and drop a PDF file or browse your computer.
                </p>
              </div>
              {file ? (
                <div className="flex items-center gap-3 p-3 border rounded-lg bg-background" data-testid="file-preview">
                  <FileText className="w-5 h-5 text-primary" />
                  <span className="text-sm font-medium">{file.name}</span>
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => setFile(null)}
                    data-testid="button-remove-file"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              ) : null}
              <div className="flex gap-3">
                <Button
                  variant="outline"
                  onClick={() => document.getElementById("cv-upload")?.click()}
                  data-testid="button-browse"
                >
                  Browse Files
                </Button>
                {file && (
                  <Button
                    onClick={handleUpload}
                    disabled={uploadMutation.isPending}
                    data-testid="button-upload-submit"
                  >
                    {uploadMutation.isPending ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      "Upload Resume"
                    )}
                  </Button>
                )}
              </div>
              <input
                id="cv-upload"
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={handleFileChange}
                data-testid="input-file-upload"
              />
              <p className="text-xs text-muted-foreground">PDF files only • Max 10MB</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Role Selection */}
      {userCv && (
        <Card data-testid="card-role-selection">
          <CardHeader>
            <CardTitle>Select Target Role</CardTitle>
            <CardDescription>Choose a career path to analyze your skill gaps</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-3">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Select value={selectedRole} onValueChange={setSelectedRole}>
                  <SelectTrigger className="pl-10" data-testid="select-target-role">
                    <SelectValue placeholder="Search for a role..." />
                  </SelectTrigger>
                  <SelectContent>
                    {roles?.map((role: any) => (
                      <SelectItem key={role.id} value={role.id}>
                        {role.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Skills Analysis */}
      {userCv && selectedRole && (
        <div className="grid md:grid-cols-2 gap-6">
          <Card data-testid="card-your-skills">
            <CardHeader>
              <CardTitle>Your Skills</CardTitle>
              <CardDescription>Identified from your resume</CardDescription>
            </CardHeader>
            <CardContent>
              {cvLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
                </div>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {userCv.extractedSkills?.skills?.map((skill: string, idx: number) => (
                    <Badge key={idx} variant="secondary" data-testid={`skill-${idx}`}>
                      <CheckCircle className="w-3 h-3 mr-1 text-primary" />
                      {skill}
                    </Badge>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card data-testid="card-missing-skills">
            <CardHeader>
              <CardTitle>Missing Skills for {analysis?.roleName}</CardTitle>
              <CardDescription>Skills to develop for this role</CardDescription>
            </CardHeader>
            <CardContent>
              {analysisLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
                </div>
              ) : analysis?.missingSkills?.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {analysis.missingSkills.map((skill: string, idx: number) => (
                    <Badge key={idx} variant="destructive" data-testid={`missing-skill-${idx}`}>
                      {skill}
                    </Badge>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">No missing skills identified. You're ready for this role!</p>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Skill Knowledge Graph Placeholder */}
      {userCv && selectedRole && (
        <Card data-testid="card-knowledge-graph">
          <CardHeader>
            <CardTitle>Skill Knowledge Graph</CardTitle>
            <CardDescription>Visualize how your skills connect to your target career path.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="border-2 border-dashed rounded-lg p-12 text-center" data-testid="graph-placeholder">
              <p className="text-muted-foreground">
                Upload a resume to generate your graph.
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
