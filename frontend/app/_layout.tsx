import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: "black",
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
      <Stack.Screen name="edit-reminder" options={{ title: "Edit Reminder" }} />
    </Stack>
  );
}
