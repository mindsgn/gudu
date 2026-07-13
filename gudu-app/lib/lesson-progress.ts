import type { LessonStatus } from "@/@types";

type StatusArgs = {
  currentStatus: LessonStatus;
  nextScrollPercent: number;
};

export const clampScrollPercent = (value: number): number => {
  if (Number.isNaN(value)) {
    return 0;
  }

  return Math.max(0, Math.min(100, Math.round(value)));
};

export const getProgressStatusForUpdate = ({
  currentStatus,
  nextScrollPercent,
}: StatusArgs): LessonStatus => {
  const clampedPercent = clampScrollPercent(nextScrollPercent);

  if (currentStatus === "completed") {
    return "completed";
  }

  if (currentStatus === "locked") {
    return "locked";
  }

  if (clampedPercent <= 0) {
    return "unlocked";
  }

  if (clampedPercent >= 100) {
    return "completed";
  }

  return "in_progress";
};

export const getDefaultLessonStatus = (orderIndex: number): LessonStatus => {
  return orderIndex === 1 ? "unlocked" : "locked";
};

export const isLessonOpenable = (status: LessonStatus): boolean => {
  return status !== "locked";
};
