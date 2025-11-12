from abc import ABC, abstractmethod
from typing import List

class BaseCharacter(ABC):
    def __init__(self, name: str, max_health: float, armor: float, picture: str):
        self.name = name
        self.picture = picture

        self.current_health = max_health
        self.max_health = max_health

        self.current_magic_resistance = 0.1
        self.base_magic_resistance = 0.1

        self.current_armor = armor
        self.base_armor = armor

        self.abilities = []
        self.effects = []

        self.current_magic_amplify = 1
        self.base_magic_amplify = 1

        self.current_attack_amplify = 1
        self.base_attack_amplify = 1

        self.stunned = False

    def take_magic_damage(self, damage: float, amplify=1) -> str:
        actual_damage = max(1.0, damage * (1 - self.current_magic_resistance) * amplify)
        self.current_health = max(0.0, self.current_health - actual_damage)
        print(actual_damage)
        return f'📜{actual_damage}'

    def take_physical_damage(self, damage: float, amplify=1) -> str:
        actual_damage = max(1.0, damage * (1 - self.current_armor) * amplify)
        self.current_health = max(0.0, self.current_health - actual_damage)
        return f'🗡️{actual_damage}'
    
    def heal(self, hp_points) -> str:
        self.current_health = min(self.max_health, self.current_health + hp_points)
        return f'❤️‍🩹 {hp_points}'

    def add_ability(self, ability):
        self.abilities.append(ability)

    def update_abilities(self):
        for ability in self.abilities:
            ability.update_cooldown()

    def add_effect(self, effect):
        print(f'{effect}------------------------')
        self.effects.append(effect)
        return effect.info()

    def remove_effect(self, effect):
        if effect in self.effects:
            self.effects.remove(effect)

    def update_effects(self):
        """Обновляет эффекты, разделяя их по типу применения"""
        effects_to_remove = []
    
        # Сначала применяем эффекты конца хода (дот-эффекты)
        for effect in self.effects:
            if effect.apply_on_turn_end:
                effect.apply_effect(self)
    
        # Затем обновляем длительности всех эффектов
        for effect in self.effects:
            effect.duration -= 1
            if effect.duration <= 0:
                effects_to_remove.append(effect)
    
        # Удаляем завершившиеся эффекты и вызываем on_remove
        for effect in effects_to_remove:
            effect.on_remove(self)
            self.effects.remove(effect)

    def is_alive(self) -> bool:
        return self.current_health > 0

    def info(self) -> str:
        """Возвращает полную информацию о персонаже"""
        info_lines = []
        
        # Основная информация
        info_lines.append(f"{self.picture} {self.name}")
        info_lines.append(f"Здоровье: {self.current_health:.1f}/{self.max_health:.1f}")
        info_lines.append(f"Броня: {self.current_armor:.1%}")
        info_lines.append(f"Маг. сопротивление: {self.current_magic_resistance:.1%}")
        
        if self.current_attack_amplify != 0:
            info_lines.append(f"Сила атаки: {self.current_attack_amplify:.1%}")
        if self.current_magic_amplify != 0:
            info_lines.append(f"Сила магии: {self.current_magic_amplify:.1%}")
        
        # Статус оглушения
        if self.stunned:
            info_lines.append("💫 Оглушен")
        
        # Активные эффекты
        if self.effects:
            info_lines.append("\nАктивные эффекты:")
            for effect in self.effects:
                info_lines.append(f"  {effect.icon} {effect.description} {effect.duration}")
        else:
            info_lines.append("\nАктивные эффекты: нет")
        
        # Способности - используем get_full_info() для каждой способности
        if self.abilities:
            info_lines.append("\nСпособности:")
            for i, ability in enumerate(self.abilities, 1):
                # Получаем всю информацию из способности
                ability_info = ability.get_full_info()
                # Добавляем номер способности
                info_lines.append(f"  {i}. {ability_info}")
        else:
            info_lines.append("\nСпособности: нет")
        
        return "\n".join(info_lines)

    def get_short_info(self) -> str:
        """Краткая информация о персонаже"""
        status = "💫" if self.stunned else "✅"
        effects_count = len(self.effects)
        effects_info = f" 📊{effects_count}" if effects_count > 0 else ""
        
        return f"{status}{self.picture} {self.name} ❤️{self.current_health:.0f}/{self.max_health:.0f}{effects_info}"

    def get_abilities_info(self) -> List[str]:
        """Возвращает информацию о способностях для UI"""
        abilities_info = []
        for i, ability in enumerate(self.abilities, 1):
            ability_name = ability.get_name()
            if ability.current_cooldown > 0:
                status = f" (Перезарядка: {ability.current_cooldown})"
            else:
                status = " (Готово)"
            abilities_info.append(f"{i}. {ability_name}{status}")
        return abilities_info

    def __str__(self) -> str:
        return f"{self.name} - HP: {self.current_health:.1f}/{self.max_health:.1f}"