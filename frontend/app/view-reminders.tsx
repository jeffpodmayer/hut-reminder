import {
  View,
  Text,
  TextInput,
  ScrollView,
  TouchableOpacity,
  Alert,
} from "react-native";
import { useState } from "react";
import dayjs from "dayjs";
import { AntDesign } from "@expo/vector-icons";
import { viewRemindersStyles } from "../styles/screens/viewReminders";
import { router } from "expo-router";

type Reminder = {
  id: string;
  user_email: string;
  start_date: string;
  end_date: string;
  hut_name: string;
};

const ViewRemindersScreen = () => {
  const [email, setEmail] = useState("");
  const [userReminders, setUserReminders] = useState<Reminder[]>([]);

  const formatDateRange = (startDate: string, endDate: string) => {
    const start = dayjs(startDate).format("MMM. D, YYYY");
    const end = dayjs(endDate).format("MMM. D, YYYY");
    return `${start} - ${end}`;
  };

  const handleSearch = async () => {
    if (!email.trim()) {
      setUserReminders([]);
      return;
    }
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/get-reminders/${encodeURIComponent(email)}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch reminders");
      }

      const data = await response.json();
      setUserReminders(data);
    } catch (error) {
      console.error("Error fetching reminders:", error);
      Alert.alert("Error", "Failed to fetch reminders");
      setUserReminders([]);
    }
  };

  const deleteReminder = async (reminderId: string) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/delete-reminder/${reminderId}`,
        { method: "DELETE" }
      );

      if (!response.ok) throw new Error("Failed to delete reminder");

      setUserReminders((current) =>
        current.filter((reminder) => reminder.id !== reminderId)
      );
    } catch (error) {
      console.error("Error deleting reminder:", error);
      Alert.alert("Error", "Failed to delete reminder");
    }
  };

  const handleDelete = (reminderId: string) => {
    Alert.alert(
      "Delete Reminder",
      "Are you sure you want to delete this reminder?",
      [
        { text: "Cancel" },
        {
          text: "Delete",
          style: "destructive",
          onPress: () => {
            void deleteReminder(reminderId);
          },
        },
      ]
    );
  };

  const handleEdit = (reminder: Reminder) => {
    router.push({
      pathname: "/edit-reminder",
      params: { reminder: JSON.stringify(reminder) },
    });
  };

  return (
    <View style={viewRemindersStyles.container}>
      <Text style={viewRemindersStyles.title}>Enter Email</Text>
      <View style={viewRemindersStyles.searchContainer}>
        <TextInput
          style={viewRemindersStyles.input}
          placeholder="Enter your email"
          placeholderTextColor="#666"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          clearButtonMode="while-editing"
        />
        <TouchableOpacity
          style={viewRemindersStyles.searchButton}
          onPress={handleSearch}
        >
          <Text style={viewRemindersStyles.buttonText}>Search</Text>
        </TouchableOpacity>
      </View>
      <Text style={viewRemindersStyles.title}>Your Reminders</Text>
      <ScrollView style={viewRemindersStyles.remindersList}>
        {userReminders.map((reminder) => (
          <View key={reminder.id} style={viewRemindersStyles.reminderCard}>
            <View>
              <Text style={viewRemindersStyles.hutName}>
                {reminder.hut_name}
              </Text>
              <Text style={viewRemindersStyles.dateRange}>
                {formatDateRange(reminder.start_date, reminder.end_date)}
              </Text>
            </View>
            <View style={viewRemindersStyles.cardActions}>
              <TouchableOpacity
                style={viewRemindersStyles.actionButton}
                onPress={() => handleEdit(reminder)}
              >
                <AntDesign name="edit" size={28} color="#0047FF" />
              </TouchableOpacity>
              <TouchableOpacity
                style={viewRemindersStyles.actionButton}
                onPress={() => handleDelete(reminder.id)}
              >
                <AntDesign name="delete" size={28} color="#FF0000" />
              </TouchableOpacity>
            </View>
          </View>
        ))}
        {userReminders.length === 0 && email !== "" && (
          <Text style={viewRemindersStyles.noReminders}>
            No reminders found for this email!
          </Text>
        )}
      </ScrollView>
    </View>
  );
};

export default ViewRemindersScreen;
