import { useEffect, useState } from "react";
import { StyleSheet, View } from "react-native";
import { useRouter } from "expo-router";
import { StatePanel } from "@/components/shared/state-panel";
import { ensureCurriculumSeeded } from "@/db/learning";
import { Block } from "@/shared/ui/organisms/block";
import { colors } from "@/theme/colors";

const wait = (duration: number) => {
  return new Promise((resolve) => {
    setTimeout(resolve, duration);
  });
};

export default function Splash() {
  const router = useRouter();
  const [attempt, setAttempt] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const bootstrap = async () => {
      setLoading(true);
      setError(null);

      try {
        await Promise.all([ensureCurriculumSeeded(), wait(2000)]);
        if (!cancelled) {
          router.replace("/home");
        }
      } catch (bootstrapError) {
        if (!cancelled) {
          setError(
            bootstrapError instanceof Error
              ? bootstrapError.message
              : "Failed to prepare the local curriculum.",
          );
          setLoading(false);
        }
      }
    };

    void bootstrap();

    return () => {
      cancelled = true;
    };
  }, [attempt, router]);

  if (error) {
    return (
      <View style={styles.centered}>
        <StatePanel
          actionLabel="Retry"
          message={error}
          onAction={() => {
            setLoading(true);
            setError(null);
            setAttempt((value) => value + 1);
          }}
          title="GUDU couldn't start"
        />
      </View>
    );
  }

  return (
    <View style={styles.centered}>
      <Block
        background={colors.surface}
        base={colors.primaryMuted}
        borderRadius={16}
        borderWidth={4}
        glow={colors.accent}
        height={72}
        speed={1}
        width={72}
      />
      {loading ? (
        <View style={styles.loadingState}>
          <StatePanel
            message="Loading your local-first engineering journey."
            progress
            title="Preparing lessons"
          />
        </View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  centered: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 16,
    gap: 24,
  },
  loadingState: {
    width: "100%",
  },
});
