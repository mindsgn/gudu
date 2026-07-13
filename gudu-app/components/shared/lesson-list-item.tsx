import { Pressable, StyleSheet, Text, View } from "react-native";
import type { LessonStatus } from "@/@types";
import { withHaptic } from "@/lib/haptics";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";

type Props = {
  title: string;
  orderIndex: number;
  status: LessonStatus;
  estimatedStudyMinutes: number | null;
  difficultyLabel: string | null;
  onPress?: () => void;
  testID?: string;
};

const statusCopy: Record<LessonStatus, string> = {
  locked: "Locked",
  unlocked: "Ready",
  in_progress: "Resume",
  completed: "Done",
};

const statusColor: Record<LessonStatus, string> = {
  locked: colors.textSecondary,
  unlocked: colors.primaryMuted,
  in_progress: colors.accent,
  completed: colors.buttonTextBackground,
};

export const LessonListItem = ({
  title,
  orderIndex,
  status,
  estimatedStudyMinutes,
  difficultyLabel,
  onPress,
  testID,
}: Props) => {
  const isLocked = status === "locked";
  const meta = [estimatedStudyMinutes ? `${estimatedStudyMinutes} min` : null, difficultyLabel]
    .filter(Boolean)
    .join(" • ");

  return (
    <Pressable
      accessibilityLabel={`${title} lesson`}
      accessibilityRole="button"
      accessibilityState={{ disabled: isLocked }}
      disabled={isLocked}
      onPress={onPress ? withHaptic(onPress, "light") : undefined}
      style={[styles.card, isLocked ? styles.lockedCard : undefined]}
      testID={testID}
    >
      <View style={styles.orderBadge}>
        <Text style={styles.orderText}>{orderIndex}</Text>
      </View>
      <View style={styles.content}>
        <Text style={styles.title}>{title}</Text>
        {meta ? <Text style={styles.meta}>{meta}</Text> : null}
      </View>
      <View style={[styles.statusPill, { backgroundColor: statusColor[status] }]}>
        <Text
          style={[
            styles.statusText,
            { color: status === "completed" ? colors.surface : colors.buttonTextBackground },
          ]}
        >
          {statusCopy[status]}
        </Text>
      </View>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: 20,
    padding: 16,
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  lockedCard: {
    opacity: 0.55,
  },
  orderBadge: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.primaryMuted,
    alignItems: "center",
    justifyContent: "center",
  },
  orderText: {
    ...typography.body,
    color: colors.buttonTextBackground,
    fontWeight: "700",
  },
  content: {
    flex: 1,
    gap: 4,
  },
  title: {
    ...typography.body,
    color: colors.buttonTextBackground,
    fontWeight: "700",
  },
  meta: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  statusPill: {
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 6,
  },
  statusText: {
    ...typography.caption,
    fontWeight: "700",
  },
});
