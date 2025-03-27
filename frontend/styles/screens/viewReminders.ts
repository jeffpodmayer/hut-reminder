import { StyleSheet } from "react-native";

export const viewRemindersStyles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#fff",
  },
  title: {
    fontSize: 25,
    fontWeight: "bold",
    marginBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
    paddingBottom: 10,
  },
  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 20,
  },
  input: {
    flex: 1,
    height: 40,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 5,
    padding: 10,
    marginRight: 10,
  },
  searchButton: {
    backgroundColor: "#0047FF",
    padding: 10,
    borderRadius: 5,
    width: 80,
    alignItems: "center",
  },
  buttonText: {
    color: "white",
    fontWeight: "bold",
  },
  remindersList: {
    flex: 1,
  },
  reminderCard: {
    backgroundColor: "#f5f5f5",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: "#eee",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  hutName: {
    fontSize: 14,
    color: "#666",
    marginBottom: 5,
  },
  dateRange: {
    fontSize: 18,
    fontWeight: "bold",
    flexShrink: 1,
    flexWrap: "nowrap",
  },
  noReminders: {
    textAlign: "center",
    color: "#666",
    marginTop: 20,
  },
  cardActions: {
    flexDirection: "row",
    alignItems: "center",
  },
  actionButton: {
    padding: 5,
    marginLeft: 15,
  },
  hutList: {
    marginTop: 5,
  },
  reminderContent: {
    flex: 1,
  },
});
