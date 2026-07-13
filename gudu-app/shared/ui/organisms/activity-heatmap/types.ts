import type { DailyActivityEntry } from "@/@types";

export type ActivityHeatmapProps = {
  activity: DailyActivityEntry[];
  days?: number;
  testID?: string;
};
