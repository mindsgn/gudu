import { and, asc, desc, eq, inArray } from "drizzle-orm";
import type {
  ContinueTargetRecord,
  DailyActivityEntry,
  LessonProgressSnapshot,
  LessonStatus,
} from "@/@types";
import { curriculumSeed, curriculumVersion } from "@/constants/curriculum";
import { db } from "@/db/client";
import {
  appState,
  courseModules,
  courses,
  dailyActivity,
  learnerProfile,
  lessonProgress,
  lessons,
} from "@/db/schema";
import { selectContinueTarget } from "@/lib/continue-target";
import {
  getDefaultLessonStatus,
  getProgressStatusForUpdate,
  isLessonOpenable,
} from "@/lib/lesson-progress";
import {
  getLessonCompletionPoints,
  LESSON_COMPLETION_POINTS,
} from "@/lib/points";
import { getLocalDateKey, getUpdatedStreak } from "@/lib/streaks";

const LOCAL_PROFILE_ID = "local-learner";
const CURRICULUM_VERSION_KEY = "curriculumVersion";
const CURRICULUM_SEEDED_AT_KEY = "curriculumSeededAt";

type CourseRow = typeof courses.$inferSelect;
type ModuleRow = typeof courseModules.$inferSelect;
type LessonRow = typeof lessons.$inferSelect;
type LessonProgressRow = typeof lessonProgress.$inferSelect;
type LearnerProfileRow = typeof learnerProfile.$inferSelect;
type DailyActivityRow = typeof dailyActivity.$inferSelect;

export type HomeCourseSummary = {
  id: string;
  slug: string;
  title: string;
  description: string;
  totalLessons: number;
  totalModules: number;
  completedLessons: number;
  inProgressLessons: number;
  nextLessonId: string | null;
  nextLessonTitle: string | null;
};

export type HomeDashboardData = {
  profile: LearnerProfileRow;
  activity: DailyActivityEntry[];
  continueTarget: ContinueTargetRecord | null;
  courses: HomeCourseSummary[];
};

export type CourseLessonItem = {
  id: string;
  title: string;
  status: LessonStatus;
  orderIndex: number;
  estimatedStudyMinutes: number | null;
  difficultyLabel: string | null;
};

export type CourseSection = {
  id: string;
  title: string;
  summary: string | null;
  lessons: CourseLessonItem[];
};

export type CourseScreenData = {
  course: CourseRow;
  sections: CourseSection[];
  completedLessons: number;
  continueTarget: ContinueTargetRecord | null;
};

export type LessonScreenData = {
  id: string;
  title: string;
  markdown: string;
  courseId: string;
  courseSlug: string;
  courseTitle: string;
  moduleTitle: string;
  orderIndex: number;
  status: LessonStatus;
  scrollPercent: number;
  lastScrollOffset: number;
  estimatedStudyMinutes: number | null;
  estimatedPracticeMinutes: number | null;
  difficultyLabel: string | null;
};

export type CompletionResult = {
  lessonId: string;
  lessonTitle: string;
  courseSlug: string;
  pointsEarned: number;
  totalPoints: number;
  currentStreak: number;
  nextLessonId: string | null;
  nextLessonTitle: string | null;
};

const serializeStringArray = (values: string[]): string => {
  return JSON.stringify(values);
};

const getAllModuleRows = () => {
  return curriculumSeed.courses.flatMap((course) =>
    course.modules.map((module) => ({
      id: module.id,
      courseId: module.courseId,
      slug: module.slug,
      title: module.title,
      summary: module.summary,
      sortOrder: module.sortOrder,
      createdAt: 0,
      updatedAt: 0,
    })),
  );
};

const getAllLessonRows = () => {
  return curriculumSeed.courses.flatMap((course) =>
    course.modules.flatMap((module) =>
      module.lessons.map((lesson) => ({
        id: lesson.id,
        courseId: lesson.courseId,
        moduleId: lesson.moduleId,
        slug: lesson.slug,
        title: lesson.title,
        sourcePath: lesson.sourcePath,
        orderIndex: lesson.orderIndex,
        estimatedStudyMinutes: lesson.estimatedStudyMinutes,
        estimatedPracticeMinutes: lesson.estimatedPracticeMinutes,
        difficultyLabel: lesson.difficultyLabel,
        prerequisitesJson: serializeStringArray(lesson.prerequisites),
        unlockedConceptsJson: serializeStringArray(lesson.unlockedConcepts),
        markdown: lesson.markdown,
        createdAt: 0,
        updatedAt: 0,
      })),
    ),
  );
};

