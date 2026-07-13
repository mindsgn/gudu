import { StyleSheet, Text, View } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { Button } from "@/components/shared/pressable-card";
import { StatePanel } from "@/components/shared/state-panel";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";

const parseParam = (value: string | string[] | undefined) => {
  return typeof value === "string" ? value : "";
};

export default function CompleteScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{
    courseSlug?: string | string[];
    currentStreak?: string | string[];
    lessonTitle?: string | string[];
    nextLessonId?: string | string[];
    nextLessonTitle?: string | string[];
    pointsEarned?: string | string[];
    totalPoints?: string | string[];
  }>();

  const lessonTitle = parseParam(params.lessonTitle);
  const nextLessonId = parseParam(params.nextLessonId);
  const nextLessonTitle = parseParam(params.nextLessonTitle);
  const totalPoints = Number(parseParam(params.totalPoints) || "0");
  const currentStreak = Number(parseParam(params.currentStreak) || "0");
  const pointsEarned = Number(parseParam(params.pointsEarned) || "0");

  if (!lessonTitle) {
    return (
      <View style={styles.centered}>
        <StatePanel
          actionLabel="Go Home"
          message="The completion summary is missing its lesson context."
          onAction={() => {
            router.replace("/home");
          }}
          title="Nothing to celebrate yet"
        />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.eyebrow}>Lesson complete</Text>
        <Text style={styles.title}>{lessonTitle}</Text>
        <Text style={styles.points}>+{pointsEarned} points</Text>
        <View style={styles.statsRow}>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Total score</Text>
            <Text style={styles.statValue}>{totalPoints}</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Current streak</Text>
            <Text style={styles.statValue}>{currentStreak} days</Text>
          </View>
        </View>
        <View style={styles.nextCard}>
          <Text style={styles.nextLabel}>Unlocked next</Text>
          <Text style={styles.nextValue}>
            {nextLessonTitle || "You have finished the available sequence."}
          </Text>
        </View>
        <Button
          accessibilityLabel="Continue next lesson"
          backgroundColor={colors.accent}
          color={colors.surface}
          label={nextLessonId ? "Continue Next Lesson" : "Return Home"}
          onPress={() => {
            if (nextLessonId) {
              router.replace({
                pathname: "/lesson",
                params: { lessonId: nextLessonId },
              });
              return;
            }

            router.replace("/home");
          }}
          testID="complete-next-button"
          width={280}
        />
        <Button
          accessibilityLabel="Exit to home"
          label="Exit to Home"
          onPress={() => {
            router.replace("/home");
          }}
          testID="complete-home-button"
          width={280}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  centered: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: "center",
    paddingHorizontal: 16,
  },
  container: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: "center",
    paddingHorizontal: 16,
  },
  card: {
    backgroundColor: colors.surface,
    borderRadius: 24,
    padding: 24,
    gap: 16,
  },
  eyebrow: {
    ...typography.caption,
    color: colors.accent,
    textTransform: "uppercase",
  },
  title: {
    ...typography.title,
    color: colors.buttonTextBackground,
  },
  points: {
    ...typography.subtitle,
    color: colors.buttonTextBackground,
  },
  statsRow: {
    flexDirection: "row",
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: colors.primaryMuted,
    borderRadius: 18,
    padding: 16,
    gap: 4,
  },
  statLabel: {
    ...typography.caption,
    color: colors.buttonTextBackground,
  },
  statValue: {
    ...typography.body,
    color: colors.buttonTextBackground,
    fontWeight: "700",
  },
  nextCard: {
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 18,
    padding: 16,
    gap: 6,
  },
  nextLabel: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  nextValue: {
    ...typography.body,
    color: colors.buttonTextBackground,
  },
});
