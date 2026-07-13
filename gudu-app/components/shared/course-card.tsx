import { Pressable, StyleSheet, Text, View } from "react-native";
import { withHaptic } from "@/lib/haptics";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";

type Props = {
  title: string;
  description: string;
  progressLabel: string;
  detailLabel: string;
  nextLessonTitle?: string | null;
  onPress: () => void;
  testID?: string;
};

export const CourseCard = ({
  title,
  description,
  progressLabel,
  detailLabel,
  nextLessonTitle,
  onPress,
  testID,
}: Props) => {
  return (
    <Pressable
      accessibilityLabel={`Open ${title} course`}
      accessibilityRole="button"
      onPress={withHaptic(onPress, "medium")}
      style={styles.card}
      testID={testID}
    >
      <View style={styles.badgeRow}>
        <View style={styles.progressPill}>
          <Text style={styles.progressPillText}>{progressLabel}</Text>
        </View>
        <Text style={styles.detailLabel}>{detailLabel}</Text>
      </View>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>{description}</Text>
      <View style={styles.footer}>
        <Text style={styles.footerLabel}>Next up</Text>
        <Text style={styles.footerValue}>
          {nextLessonTitle ?? "Start from lesson one"}
        </Text>
      </View>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: 24,
    padding: 20,
    gap: 12,
  },
  badgeRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  progressPill: {
    backgroundColor: colors.primaryMuted,
    borderRadius: 999,
    paddingHorizontal: 12,
    paddingVertical: 6,
  },
  progressPillText: {
    ...typography.caption,
    color: colors.buttonTextBackground,
  },
  detailLabel: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  title: {
    ...typography.subtitle,
    color: colors.buttonTextBackground,
  },
  description: {
    ...typography.body,
    color: colors.textSecondary,
    lineHeight: 22,
  },
  footer: {
    borderTopColor: colors.border,
    borderTopWidth: 1,
    paddingTop: 12,
    gap: 4,
  },
  footerLabel: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  footerValue: {
    ...typography.body,
    color: colors.buttonTextBackground,
  },
});
