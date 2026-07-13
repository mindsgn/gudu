import { Stack } from "expo-router";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { db, DATABASE_NAME } from "@/db/client";
import { SQLiteProvider } from "expo-sqlite";
import { Suspense } from "react";
import { ActivityIndicator, View } from "react-native";
import { useMigrations } from "drizzle-orm/expo-sqlite/migrator";
import migrations from "@/drizzle/migrations";
import { colors } from "@/theme/colors";

export default function RootLayout() {
  const { success: migrationsReady } = useMigrations(db, migrations);

  if (!migrationsReady) {
    return (
      <View
        style={{
          flex: 1,
          justifyContent: "center",
          backgroundColor: colors.background,
        }}
      >
        <ActivityIndicator color={colors.accent} />
      </View>
    );
  }

  return (
    <Suspense
      fallback={
        <View
          style={{
            flex: 1,
            justifyContent: "center",
            backgroundColor: colors.background,
          }}
        >
          <ActivityIndicator color={colors.accent} />
        </View>
      }
    >
      <SQLiteProvider
        databaseName={DATABASE_NAME}
        options={{ enableChangeListener: true }}
        useSuspense
      >
        <GestureHandlerRootView style={{ flex: 1 }}>
          <Stack>
            <Stack.Screen name="index" options={{ headerShown: false }} />
            <Stack.Screen name="home" options={{ headerShown: false }} />
            <Stack.Screen name="course" options={{ headerShown: false }} />
            <Stack.Screen name="backend" options={{ headerShown: false }} />
            <Stack.Screen name="lesson" options={{ headerShown: false }} />
            <Stack.Screen name="complete" options={{ headerShown: false }} />
          </Stack>
        </GestureHandlerRootView>
      </SQLiteProvider>
    </Suspense>
  );
}
