import {
  View,
  TouchableOpacity,
  Text,
  StyleSheet,
  ImageBackground,
} from "react-native";
import { useRouter } from "expo-router";

export default function HomeScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <ImageBackground
        source={require("../assets/images/cassal-hut2.jpg")}
        style={styles.image}
        resizeMode="cover"
      >
        <View style={styles.overlay}>
          <Text style={styles.title}>Rendezvous Reminder</Text>
        </View>
      </ImageBackground>

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.push("/set-reminder")}
        >
          <Text style={styles.buttonText}>Set Reminder</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.push("/view-reminders")}
        >
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
  image: {
    width: "100%",
    height: "100%",
    justifyContent: "center",
    alignItems: "center",
  },
  overlay: {
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    width: 260,
    height: 260,
    borderRadius: 150,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 400,
  },
  title: {
    fontSize: 30,
    color: "white",
    fontWeight: "bold",
    textAlign: "center",
  },

  // CREATE MASTER STYLES SHEET FOR BUTTON BELOW
  buttonContainer: {
    position: "absolute",
    bottom: 50,
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
    backgroundColor: "rgba(255, 255, 255, 0.7)", // Slightly transparent white for visibility
  },
  buttonText: {
    fontSize: 25,
    color: "black",
  },
});