const getLessonLookup = (lessonRows: LessonRow[]) => {
  return new Map(lessonRows.map((lesson) => [lesson.id, lesson]));
};

const getCourseLookup = (courseRows: CourseRow[]) => {
  return new Map(courseRows.map((course) => [course.id, course]));
};

const getModuleLookup = (moduleRows: ModuleRow[]) => {
  return new Map(moduleRows.map((module) => [module.id, module]));
};

const buildLessonSnapshots = (
  courseRows: CourseRow[],
  moduleRows: ModuleRow[],
  lessonRows: LessonRow[],
  progressRows: LessonProgressRow[],
): LessonProgressSnapshot[] => {
  const courseById = getCourseLookup(courseRows);
  const moduleById = getModuleLookup(moduleRows);
  const progressByLessonId = new Map(
    progressRows.map((progress) => [progress.lessonId, progress]),
  );

  return lessonRows.map((lesson) => {
    const course = courseById.get(lesson.courseId);
    const module = moduleById.get(lesson.moduleId);
    const progress = progressByLessonId.get(lesson.id);

    if (!course || !module || !progress) {
      throw new Error(`Missing curriculum state for lesson ${lesson.id}`);
    }

    return {
      lessonId: lesson.id,
      courseId: course.id,
      courseSlug: course.slug,
      lessonTitle: lesson.title,
      moduleTitle: module.title,
      orderIndex: lesson.orderIndex,
      status: progress.status as LessonStatus,
      lastOpenedAt: progress.lastOpenedAt,
      scrollPercent: progress.scrollPercent,
    };
  });
};

const getOrCreateProfile = (timestamp: number): LearnerProfileRow => {
  const existingProfile = db
    .select()
    .from(learnerProfile)
    .where(eq(learnerProfile.id, LOCAL_PROFILE_ID))
    .get();

  if (existingProfile) {
    return existingProfile;
  }

  const newProfile: LearnerProfileRow = {
    id: LOCAL_PROFILE_ID,
    totalPoints: 0,
    currentStreak: 0,
    longestStreak: 0,
    lastActiveOn: null,
    createdAt: timestamp,
    updatedAt: timestamp,
  };

  db.insert(learnerProfile).values(newProfile).run();
  return newProfile;
};

export const ensureCurriculumSeeded = async (): Promise<void> => {
  const seededVersion = db
    .select()
    .from(appState)
    .where(eq(appState.key, CURRICULUM_VERSION_KEY))
    .get();

  const existingCourseCount = db.select().from(courses).all().length;
  if (seededVersion?.value === curriculumVersion && existingCourseCount > 0) {
    return;
  }

  const timestamp = Date.now();

  db.transaction((tx) => {
    const seededProfile = tx
      .select()
      .from(learnerProfile)
      .where(eq(learnerProfile.id, LOCAL_PROFILE_ID))
      .get();

    if (!seededProfile) {
      tx.insert(learnerProfile)
        .values({
          id: LOCAL_PROFILE_ID,
          totalPoints: 0,
          currentStreak: 0,
          longestStreak: 0,
          lastActiveOn: null,
          createdAt: timestamp,
          updatedAt: timestamp,
        })
        .run();
    }

    for (const course of curriculumSeed.courses) {
      tx.insert(courses)
        .values({
          id: course.id,
          slug: course.slug,
          title: course.title,
          description: course.description,
          sourceIndexPath: course.sourceIndexPath,
          totalLessons: course.totalLessons,
          totalModules: course.totalModules,
          sortOrder: course.sortOrder,
          createdAt: timestamp,
          updatedAt: timestamp,
        })
        .onConflictDoUpdate({
          target: courses.id,
          set: {
            slug: course.slug,
            title: course.title,
            description: course.description,
            sourceIndexPath: course.sourceIndexPath,
            totalLessons: course.totalLessons,
            totalModules: course.totalModules,
            sortOrder: course.sortOrder,
            updatedAt: timestamp,
          },
        })
        .run();
    }

    for (const module of getAllModuleRows()) {
      tx.insert(courseModules)
        .values({
          ...module,
          createdAt: timestamp,
          updatedAt: timestamp,
        })
        .onConflictDoUpdate({
          target: courseModules.id,
          set: {
            courseId: module.courseId,
            slug: module.slug,
            title: module.title,
            summary: module.summary,
            sortOrder: module.sortOrder,
            updatedAt: timestamp,
          },
        })
        .run();
    }

    for (const lesson of getAllLessonRows()) {
      tx.insert(lessons)
        .values({
          ...lesson,
          createdAt: timestamp,
          updatedAt: timestamp,
        })
        .onConflictDoUpdate({
          target: lessons.id,
          set: {
            courseId: lesson.courseId,
            moduleId: lesson.moduleId,
            slug: lesson.slug,
            title: lesson.title,
            sourcePath: lesson.sourcePath,
            orderIndex: lesson.orderIndex,
            estimatedStudyMinutes: lesson.estimatedStudyMinutes,
            estimatedPracticeMinutes: lesson.estimatedPracticeMinutes,
            difficultyLabel: lesson.difficultyLabel,
            prerequisitesJson: lesson.prerequisitesJson,
            unlockedConceptsJson: lesson.unlockedConceptsJson,
            markdown: lesson.markdown,
            updatedAt: timestamp,
          },
        })
        .run();

      tx.insert(lessonProgress)
        .values({
          lessonId: lesson.id,
          status: getDefaultLessonStatus(lesson.orderIndex),
          scrollPercent: 0,
          lastScrollOffset: 0,
          startedAt: null,
          completedAt: null,
          lastOpenedAt: null,
          pointsAwarded: 0,
          createdAt: timestamp,
          updatedAt: timestamp,
        })
        .onConflictDoNothing()
        .run();
    }

    tx.insert(appState)
      .values({
        key: CURRICULUM_VERSION_KEY,
        value: curriculumVersion,
        updatedAt: timestamp,
      })
      .onConflictDoUpdate({
        target: appState.key,
        set: {
          value: curriculumVersion,
          updatedAt: timestamp,
        },
      })
      .run();

    tx.insert(appState)
      .values({
        key: CURRICULUM_SEEDED_AT_KEY,
        value: `${timestamp}`,
        updatedAt: timestamp,
      })
      .onConflictDoUpdate({
        target: appState.key,
        set: {
          value: `${timestamp}`,
          updatedAt: timestamp,
        },
      })
      .run();
  });
};

