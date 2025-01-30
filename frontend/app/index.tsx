import { View, TouchableOpacity, Text, StyleSheet, Button } from "react-native";

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to the Rendezvous Reminder!</Text>
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Set Reminder</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>View My Reminders</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 35,
    alignItems: "center",
    justifyContent: "center",
    margin: 10,
  },
  buttonContainer: {
    position: "absolute",
    bottom: 30, // Adjust as needed
    width: "100%",
    alignItems: "center",
  },
  button: {
    borderColor: "purple",
    borderWidth: 2, // Added border width to make the border visible
    padding: 15, // Increased padding for better spacing
    margin: 10,
    borderRadius: 10,
    width: "90%", // Adjusted width for a better look
    alignItems: "center", // Ensures text is centered
    justifyContent: "center", // Centers content vertically
  },
  buttonText: {
    fontSize: 25, // Increase font size
    fontWeight: "bold", // Optional: Makes the text bolder
    color: "black", // Optional: Set text color
  },
});
