export type LessonStatus = "locked" | "unlocked" | "in_progress" | "completed";

export type ContinueReason = "resume" | "next_unlocked" | "course_start";

export type CurriculumSeed = {
  version: string;
  generatedAt: string;
  courses: CurriculumCourseSeed[];
};

export type CurriculumCourseSeed = {
  id: string;
  slug: string;
  title: string;
  description: string;
  sourceIndexPath: string;
  totalLessons: number;
  totalModules: number;
  sortOrder: number;
  modules: CurriculumModuleSeed[];
};

export type CurriculumModuleSeed = {
  id: string;
  courseId: string;
  slug: string;
  title: string;
  summary: string | null;
  sortOrder: number;
  lessons: CurriculumLessonSeed[];
};

export type CurriculumLessonSeed = {
  id: string;
  courseId: string;
  moduleId: string;
  slug: string;
  title: string;
  sourcePath: string;
  orderIndex: number;
  estimatedStudyMinutes: number | null;
  estimatedPracticeMinutes: number | null;
  difficultyLabel: string | null;
  prerequisites: string[];
  unlockedConcepts: string[];
  markdown: string;
};

export type ContinueTargetRecord = {
  courseId: string;
  courseSlug: string;
  lessonId: string;
  lessonTitle: string;
  moduleTitle: string;
  orderIndex: number;
  lastOpenedAt: number | null;
  reason: ContinueReason;
};

export type LessonProgressSnapshot = {
  lessonId: string;
  courseId: string;
  courseSlug: string;
  lessonTitle: string;
  moduleTitle: string;
  orderIndex: number;
  status: LessonStatus;
  lastOpenedAt: number | null;
  scrollPercent: number;
};

export type DailyActivityEntry = {
  activityDate: string;
  pointsEarned: number;
};

export type ActivityHeatmapCell = {
  activityDate: string;
  pointsEarned: number;
  intensity: 0 | 1 | 2 | 3 | 4;
  rowIndex: number;
  columnIndex: number;
  isToday: boolean;
};