export const getHomeDashboardData = async (): Promise<HomeDashboardData> => {
  await ensureCurriculumSeeded();

  const profile = getOrCreateProfile(Date.now());
  const courseRows = db.select().from(courses).orderBy(asc(courses.sortOrder)).all();
  const moduleRows = db
    .select()
    .from(courseModules)
    .orderBy(asc(courseModules.sortOrder))
    .all();
  const lessonRows = db.select().from(lessons).orderBy(asc(lessons.orderIndex)).all();
  const progressRows = db.select().from(lessonProgress).all();
  const activityRows = db
    .select()
    .from(dailyActivity)
    .orderBy(desc(dailyActivity.activityDate))
    .all();

  const snapshots = buildLessonSnapshots(
    courseRows,
    moduleRows,
    lessonRows,
    progressRows,
  );
  const continueTarget = selectContinueTarget(snapshots);
  const lessonById = getLessonLookup(lessonRows);

  const courseSummaries = courseRows.map((course) => {
    const courseSnapshots = snapshots.filter(
      (snapshot) => snapshot.courseId === course.id,
    );
    const completedLessons = courseSnapshots.filter(
      (snapshot) => snapshot.status === "completed",
    ).length;
    const inProgressLessons = courseSnapshots.filter(
      (snapshot) => snapshot.status === "in_progress",
    ).length;
    const nextLesson = courseSnapshots.find(
      (snapshot) => snapshot.status === "in_progress" || snapshot.status === "unlocked",
    );
    const nextLessonRow = nextLesson ? lessonById.get(nextLesson.lessonId) : null;

    return {
      id: course.id,
      slug: course.slug,
      title: course.title,
      description: course.description,
      totalLessons: course.totalLessons,
      totalModules: course.totalModules,
      completedLessons,
      inProgressLessons,
      nextLessonId: nextLesson?.lessonId ?? null,
      nextLessonTitle: nextLessonRow?.title ?? nextLesson?.lessonTitle ?? null,
    };
  });

  return {
    profile,
    activity: activityRows.map((entry) => ({
      activityDate: entry.activityDate,
      pointsEarned: entry.pointsEarned,
    })),
    continueTarget,
    courses: courseSummaries,
  };
};

