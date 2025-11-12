import yaml
from typing import Dict, List
from Characters.Character import BaseCharacter
from Abilities.AbilityGenerator import AbilityGenerator
from Abilities.Ability import Ability


class CharacterGenerator:
    """Генератор персонажей из YAML файла"""
    
    @staticmethod
    def load_characters(file_path: str, abilities_dict: Dict[str, Ability] = None) -> Dict[str, BaseCharacter]:
        """
        Загружает персонажей из YAML файла
        
        Args:
            file_path (str): Путь к YAML файлу с персонажами
            abilities_dict (Dict[str, Ability]): Словарь способностей для добавления персонажам
            
        Returns:
            Dict[str, BaseCharacter]: Словарь персонажей
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            characters_data = yaml.safe_load(file) or {}
        
        characters = {}
        
        for char_id, char_data in characters_data.items():
            character = CharacterGenerator._create_character(char_id, char_data)
            
            # Добавляем способности если они есть
            if abilities_dict and 'abilities' in char_data:
                for ability_name in char_data['abilities']:
                    if ability_name in abilities_dict:
                        character.add_ability(abilities_dict[ability_name])
            
            characters[char_id] = character
        
        return characters

    @staticmethod
    def _create_character(char_id: str, char_data: dict) -> BaseCharacter:
        """Создает персонажа из данных"""
        # Создаем конкретного персонажа
        character = BaseCharacter(
            name=char_data.get('name', char_id),
            max_health=char_data.get('max_health', 100),
            armor=char_data.get('armor', 0.1),
            picture=char_data.get('picture', '')
        )
        
        return character


