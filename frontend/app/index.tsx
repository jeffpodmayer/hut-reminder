import { View, TouchableOpacity, Text, StyleSheet, Button } from "react-native";

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.button}>
        <Text>Set Reminder</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.button}>
        <Text>View My Reminders</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  button: {},
});