export const getCourseScreenData = async (
  courseSlug: string,
): Promise<CourseScreenData> => {
  await ensureCurriculumSeeded();

  const course = db
    .select()
    .from(courses)
    .where(eq(courses.slug, courseSlug))
    .get();

  if (!course) {
    throw new Error(`Course ${courseSlug} not found`);
  }

  const moduleRows = db
    .select()
    .from(courseModules)
    .where(eq(courseModules.courseId, course.id))
    .orderBy(asc(courseModules.sortOrder))
    .all();
  const lessonRows = db
    .select()
    .from(lessons)
    .where(eq(lessons.courseId, course.id))
    .orderBy(asc(lessons.orderIndex))
    .all();
  const progressRows = db
    .select()
    .from(lessonProgress)
    .where(inArray(lessonProgress.lessonId, lessonRows.map((lesson) => lesson.id)))
    .all();

  const snapshots = buildLessonSnapshots([course], moduleRows, lessonRows, progressRows);
  const progressByLessonId = new Map(
    progressRows.map((progress) => [progress.lessonId, progress]),
  );

  const sections = moduleRows.map((module) => ({
    id: module.id,
    title: module.title,
    summary: module.summary,
    lessons: lessonRows
      .filter((lesson) => lesson.moduleId === module.id)
      .map((lesson) => {
        const progress = progressByLessonId.get(lesson.id);
        if (!progress) {
          throw new Error(`Missing lesson progress for ${lesson.id}`);
        }

        return {
          id: lesson.id,
          title: lesson.title,
          status: progress.status as LessonStatus,
          orderIndex: lesson.orderIndex,
          estimatedStudyMinutes: lesson.estimatedStudyMinutes,
          difficultyLabel: lesson.difficultyLabel,
        };
      }),
  }));

  return {
    course,
    sections,
    completedLessons: snapshots.filter(
      (snapshot) => snapshot.status === "completed",
    ).length,
    continueTarget: selectContinueTarget(snapshots),
  };
};

export const getLessonScreenData = async (
  lessonId: string,
): Promise<LessonScreenData> => {
  await ensureCurriculumSeeded();

  const lesson = db
    .select()
    .from(lessons)
    .where(eq(lessons.id, lessonId))
    .get();
  const progress = db
    .select()
    .from(lessonProgress)
    .where(eq(lessonProgress.lessonId, lessonId))
    .get();

  if (!lesson || !progress) {
    throw new Error(`Lesson ${lessonId} not found`);
  }

  const course = db
    .select()
    .from(courses)
    .where(eq(courses.id, lesson.courseId))
    .get();
  const module = db
    .select()
    .from(courseModules)
    .where(eq(courseModules.id, lesson.moduleId))
    .get();

  if (!course || !module) {
    throw new Error(`Missing course context for lesson ${lessonId}`);
  }

  return {
    id: lesson.id,
    title: lesson.title,
    markdown: lesson.markdown,
    courseId: course.id,
    courseSlug: course.slug,
    courseTitle: course.title,
    moduleTitle: module.title,
    orderIndex: lesson.orderIndex,
    status: progress.status as LessonStatus,
    scrollPercent: progress.scrollPercent,
    lastScrollOffset: progress.lastScrollOffset,
    estimatedStudyMinutes: lesson.estimatedStudyMinutes,
    estimatedPracticeMinutes: lesson.estimatedPracticeMinutes,
    difficultyLabel: lesson.difficultyLabel,
  };
};

export const markLessonOpened = async (lessonId: string): Promise<void> => {
  await ensureCurriculumSeeded();

  const progress = db
    .select()
    .from(lessonProgress)
    .where(eq(lessonProgress.lessonId, lessonId))
    .get();

  if (!progress) {
    return;
  }

  db.update(lessonProgress)
    .set({
      lastOpenedAt: Date.now(),
      updatedAt: Date.now(),
    })
    .where(eq(lessonProgress.lessonId, lessonId))
    .run();
};

export const saveLessonProgress = async (
  lessonId: string,
  scrollPercent: number,
  lastScrollOffset: number,
): Promise<void> => {
  await ensureCurriculumSeeded();

  const progress = db
    .select()
    .from(lessonProgress)
    .where(eq(lessonProgress.lessonId, lessonId))
    .get();

  if (!progress || !isLessonOpenable(progress.status as LessonStatus)) {
    return;
  }

  const timestamp = Date.now();
  const nextStatus = getProgressStatusForUpdate({
    currentStatus: progress.status as LessonStatus,
    nextScrollPercent: scrollPercent,
  });

  db.update(lessonProgress)
    .set({
      status: nextStatus,
      scrollPercent: Math.max(0, Math.min(100, Math.round(scrollPercent))),
      lastScrollOffset: Math.max(0, Math.round(lastScrollOffset)),
      startedAt:
        progress.startedAt ?? (scrollPercent > 0 ? timestamp : progress.startedAt),
      lastOpenedAt: timestamp,
      updatedAt: timestamp,
    })
    .where(eq(lessonProgress.lessonId, lessonId))
    .run();
};

