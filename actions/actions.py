from typing import Any, Dict, List, Text
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import SlotSet

class ActionResetOrderSlots(Action):
    def name(self) -> str:
        return "action_reset_order_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [
            SlotSet("clothing_type", None),
            SlotSet("materials", None),
            SlotSet("quantity", None),
        ]


class ActionAskClothingType(Action):
    def name(self) -> str:
        return "action_ask_clothing_type"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Apa pakaian yang anda butuhkan?")  # Asking clothing type
        return []

class ActionAskMaterial(Action):
    def name(self) -> str:
        return "action_ask_material"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Apa jenis bahan yang anda butuhkan?")  # Asking for materials
        return []

class ActionAskQuantity(Action):
    def name(self) -> str:
        return "action_ask_quantity"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Berapa banyak yang ingin anda pesan?")  # Asking for quantity
        return []

class ActionSummary(Action):
    def name(self) -> str:
        return "action_summary"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        clothing_type = tracker.get_slot('clothing_type')
        material = tracker.get_slot('materials')
        quantity = tracker.get_slot('quantity')

        # Ensure that all necessary slots are filled
        if clothing_type and material and quantity:
            summary = f"Anda telah memesan {quantity} {clothing_type} dengan bahan {material}."
            dispatcher.utter_message(text=summary)
        else:
            dispatcher.utter_message(text="Ada informasi yang kurang dalam pesanan Anda. Silakan ulangi.")
        
        return []
