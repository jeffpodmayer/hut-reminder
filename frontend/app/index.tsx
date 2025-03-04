import { View, TouchableOpacity, Text, ImageBackground } from "react-native";
import { useRouter } from "expo-router";
import { homeStyles } from "../styles/screens/homeStyles";
import { buttonStyles } from "../styles/components/buttonStyles";

export default function HomeScreen() {
  const router = useRouter();

  return (
    <View style={homeStyles.container}>
      <ImageBackground
        source={require("../assets/images/cassal-hut2.jpg")}
        style={homeStyles.image}
        resizeMode="cover"
      >
        <View style={homeStyles.overlay}>
          <Text style={homeStyles.title}>Rendezvous Reminder</Text>
        </View>
      </ImageBackground>

      <View style={buttonStyles.container}>
        <TouchableOpacity
          style={[buttonStyles.button, buttonStyles.primaryButton]}
          onPress={() => router.push("/set-reminder")}
        >
          <Text style={buttonStyles.buttonText}>Set Reminder</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[buttonStyles.button, buttonStyles.primaryButton]}
          onPress={() => router.push("/view-reminders")}
        >
          <Text style={buttonStyles.buttonText}>View My Reminders</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
