import { View, Text, Modal, ScrollView, TouchableOpacity } from "react-native";
import { modalStyles } from "../styles/modalStyles";

interface HutSelectionModalProps {
  isVisible: boolean;
  onClose: () => void;
  huts: Array<{ id: number; name: string }>;
  selectedHuts: string[];
  onHutToggle: (hutId: string) => void;
  isLoading: boolean;
}

export const HutSelectionModal = ({
  isVisible,
  onClose,
  huts,
  selectedHuts,
  onHutToggle,
  isLoading,
}: HutSelectionModalProps) => {
  return (
    <Modal transparent={true} visible={isVisible} animationType="slide">
      <View style={modalStyles.modalContainer}>
        <View style={modalStyles.modalContent}>
          <Text style={modalStyles.inputLabel}>Select Huts</Text>
          <Text style={modalStyles.description}>Choose 1 or more</Text>
          <ScrollView style={modalStyles.hutList}>
            {huts.map((hut) => (
              <TouchableOpacity
                key={hut.id}
                style={[
                  modalStyles.hutOption,
                  selectedHuts.includes(hut.id.toString()) &&
                    modalStyles.hutOptionSelected,
                ]}
                onPress={() => onHutToggle(hut.id.toString())}
              >
                <Text style={modalStyles.hutOptionText}>{hut.name}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
          <TouchableOpacity
            style={[
              modalStyles.button,
              isLoading && modalStyles.buttonDisabled,
              { width: "50%", backgroundColor: "green" },
            ]}
            onPress={onClose}
          >
            <Text style={modalStyles.buttonText}>Done</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
};
