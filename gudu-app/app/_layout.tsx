import { Stack } from "expo-router";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { db, DATABASE_NAME } from "@/db/client";
import { SQLiteProvider } from "expo-sqlite";
import { Suspense } from "react";
import { ActivityIndicator, View } from "react-native";
import { useMigrations } from "drizzle-orm/expo-sqlite/migrator";
import migrations from "@/drizzle/migrations";

export default function RootLayout() {
  const { success: migrationsReady } = useMigrations(db, migrations);

  if (!migrationsReady) {
    return (
      <View style={{ flex: 1 }}>
        <ActivityIndicator />
      </View>
    );
  }

  return (
    <Suspense
      fallback={
        <View style={{ flex: 1 }}>
          <ActivityIndicator />
        </View>
      }
    >
      <SQLiteProvider
        databaseName={DATABASE_NAME}
        options={{ enableChangeListener: true }}
        useSuspense
      >
        <GestureHandlerRootView>
          <Stack>
            <Stack.Screen name="index" options={{ headerShown: false }} />
            <Stack.Screen name="home" options={{ headerShown: false }} />
            <Stack.Screen name="backend" options={{ headerShown: false }} />
            <Stack.Screen name="lesson" options={{ headerShown: false }} />
            <Stack.Screen name="complete" options={{ headerShown: false }} />
          </Stack>
        </GestureHandlerRootView>
      </SQLiteProvider>
    </Suspense>
  );
}
