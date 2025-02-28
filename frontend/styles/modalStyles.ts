import { StyleSheet } from "react-native";

export const modalStyles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  modalContent: {
    backgroundColor: "white",
    padding: 20,
    borderRadius: 10,
    width: "80%",
    alignItems: "center",
  },
  inputLabel: {
    fontSize: 20,
    fontWeight: "bold",
  },
  description: {
    paddingBottom: 15,
    paddingTop: 10,
    textAlign: "center",
    width: "80%",
  },
  hutList: {
    maxHeight: 400,
    width: "100%",
    borderWidth: 1,
    borderRadius: 10,
    borderColor: "#ccc",
    marginBottom: 10,
  },
  hutOption: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
    backgroundColor: "white",
  },
  hutOptionSelected: {
    backgroundColor: "#e6efff",
  },
  hutOptionText: {
    fontSize: 16,
  },
  button: {
    borderColor: "none",
    borderWidth: 2,
    padding: 15,
    margin: 10,
    borderRadius: 10,
    alignItems: "center",
  },
  buttonText: {
    fontSize: 25,
    color: "white",
  },
  buttonDisabled: {
    opacity: 0.6,
  },
});
