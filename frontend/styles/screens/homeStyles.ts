import { StyleSheet } from "react-native";

export const homeStyles = StyleSheet.create({
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
    marginBottom: 325,
  },
  title: {
    fontSize: 30,
    color: "white",
    fontWeight: "bold",
    textAlign: "center",
  },
});
