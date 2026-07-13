import { index, integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const user = sqliteTable("user", {
  id: text("user").primaryKey(),
  createdAt: integer("created_at").notNull(),
  updatedAt: integer("updated_at").notNull(),
});

export const learnerProfile = sqliteTable("learner_profile", {
  id: text("id").primaryKey(),
  totalPoints: integer("total_points").notNull(),
  currentStreak: integer("current_streak").notNull(),
  longestStreak: integer("longest_streak").notNull(),
  lastActiveOn: text("last_active_on"),
  createdAt: integer("created_at").notNull(),
  updatedAt: integer("updated_at").notNull(),
});

export const courses = sqliteTable(
  "courses",
  {
    id: text("id").primaryKey(),
    slug: text("slug").notNull(),
    title: text("title").notNull(),
    description: text("description").notNull(),
    sourceIndexPath: text("source_index_path").notNull(),
    totalLessons: integer("total_lessons").notNull(),
    totalModules: integer("total_modules").notNull(),
    sortOrder: integer("sort_order").notNull(),
    createdAt: integer("created_at").notNull(),
    updatedAt: integer("updated_at").notNull(),
  },
  (table) => [index("courses_slug_idx").on(table.slug)],
);

export const courseModules = sqliteTable(
  "course_modules",
  {
    id: text("id").primaryKey(),
    courseId: text("course_id")
      .notNull()
      .references(() => courses.id),
    slug: text("slug").notNull(),
    title: text("title").notNull(),
    summary: text("summary"),
    sortOrder: integer("sort_order").notNull(),
    createdAt: integer("created_at").notNull(),
    updatedAt: integer("updated_at").notNull(),
  },
  (table) => [
    index("course_modules_course_idx").on(table.courseId, table.sortOrder),
  ],
);

export const lessons = sqliteTable(
  "lessons",
  {
    id: text("id").primaryKey(),
    courseId: text("course_id")
      .notNull()
      .references(() => courses.id),
    moduleId: text("module_id")
      .notNull()
      .references(() => courseModules.id),
    slug: text("slug").notNull(),
    title: text("title").notNull(),
    sourcePath: text("source_path").notNull(),
    orderIndex: integer("order_index").notNull(),
    estimatedStudyMinutes: integer("estimated_study_minutes"),
    estimatedPracticeMinutes: integer("estimated_practice_minutes"),
    difficultyLabel: text("difficulty_label"),
    prerequisitesJson: text("prerequisites_json").notNull(),
    unlockedConceptsJson: text("unlocked_concepts_json").notNull(),
    markdown: text("markdown").notNull(),
    createdAt: integer("created_at").notNull(),
    updatedAt: integer("updated_at").notNull(),
  },
  (table) => [
    index("lessons_course_idx").on(table.courseId, table.orderIndex),
    index("lessons_module_idx").on(table.moduleId, table.orderIndex),
  ],
);

export const lessonProgress = sqliteTable(
  "lesson_progress",
  {
    lessonId: text("lesson_id")
      .primaryKey()
      .references(() => lessons.id),
    status: text("status").notNull(),
    scrollPercent: integer("scroll_percent").notNull(),
    lastScrollOffset: integer("last_scroll_offset").notNull(),
    startedAt: integer("started_at"),
    completedAt: integer("completed_at"),
    lastOpenedAt: integer("last_opened_at"),
    pointsAwarded: integer("points_awarded").notNull(),
    createdAt: integer("created_at").notNull(),
    updatedAt: integer("updated_at").notNull(),
  },
  (table) => [index("lesson_progress_status_idx").on(table.status)],
);

export const dailyActivity = sqliteTable("daily_activity", {
  activityDate: text("activity_date").primaryKey(),
  pointsEarned: integer("points_earned").notNull(),
  lessonsCompleted: integer("lessons_completed").notNull(),
  createdAt: integer("created_at").notNull(),
  updatedAt: integer("updated_at").notNull(),
});

export const appState = sqliteTable("app_state", {
  key: text("key").primaryKey(),
  value: text("value").notNull(),
  updatedAt: integer("updated_at").notNull(),
});
