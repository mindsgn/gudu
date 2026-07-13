import { useCallback, useState } from "react";
import { Dimensions, StyleSheet, Text, View } from "react-native";
import { useFocusEffect, useRouter } from "expo-router";
import { FlashList } from "@shopify/flash-list";
import { Button } from "@/components/shared/pressable-card";
import { CourseCard } from "@/components/shared/course-card";
import { StatePanel } from "@/components/shared/state-panel";
import {
  getHomeDashboardData,
  type HomeCourseSummary,
  type HomeDashboardData,
} from "@/db/learning";
import { AnimatedHeaderScrollView } from "@/shared/ui/organisms/animated-header-scrollview";
import { ActivityHeatmap } from "@/shared/ui/organisms/activity-heatmap";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";

const ctaWidth = Dimensions.get("window").width - 32;

type ScreenState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "empty" }
  | { status: "ready"; data: HomeDashboardData };

const getProgressLabel = (course: HomeCourseSummary) => {
  return `${course.completedLessons}/${course.totalLessons} complete`;
};

const getDetailLabel = (course: HomeCourseSummary) => {
  return `${course.totalModules} modules`;
};

export default function Home() {
  const router = useRouter();
  const [state, setState] = useState<ScreenState>({ status: "loading" });

  const loadDashboard = useCallback(async () => {
    setState({ status: "loading" });

    try {
      const data = await getHomeDashboardData();

      if (!data.courses.length) {
        setState({ status: "empty" });
        return;
      }

      setState({ status: "ready", data });
    } catch (dashboardError) {
      setState({
        status: "error",
        message:
          dashboardError instanceof Error
            ? dashboardError.message
            : "Failed to load the local dashboard.",
      });
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      void loadDashboard();
    }, [loadDashboard]),
  );

  if (state.status === "loading") {
    return (
      <View style={styles.centered}>
        <StatePanel
          message="Loading your score, streaks, and unlocked lessons."
          progress
          title="Building your dashboard"
        />
      </View>
    );
  }

  if (state.status === "error") {
    return (
      <View style={styles.centered}>
        <StatePanel
          actionLabel="Retry"
          message={state.message}
          onAction={() => {
            void loadDashboard();
          }}
          title="Dashboard unavailable"
        />
      </View>
    );
  }

  if (state.status === "empty") {
    return (
      <View style={styles.centered}>
        <StatePanel
          actionLabel="Reload"
          message="No local courses were found after bootstrapping."
          onAction={() => {
            void loadDashboard();
          }}
          title="No courses yet"
        />
      </View>
    );
  }

  const { data } = state;

  return (
    <AnimatedHeaderScrollView
      largeTitle="GUDU"
      subtitle="Learning Engineering from first principals"
    >
      <View style={styles.heroCard}>
        <Text style={styles.heroValue}>{data.profile.totalPoints}</Text>
        <Text style={styles.heroLabel}>POINTS</Text>
        {
          /*
          <View style={styles.streakRow}>
            <View style={styles.streakCard}>
              <Text style={styles.streakLabel}>Current streak</Text>
              <Text style={styles.streakValue}>{data.profile.currentStreak} days</Text>
            </View>
            <View style={styles.streakCard}>
              <Text style={styles.streakLabel}>Best streak</Text>
              <Text style={styles.streakValue}>{data.profile.longestStreak} days</Text>
            </View>
          </View>
          */
        }

      </View>

      {data && data.continueTarget && data.continueTarget.reason === "resume" ? (
        <Button
          accessibilityLabel="Continue learning"
          backgroundColor={colors.accent}
          color={colors.surface}
          label={`Continue`
          }
          onPress={() => {
            router.push({
              pathname: "/lesson",
              params: { lessonId: data.continueTarget?.lessonId },
            });
          }}
          testID="home-continue-button"
          width={ctaWidth}
        />
      ) : null}

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Activity</Text>
        <ActivityHeatmap activity={data.activity} testID="activity-heatmap" />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Courses</Text>
        <FlashList
          data={data.courses}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <View style={styles.courseCardWrap}>
              <CourseCard
                description={item.description}
                detailLabel={getDetailLabel(item)}
                nextLessonTitle={item.nextLessonTitle}
                onPress={() => {
                  router.push({
                    pathname: "/course",
                    params: { courseSlug: item.slug },
                  });
                }}
                progressLabel={getProgressLabel(item)}
                testID={`course-card-${item.slug}`}
                title={item.title}
              />
            </View>
          )}
          scrollEnabled={false}
        />
      </View>
    </AnimatedHeaderScrollView>
  );
}

const styles = StyleSheet.create({
  centered: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: "center",
    paddingHorizontal: 16,
  },
  heroCard: {
    borderRadius: 24,
    padding: 24,
    gap: 16,
  },
  heroLabel: {
    ...typography.caption,
    color: colors.textSecondary,
    textTransform: "uppercase",
    alignSelf: "center",
  },
  heroValue: {
    ...typography.balance,
    color: colors.buttonTextBackground,
    fontSize: 100,
    alignSelf: "center",
  },
  streakRow: {
    flexDirection: "row",
    gap: 12,
  },
  streakCard: {
    flex: 1,
    backgroundColor: colors.primaryMuted,
    borderRadius: 18,
    padding: 16,
    gap: 6,
  },
  streakLabel: {
    ...typography.caption,
    color: colors.buttonTextBackground,
  },
  streakValue: {
    ...typography.body,
    color: colors.buttonTextBackground,
    fontWeight: "700",
  },
  section: {
    marginTop: 24,
    gap: 16,
  },
  sectionTitle: {
    ...typography.subtitle,
    color: colors.buttonTextBackground,
  },
  courseCardWrap: {
    marginBottom: 12,
  },
});
