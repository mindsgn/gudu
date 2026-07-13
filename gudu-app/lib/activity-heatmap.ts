import type { ActivityHeatmapCell, DailyActivityEntry } from "@/@types";
import { getLocalDateKey } from "@/lib/streaks";

export const getHeatmapIntensity = (
  pointsEarned: number,
  maxPoints: number,
): 0 | 1 | 2 | 3 | 4 => {
  if (pointsEarned <= 0 || maxPoints <= 0) {
    return 0;
  }

  const ratio = pointsEarned / maxPoints;

  if (ratio >= 0.9) {
    return 4;
  }

  if (ratio >= 0.6) {
    return 3;
  }

  if (ratio >= 0.3) {
    return 2;
  }

  return 1;
};

export const buildActivityHeatmap = (
  activity: DailyActivityEntry[],
  days: number,
  today: Date,
): ActivityHeatmapCell[] => {
  const activityByDate = new Map(
    activity.map((entry) => [entry.activityDate, entry.pointsEarned]),
  );
  const todayKey = getLocalDateKey(today);
  const maxPoints = Math.max(
    0,
    ...activity.map((entry) => entry.pointsEarned),
  );
  const cells: ActivityHeatmapCell[] = [];

  for (let offset = days - 1; offset >= 0; offset -= 1) {
    const date = new Date(today);
    date.setDate(today.getDate() - offset);
    const activityDate = getLocalDateKey(date);
    const pointsEarned = activityByDate.get(activityDate) ?? 0;
    const absoluteIndex = days - 1 - offset;

    cells.push({
      activityDate,
      pointsEarned,
      intensity: getHeatmapIntensity(pointsEarned, maxPoints),
      rowIndex: absoluteIndex % 7,
      columnIndex: Math.floor(absoluteIndex / 7),
      isToday: activityDate === todayKey,
    });
  }

  return cells;
};
