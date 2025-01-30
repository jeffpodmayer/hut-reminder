import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: "transparent",
        },
        headerTintColor: "#fff",
      }}
    >
      <Stack.Screen
        name="index"
        options={{ title: "", headerTransparent: true }}
      />
      <Stack.Screen name="set-reminder" options={{ title: "Set Reminder" }} />
      <Stack.Screen
        name="view-reminders"
        options={{ title: "View Your Reminders" }}
      />
    </Stack>
  );
}
