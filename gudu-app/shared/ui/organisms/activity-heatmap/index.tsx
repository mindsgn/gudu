import { ScrollView, StyleSheet, Text, View } from "react-native";
import { buildActivityHeatmap } from "@/lib/activity-heatmap";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";
import {
  HEATMAP_CELL_SIZE,
  HEATMAP_DAYS,
  HEATMAP_GAP,
  HEATMAP_INTENSITY_COLORS,
} from "./conf";
import type { ActivityHeatmapProps } from "./types";

export const ActivityHeatmap = ({
  activity,
  days = HEATMAP_DAYS,
  testID,
}: ActivityHeatmapProps) => {
  const cells = buildActivityHeatmap(activity, days, new Date());
  const columnCount = cells.reduce(
    (max, cell) => Math.max(max, cell.columnIndex),
    0,
  );
  const columns = Array.from({ length: columnCount + 1 }, (_, columnIndex) =>
    cells.filter((cell) => cell.columnIndex === columnIndex),
  );

  return (
    <View style={styles.wrapper}>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} testID={testID}>
        <View style={styles.columns}>
          {columns.map((column, columnIndex) => (
            <View key={`column-${columnIndex}`} style={styles.column}>
              {column.map((cell) => (
                <View
                  key={cell.activityDate}
                  style={[
                    styles.cell,
                    {
                      backgroundColor: HEATMAP_INTENSITY_COLORS[cell.intensity],
                      borderColor: cell.isToday ? colors.accent : "transparent",
                    },
                  ]}
                  testID={`heatmap-cell-${cell.activityDate}`}
                />
              ))}
            </View>
          ))}
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    gap: 12,
  },
  columns: {
    flexDirection: "row",
    gap: HEATMAP_GAP,
  },
  column: {
    gap: HEATMAP_GAP,
  },
  cell: {
    width: HEATMAP_CELL_SIZE,
    height: HEATMAP_CELL_SIZE,
    borderRadius: 4,
    borderWidth: 1,
  },
  caption: {
    ...typography.caption,
    color: colors.textSecondary,
  },
});
