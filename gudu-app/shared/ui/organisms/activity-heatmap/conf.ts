import { colors } from "@/theme/colors";

export const HEATMAP_DAYS = 98;
export const HEATMAP_CELL_SIZE = 12;
export const HEATMAP_GAP = 4;
export const HEATMAP_INTENSITY_COLORS = {
  0: colors.surface,
  1: colors.primaryMuted,
  2: colors.primary,
  3: colors.accent,
  4: colors.buttonTextBackground,
} as const;
