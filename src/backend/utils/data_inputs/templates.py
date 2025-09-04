from src.backend.utils.models.enums.general import *
from src.backend.utils.models.enums.runes import *
from src.backend.utils.models.enums.stats import *

NORMAL_SLOT_ONE_NO_PREFIX_RUNE = {
    "slot": RuneSlot.ONE,
    "stars": RuneStars.SIX,
    "default_grade": Grade.NORMAL,
    "rune_set": RuneSet.ENERGY,
    "main_property": StatProperty.ATK_ADD,
    "prefix_property": StatProperty.NO_PROPERTY,
    "prefix_value": 0,
    "innate_sub_properties": None,
    "innate_sub_upgrades": None,
    "innate_sub_values": {},
    "additional_sub_properties": [
        StatProperty.ATK_MUL, StatProperty.HP_ADD,
        StatProperty.HP_MUL, StatProperty.CD],
    "additional_sub_values": {
        StatProperty.ATK_MUL: 6, StatProperty.HP_ADD: 200, 
        StatProperty.HP_MUL: 6, StatProperty.CD: 5
    }
}

MAGIC_SLOT_TWO_WITH_PREFIX_RUNE = {
    "slot": RuneSlot.TWO,
    "stars": RuneStars.SIX,
    "default_grade": Grade.MAGIC,
    "rune_set": RuneSet.GUARD,
    "main_property": StatProperty.SPD,
    "prefix_property": StatProperty.CR,
    "prefix_value": 6,
    "innate_sub_properties": [StatProperty.HP_MUL],
    "innate_sub_upgrades": {StatProperty.HP_MUL: 1},
    "innate_sub_values": {StatProperty.HP_MUL: 12},
    "additional_sub_properties": [
        StatProperty.RES, StatProperty.ACC,
        StatProperty.DEF_ADD],
    "additional_sub_values": {
        StatProperty.RES: 8, StatProperty.ACC: 5, StatProperty.DEF_ADD: 16
    }
}

RARE_SLOT_FIVE_NO_PREFIX_RUNE = {
    "slot": RuneSlot.FIVE,
    "stars": RuneStars.SIX,
    "default_grade": Grade.RARE,
    "rune_set": RuneSet.FIGHT,
    "main_property": StatProperty.HP_ADD,
    "prefix_property": StatProperty.NO_PROPERTY,
    "prefix_value": 0,
    "innate_sub_properties": [
        StatProperty.DEF_MUL, StatProperty.ATK_MUL],
    "innate_sub_upgrades": {StatProperty.DEF_MUL: 1, StatProperty.ATK_MUL: 1},
    "innate_sub_values": {StatProperty.DEF_MUL: 14, StatProperty.ATK_MUL: 13},
    "additional_sub_properties": [StatProperty.HP_MUL, StatProperty.SPD],
    "additional_sub_values": {StatProperty.HP_MUL: 6, StatProperty.SPD: 4}
}

HERO_SLOT_FOUR_NO_PREFIX_RUNE = {
    "slot": RuneSlot.FOUR,
    "stars": RuneStars.SIX,
    "default_grade": Grade.HERO,
    "rune_set": RuneSet.VIOLENT,
    "main_property": StatProperty.CD,
    "prefix_property": StatProperty.NO_PROPERTY,
    "prefix_value": 0,
    "innate_sub_properties": [
        StatProperty.ATK_MUL, StatProperty.SPD,
        StatProperty.CR],
    "innate_sub_upgrades": {
        StatProperty.ATK_MUL: 0, StatProperty.SPD: 2,
        StatProperty.CR: 1},
    "innate_sub_values": {
        StatProperty.ATK_MUL: 8, StatProperty.SPD: 18,
        StatProperty.CR: 10},
    "additional_sub_properties": [StatProperty.DEF_ADD],
    "additional_sub_values": {StatProperty.DEF_ADD: 12}
}

LEGEND_SLOT_SIX_WITH_PREFIX_RUNE = {
    "slot": RuneSlot.SIX,
    "stars": RuneStars.SIX,
    "default_grade": Grade.LEGEND,
    "rune_set": RuneSet.SWIFT,
    "main_property": StatProperty.HP_MUL,
    "prefix_property": StatProperty.ACC,
    "prefix_value": 8,
    "innate_sub_properties": [
        StatProperty.DEF_MUL, StatProperty.SPD,
        StatProperty.CR, StatProperty.RES],
    "innate_sub_upgrades": {
        StatProperty.DEF_MUL: 0, StatProperty.SPD: 4,
        StatProperty.CR: 0, StatProperty.RES: 0},
    "innate_sub_values": {
        StatProperty.DEF_MUL: 8, StatProperty.SPD: 26,
        StatProperty.CR: 6, StatProperty.RES: 8},
    "additional_sub_properties": None,
    "additional_sub_values": {}
}