export const completeLesson = async (
  lessonId: string,
): Promise<CompletionResult> => {
  await ensureCurriculumSeeded();

  return db.transaction((tx) => {
    const timestamp = Date.now();
    const activityDate = getLocalDateKey(new Date(timestamp));
    const lesson = tx
      .select()
      .from(lessons)
      .where(eq(lessons.id, lessonId))
      .get();
    const progress = tx
      .select()
      .from(lessonProgress)
      .where(eq(lessonProgress.lessonId, lessonId))
      .get();

    if (!lesson || !progress) {
      throw new Error(`Lesson ${lessonId} not found`);
    }

    const course = tx
      .select()
      .from(courses)
      .where(eq(courses.id, lesson.courseId))
      .get();

    if (!course) {
      throw new Error(`Course ${lesson.courseId} not found`);
    }

    const nextLesson = tx
      .select()
      .from(lessons)
      .where(
        and(
          eq(lessons.courseId, lesson.courseId),
          eq(lessons.orderIndex, lesson.orderIndex + 1),
        ),
      )
      .get();
    const existingProfile = tx
      .select()
      .from(learnerProfile)
      .where(eq(learnerProfile.id, LOCAL_PROFILE_ID))
      .get();
    const profile = existingProfile ?? {
      id: LOCAL_PROFILE_ID,
      totalPoints: 0,
      currentStreak: 0,
      longestStreak: 0,
      lastActiveOn: null,
      createdAt: timestamp,
      updatedAt: timestamp,
    };

    if (!existingProfile) {
      tx.insert(learnerProfile).values(profile).run();
    }
    const activityForDay = tx
      .select()
      .from(dailyActivity)
      .where(eq(dailyActivity.activityDate, activityDate))
      .get();
    const alreadyCompleted = progress.status === "completed";
    const pointsEarned = getLessonCompletionPoints(alreadyCompleted);

    if (!alreadyCompleted) {
      tx.update(lessonProgress)
        .set({
          status: "completed",
          scrollPercent: 100,
          pointsAwarded: LESSON_COMPLETION_POINTS,
          lastScrollOffset: progress.lastScrollOffset,
          startedAt: progress.startedAt ?? timestamp,
          completedAt: timestamp,
          lastOpenedAt: timestamp,
          updatedAt: timestamp,
        })
        .where(eq(lessonProgress.lessonId, lessonId))
        .run();

      if (nextLesson) {
        tx.update(lessonProgress)
          .set({
            status: "unlocked",
            updatedAt: timestamp,
          })
          .where(
            and(
              eq(lessonProgress.lessonId, nextLesson.id),
              eq(lessonProgress.status, "locked"),
            ),
          )
          .run();
      }

      if (activityForDay) {
        tx.update(dailyActivity)
          .set({
            pointsEarned: activityForDay.pointsEarned + LESSON_COMPLETION_POINTS,
            lessonsCompleted: activityForDay.lessonsCompleted + 1,
            updatedAt: timestamp,
          })
          .where(eq(dailyActivity.activityDate, activityDate))
          .run();
      } else {
        tx.insert(dailyActivity)
          .values({
            activityDate,
            pointsEarned: LESSON_COMPLETION_POINTS,
            lessonsCompleted: 1,
            createdAt: timestamp,
            updatedAt: timestamp,
          })
          .run();
      }

      const nextStreak = getUpdatedStreak(
        profile,
        activityDate,
        activityForDay !== undefined,
      );

      tx.update(learnerProfile)
        .set({
          totalPoints: profile.totalPoints + LESSON_COMPLETION_POINTS,
          currentStreak: nextStreak.currentStreak,
          longestStreak: nextStreak.longestStreak,
          lastActiveOn: nextStreak.lastActiveOn,
          updatedAt: timestamp,
        })
        .where(eq(learnerProfile.id, LOCAL_PROFILE_ID))
        .run();
    }

    const refreshedProfile = tx
      .select()
      .from(learnerProfile)
      .where(eq(learnerProfile.id, LOCAL_PROFILE_ID))
      .get();

    if (!refreshedProfile) {
      throw new Error("Learner profile missing after completion");
    }

    return {
      lessonId: lesson.id,
      lessonTitle: lesson.title,
      courseSlug: course.slug,
      pointsEarned,
      totalPoints: refreshedProfile.totalPoints,
      currentStreak: refreshedProfile.currentStreak,
      nextLessonId: nextLesson?.id ?? null,
      nextLessonTitle: nextLesson?.title ?? null,
    };
  });
};
