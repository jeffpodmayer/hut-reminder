import {
  View,
  TouchableOpacity,
  Text,
  StyleSheet,
  ImageBackground,
} from "react-native";

export default function HomeScreen() {
  return (
    <ImageBackground
      source={require("../assets/images/cassal-hut.jpg")}
      style={styles.image}
      resizeMode="cover"
    >
      {/* Title Overlay */}
      <View style={styles.overlay}>
        <Text style={styles.title}>Rendezvous Reminder</Text>
      </View>

      {/* Buttons at the bottom */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Set Reminder</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>View My Reminders</Text>
        </TouchableOpacity>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  image: {
    flex: 1, // Full-screen background
    width: "100%",
    justifyContent: "center", // Centers the overlay vertically
    alignItems: "center",
  },
  overlay: {
    backgroundColor: "rgba(0, 0, 0, 0.5)", // Dark overlay for contrast
    width: 260, // Circle diameter
    height: 260, // Same as width to make it a circle
    borderRadius: 150, // Half of width/height to make it round
    justifyContent: "center", // Centers text vertically
    alignItems: "center", // Centers text horizontally
    marginBottom: 400,
  },
  title: {
    fontSize: 30,
    color: "white",
    fontWeight: "bold",
    textAlign: "center",
  },
  buttonContainer: {
    position: "absolute",
    bottom: 50, // Keeps buttons above the bottom edge
    width: "100%",
    alignItems: "center",
  },
  button: {
    borderColor: "none",
    borderWidth: 2,
    padding: 15,
    margin: 10,
    borderRadius: 10,
    width: "90%",
    alignItems: "center",
    backgroundColor: "rgba(255, 255, 255, 0.8)", // Slightly transparent white for visibility
  },
  buttonText: {
    fontSize: 25,
    fontWeight: "bold",
    color: "black",
  },
});
