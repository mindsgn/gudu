import type { ContinueTargetRecord, LessonProgressSnapshot } from "@/@types";

const sortByLessonOrder = (a: LessonProgressSnapshot, b: LessonProgressSnapshot) => {
  if (a.courseSlug !== b.courseSlug) {
    return a.courseSlug.localeCompare(b.courseSlug);
  }

  return a.orderIndex - b.orderIndex;
};

export const selectContinueTarget = (
  lessons: LessonProgressSnapshot[],
): ContinueTargetRecord | null => {
  const inProgressLessons = lessons
    .filter((lesson) => lesson.status === "in_progress")
    .sort((left, right) => (right.lastOpenedAt ?? 0) - (left.lastOpenedAt ?? 0));

  const resumeLesson = inProgressLessons[0];
  if (resumeLesson) {
    return {
      courseId: resumeLesson.courseId,
      courseSlug: resumeLesson.courseSlug,
      lessonId: resumeLesson.lessonId,
      lessonTitle: resumeLesson.lessonTitle,
      moduleTitle: resumeLesson.moduleTitle,
      orderIndex: resumeLesson.orderIndex,
      lastOpenedAt: resumeLesson.lastOpenedAt,
      reason: "resume",
    };
  }

  const nextUnlockedLesson = lessons
    .filter((lesson) => lesson.status === "unlocked")
    .sort(sortByLessonOrder)[0];

  if (nextUnlockedLesson) {
    return {
      courseId: nextUnlockedLesson.courseId,
      courseSlug: nextUnlockedLesson.courseSlug,
      lessonId: nextUnlockedLesson.lessonId,
      lessonTitle: nextUnlockedLesson.lessonTitle,
      moduleTitle: nextUnlockedLesson.moduleTitle,
      orderIndex: nextUnlockedLesson.orderIndex,
      lastOpenedAt: nextUnlockedLesson.lastOpenedAt,
      reason: "next_unlocked",
    };
  }

  const firstAccessibleLesson = lessons
    .filter((lesson) => lesson.status === "completed")
    .sort(sortByLessonOrder)[0];

  if (!firstAccessibleLesson) {
    return null;
  }

  return {
    courseId: firstAccessibleLesson.courseId,
    courseSlug: firstAccessibleLesson.courseSlug,
    lessonId: firstAccessibleLesson.lessonId,
    lessonTitle: firstAccessibleLesson.lessonTitle,
    moduleTitle: firstAccessibleLesson.moduleTitle,
    orderIndex: firstAccessibleLesson.orderIndex,
    lastOpenedAt: firstAccessibleLesson.lastOpenedAt,
    reason: "course_start",
  };
};
