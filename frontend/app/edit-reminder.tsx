import { Text } from "react-native";
import { useLocalSearchParams } from "expo-router";
import SetReminderScreen from "./set-reminder";

const EditReminderScreen = () => {
  const params = useLocalSearchParams();
  const reminderString = params.reminder as string;

  if (!reminderString) {
    return <Text>Error: Invalid reminder data</Text>;
  }

  const reminder = JSON.parse(reminderString);

  return <SetReminderScreen isEditing={true} reminderToEdit={reminder} />;
};

export default EditReminderScreen;
