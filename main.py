#ЭТО ФАЙЛ ДЛЯ ТЕСТОВ

from Characters.CharacterGenerator import CharacterGenerator
from Abilities.AbilityGenerator import AbilityGenerator
import copy

abilities = AbilityGenerator.load_abilities('Abilities/abilities.yaml')
northpaw_veteran1 = copy.deepcopy(CharacterGenerator.load_characters('Characters/characters.yaml', abilities)['northpaw_veteran'])
bloodfang_berserk = copy.deepcopy(CharacterGenerator.load_characters('Characters/characters.yaml', abilities)['bloodfang_berserk'])


#print(northpaw_veteran1.abilities[4].use(northpaw_veteran1, bloodfang_berserk))

print(northpaw_veteran1.info())
print(bloodfang_berserk.info())

#characters = [northpaw_veteran1, bloodfang_berserk]
#for character in characters:
#    character.update_effects()

#print(northpaw_veteran1.info())
#print(bloodfang_berserk.info())