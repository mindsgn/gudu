export const LESSON_COMPLETION_POINTS = 10;

export const getLessonCompletionPoints = (alreadyCompleted: boolean): number => {
  return alreadyCompleted ? 0 : LESSON_COMPLETION_POINTS;
};
