import { StyleSheet } from "react-native";

export const buttonStyles = StyleSheet.create({
  container: {
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
  },
  primaryButton: {
    backgroundColor: "rgba(255, 255, 255, 0.7)",
  },
  buttonText: {
    fontSize: 25,
    color: "black",
  },
});
