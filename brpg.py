import sys
import os
import random
import math
import openpyxl
import pyperclip
import copy

"""
todo:
	high priority
		- refactor combat logic
		- rework status effects
		- rework inventory
	low priority
"""


# Prints out a message and requires the user to press enter to continue. End determines where the cursor is placed (empty space is at the end of the string, \n is on a new line).
def proceduralPrint(string, end):
	print(string, end = end)
	input()


# Returns a bar based on a desired length, the alignment (0 for left align, 1 for right align), a character for the bar, a current value, and a max value.
def generalUIBar(length, alignment, characterString, currentValue, maxValue):
	if (len(characterString) > 1):
		characterString = characterString[0]

	if (alignment == 1):
		alignment = ">"
		borderStyle = "\\"
	else:
		alignment = "<"
		borderStyle = "/"

	barPercentage = currentValue / maxValue
	barDisplay = characterString * int(math.ceil((length * barPercentage)))

	return (borderStyle + ("{:" + alignment + str(length) + "}").format(barDisplay) + borderStyle)


# Returns a row of the battle UI based on the provided string and the alignment (0 for left align, 1 for right align).
def battleUIRow(string, alignment):
	if (len(string) > 37):
		string = string[0:37]

	if (alignment == 0):
		currentRow = "| {:<37} |".format(string)
	else:
		currentRow = " {:>37} |".format(string)

	return currentRow


# Returns a row divider for the battle UI.
def battleUIRowDivider():
	return "+–––––––––––––––––––––––––––––––––––––––+–––––––––––––––––––––––––––––––––––––––+"


# Returns a row of the level up UI based on the provided value and the mode (0 for standard text, 1 for stat names, 2 for current stats, 3 for change in stats).
def levelUpUIRow(value, mode):
	currentRow = ""
	if (mode == 0):
		currentRow += "| " + str(value)
		currentRow += "\t" * (11 - math.ceil(len(currentRow) / 8))
		currentRow += "|"
	elif (mode == 1):
		currentRow += "|\tHP\tMP\tMA\tRA\tMD\tRD\tACC\tEVA\t\t|"
	elif (mode == 2):
		currentRow += "|"
		currentRow += "\t " + "{:q>4}".format(str(value.hp))
		currentRow += "\t " + "{:q>4}".format(str(value.mp))
		currentRow += "\t " + "{:q>4}".format(str(value.ballisticAttack))
		currentRow += "\t " + "{:q>4}".format(str(value.magicAttack))
		currentRow += "\t " + "{:q>4}".format(str(value.ballisticDefense))
		currentRow += "\t " + "{:q>4}".format(str(value.magicDefense))
		currentRow += "\t " + "{:q>4}".format(str(value.accuracy))
		currentRow += "\t " + "{:q>4}".format(str(value.evade))
		currentRow += "\t\t|"

		for i in range(len(currentRow)):
			if (currentRow[i] == "q"):
				currentRow = currentRow[0:i] + " " + currentRow[i+1:len(currentRow)]
	elif (mode == 3):
		currentRow += "|"
		currentRow += "\t+" + "{:q>4}".format(str(value.hp))
		currentRow += "\t+" + "{:q>4}".format(str(value.mp))
		currentRow += "\t+" + "{:q>4}".format(str(value.ballisticAttack))
		currentRow += "\t+" + "{:q>4}".format(str(value.magicAttack))
		currentRow += "\t+" + "{:q>4}".format(str(value.ballisticDefense))
		currentRow += "\t+" + "{:q>4}".format(str(value.magicDefense))
		currentRow += "\t+" + "{:q>4}".format(str(value.accuracy))
		currentRow += "\t+" + "{:q>4}".format(str(value.evade))
		currentRow += "\t\t|"

		for i in range(len(currentRow)):
			if (currentRow[i] == "q"):
				currentRow = currentRow[0:i] + " " + currentRow[i+1:len(currentRow)]

	return currentRow


# Rounds a value into an integer and then converts the result into another specified variable type.
def superRound(value, varType):
	return varType(round(value)) if (value != None) else None


# Clears the screen.
def clearScreen():
	if (os.name == "nt"):
		os.system("cls")
	else:
		os.system("clear")


# Formats text based on alignment and length.
def formatText(text, alignment, length):
	text = str(text)

	if (alignment == 0):
		alignment = "<"
	elif (alignment == 1):
		alignment = "^"
	elif (alignment == 2):
		alignment = ">"

	if (len(str(text)) > length):
		text = text[0:(length - 3)] + "..."

	return str("{:" + alignment + str(length) + "}").format(text)


# Initialize classes #
class Stats:
	def __init__(self, hp=1, mp=1, ballisticAttack=1, magicAttack=1, ballisticDefense=1, magicDefense=1, accuracy=1, evade=1, every=1):
		self.hp = every if (every != 1 and hp == 1) else hp
		self.mp = every if (every != 1 and mp == 1) else mp
		self.ballisticAttack = every if (every != 1 and ballisticAttack == 1) else ballisticAttack
		self.magicAttack = every if (every != 1 and magicAttack == 1) else magicAttack
		self.ballisticDefense = every if (every != 1 and ballisticDefense == 1) else ballisticDefense
		self.magicDefense = every if (every != 1 and magicDefense == 1) else magicDefense
		self.accuracy = every if (every != 1 and accuracy == 1) else accuracy
		self.evade = every if (every != 1 and evade == 1) else evade

	def __add__(self, other):
		totalHP = self.hp
		totalMP = self.mp
		totalBallisticAttack = self.ballisticAttack
		totalMagicAttack = self.magicAttack
		totalBallisticDefense = self.ballisticDefense
		totalMagicDefense = self.magicDefense
		totalAccuracy = self.accuracy
		totalEvade = self.evade

		if (type(other) is int):
			totalHP += other
			totalMP += other
			totalBallisticAttack += other
			totalMagicAttack += other
			totalBallisticDefense += other
			totalMagicDefense += other
			totalAccuracy += other
			totalEvade += other

		elif (type(other) is Stats):
			totalHP += other.hp
			totalMP += other.mp
			totalBallisticAttack += other.ballisticAttack
			totalMagicAttack += other.magicAttack
			totalBallisticDefense += other.ballisticDefense
			totalMagicDefense += other.magicDefense
			totalAccuracy += other.accuracy
			totalEvade += other.evade

		return Stats(
			totalHP,
			totalMP,
			totalBallisticAttack,
			totalMagicAttack,
			totalBallisticDefense,
			totalMagicDefense,
			totalAccuracy,
			totalEvade
		)

	def __sub__(self, other):
		totalHP = self.hp
		totalMP = self.mp
		totalBallisticAttack = self.ballisticAttack
		totalMagicAttack = self.magicAttack
		totalBallisticDefense = self.ballisticDefense
		totalMagicDefense = self.magicDefense
		totalAccuracy = self.accuracy
		totalEvade = self.evade

		if (type(other) is int):
			totalHP -= other
			totalMP -= other
			totalBallisticAttack -= other
			totalMagicAttack -= other
			totalBallisticDefense -= other
			totalMagicDefense -= other
			totalAccuracy -= other
			totalEvade -= other

		elif (type(other) is Stats):
			totalHP -= other.hp
			totalMP -= other.mp
			totalBallisticAttack -= other.ballisticAttack
			totalMagicAttack -= other.magicAttack
			totalBallisticDefense -= other.ballisticDefense
			totalMagicDefense -= other.magicDefense
			totalAccuracy -= other.accuracy
			totalEvade -= other.evade

		return Stats(
			totalHP,
			totalMP,
			totalBallisticAttack,
			totalMagicAttack,
			totalBallisticDefense,
			totalMagicDefense,
			totalAccuracy,
			totalEvade
		)


class StatusEffect:
	def __init__(self, name, effect):
		self.name = name
		self.effect = effect

	def __repr__(self):
		return str(self.name)


class Skill:
	def __init__(self, name="Null", skillType=0, statType=0, element=0, mpChange=0, targetingTypeA=None, basePowerA=None, targetingTypeB=None, basePowerB=None, accuracyMod=0.00, critChance=0.00, randomMod=0.00, buffDebuff=None, statusEffect=None, statusEffectDuration=0):
		self.name = str(name)
		self.skillType = skillTypes[skillType]
		self.statType = statTypes[statType]
		self.element = elements[element]
		self.mpChange = mpChange
		self.targetingTypeA = targetingTypes[targetingTypeA] if (targetingTypeA != None) else None
		self.basePowerA = basePowerA
		self.targetingTypeB = targetingTypes[targetingTypeB] if (targetingTypeB != None) else None
		self.basePowerB = basePowerB
		self.accuracyMod = accuracyMod
		self.critChance = critChance
		self.randomMod = randomMod
		self.buffDebuff = buffDebuff
		if (statusEffect != None):
			self.statusEffect = statusEffectsList[statusEffect]
		else:
			self.statusEffect = None
		self.statusEffectDuration = statusEffectDuration

		if (self.targetingTypeA == None or self.basePowerA == None):
			self.targetingTypeA = None
			self.basePowerA = None
		if (self.targetingTypeB == None or self.basePowerB == None):
			self.targetingTypeB = None
			self.basePowerB = None
		if ((self.targetingTypeA == None or self.basePowerA == None) and self.targetingTypeB != None and self.basePowerB != None):
			self.targetingTypeA = self.targetingTypeB
			self.basePowerA = self.basePowerB
			self.targetingTypeB = None
			self.basePowerB = None

		self.skillLevel = 1


	def __repr__(self):
		costString = superRound(self.mpChange, str) if (self.mpChange < 0) else "+" + superRound(self.mpChange, str)
		powerAString = superRound((self.basePowerA * 100), str) + "%" if (self.basePowerA != None) else "None"
		powerBString = superRound((self.basePowerB * 100), str) + "%" if (self.basePowerB != None) else "None"
		accuracyString = "Guaranteed" if (self.accuracyMod >= 100) else superRound((self.accuracyMod * 100), str) + "%"
		effectsString = str(self.statusEffect.name) + " for " + str(self.statusEffectDuration) + " turns" if (self.statusEffect != None and self.statusEffectDuration > 0) else "None"

		if (self.targetingTypeA != None and self.targetingTypeB != None and self.basePowerA != None and self.basePowerB != None):
			return (
				"+–––––––––––––––––––––––––––––––+"
				+ "\n| " + formatText(self.name, 0, 29) + " |"
				+ "\n+–––––––+–––––––––––––––––––––––––––––––––––––––––––––––+"
				+ "\n| " + formatText("MP", 0, 5) + " | " + formatText(costString, 0, 45) + " |"
				+ "\n| " + formatText("Type", 0, 5) + " | " + formatText(self.statType, 0, 45) + " |"
				+ "\n| " + formatText("Elmnt", 0, 5) + " | " + formatText(self.element, 0, 45) + " |"
				+ "\n| " + formatText("Trgt", 0, 5) + " | " + formatText(self.targetingTypeA, 0, 21) + " | " + formatText(self.targetingTypeB, 0, 21) + " |"
				+ "\n| " + formatText("Power", 0, 5) + " | " + formatText(powerAString, 0, 21) + " | " + formatText(powerBString, 0, 21) + " |"
				+ "\n| " + formatText("Acc.", 0, 5) + " | " + formatText(accuracyString, 0, 21) + " | " + formatText(accuracyString, 0, 21) + " |"
				+ "\n| " + formatText("Effct", 0, 5) + " | " + formatText(effectsString, 0, 21) + " | " + formatText(effectsString, 0, 21) + " |"
				+ "\n+–––––––+–––––––––––––––––––––––––––––––––––––––––––––––+"
			)
		else:
			return (
				"+–––––––––––––––––––––––––––––––+"
				+ "\n| " + formatText(self.name, 0, 29) + " |"
				+ "\n+–––––––+–––––––––––––––––––––––––––––––––––––––––––––––+"
				+ "\n| " + formatText("MP", 0, 5) + " | " + formatText(costString, 0, 45) + " |"
				+ "\n| " + formatText("Type", 0, 5) + " | " + formatText(self.statType, 0, 45) + " |"
				+ "\n| " + formatText("Elmnt", 0, 5) + " | " + formatText(self.element, 0, 45) + " |"
				+ "\n| " + formatText("Trgt", 0, 5) + " | " + formatText(self.targetingTypeA, 0, 45) + " |"
				+ "\n| " + formatText("Power", 0, 5) + " | " + formatText(powerAString, 0, 45) + " |"
				+ "\n| " + formatText("Acc.", 0, 5) + " | " + formatText(accuracyString, 0, 45) + " |"
				+ "\n| " + formatText("Effct", 0, 5) + " | " + formatText(effectsString, 0, 45) + " |"
				+ "\n+–––––––+–––––––––––––––––––––––––––––––––––––––––––––––+"
			)


class Item:
	def __init__(self, name, itemType, primaryPower, secondaryPower, value):
		self.name = name
		self.itemType = itemType
		self.primaryPower = primaryPower
		self.secondaryPower = secondaryPower
		self.value = value

	def __repr__(self):
		if (self.itemType == itemTypes[0]):
			powerString = str(self.primaryPower) + " HP or " + str(self.secondaryPower) + "% HP (whichever is higher)"
		else:
			powerString = str(self.primaryPower) + " MP or " + str(self.secondaryPower) + "% MP (whichever is higher)"

		return "+–––––––+–––––––––––––––––––––––––––––––+\n|Name\t| " + str(self.name) + "\n|Type\t| " + str(self.itemType) + "\n|Power\t| " + powerString + "\n+–––––––+–––––––––––––––––––––––––––––––+"


class PlayerCharacter:
	def __init__(self, name="Null", stats=Stats(), skills=[], inventory="050100050100"):
		self.name = name
		self.curHP = 1
		self.curMP = 1

		self.baseStats = stats

		self.leveledUpStats = Stats(
			round(self.baseStats.hp * (1.05 ** (partyLevel - 1))),
			round(self.baseStats.mp * (1.01 ** (partyLevel - 1))),
			round(self.baseStats.ballisticAttack * (1.05 ** (partyLevel - 1))),
			round(self.baseStats.magicAttack * (1.05 ** (partyLevel - 1))),
			round(self.baseStats.ballisticDefense * (1.05 ** (partyLevel - 1))),
			round(self.baseStats.magicDefense * (1.05 ** (partyLevel - 1))),
			round(self.baseStats.accuracy * (1.05 ** (partyLevel - 1))),
			round(self.baseStats.evade * (1.05 ** (partyLevel - 1)))
		)

		self.skills = skills

		self.itemInventory = [
			int(inventory[0:2]),
			int(inventory[2:4]),
			int(inventory[4:6]),
			int(inventory[6:8]),
			int(inventory[8:10]),
			int(inventory[10:12])
		]

		self.buffsDebuffs = Stats(100, 100, 100, 100, 100, 100, 100, 100)

		self.statusEffects = []
		self.statusEffectDurations = []

		self.totalStats = Stats()
		self.evaluateTotalStats()

		self.maxHP = self.totalStats.hp
		self.maxMP = self.totalStats.mp
		self.curHP = self.maxHP
		self.curMP = self.maxMP

	def evaluateTotalStats(self):
		healthRatio = self.curHP / self.totalStats.hp
		manaRatio = self.curMP / self.totalStats.mp

		self.totalStats = Stats(
			round(self.leveledUpStats.hp * (self.buffsDebuffs.hp / 100)),
			round(self.leveledUpStats.mp * (self.buffsDebuffs.mp / 100)),
			round(self.leveledUpStats.ballisticAttack * (self.buffsDebuffs.ballisticAttack / 100)),
			round(self.leveledUpStats.magicAttack * (self.buffsDebuffs.magicAttack / 100)),
			round(self.leveledUpStats.ballisticDefense * (self.buffsDebuffs.ballisticDefense / 100)),
			round(self.leveledUpStats.magicDefense * (self.buffsDebuffs.magicDefense / 100)),
			round(self.leveledUpStats.accuracy * (self.buffsDebuffs.accuracy / 100)),
			round(self.leveledUpStats.evade * (self.buffsDebuffs.evade / 100))
		)

		self.maxHP = self.totalStats.hp
		self.maxMP = self.totalStats.mp
		self.curHP = int(self.totalStats.hp * healthRatio)
		self.curMP = int(self.totalStats.mp * manaRatio)

	def evaluateCurrentPoints(self):
		if (self.curHP > self.maxHP):
			self.curHP = self.maxHP
		elif (self.curHP < 0):
			self.curHP = 0

		if (self.curMP > self.maxMP):
			self.curMP = self.maxMP
		elif (self.curMP < 0):
			self.curMP = 0


class EnemyCharacter:
	def __init__(self, name="Null", stats=Stats(), skills=[]):
		self.name = name
		# levelConstant = gameRegion * regionBattle
		self.currentLevel = random.choice([max(1, partyLevel - 1), max(1, partyLevel - 1), max(1, partyLevel - 1), partyLevel, partyLevel, partyLevel, partyLevel, min(maxPlayerLevel, partyLevel + 1)])
		self.curHP = 1

		self.baseStats = stats

		self.leveledUpStats = Stats(
			round(self.baseStats.hp * (1.05 ** (self.currentLevel - 1))),
			0,
			round(self.baseStats.ballisticAttack * (1.05 ** (self.currentLevel - 1))),
			round(self.baseStats.magicAttack * (1.05 ** (self.currentLevel - 1))),
			round(self.baseStats.ballisticDefense * (1.05 ** (self.currentLevel - 1))),
			round(self.baseStats.magicDefense * (1.05 ** (self.currentLevel - 1))),
			round(self.baseStats.accuracy * (1.05 ** (self.currentLevel - 1))),
			round(self.baseStats.evade * (1.05 ** (self.currentLevel - 1)))
		)

		self.skills = skills

		self.buffsDebuffs = Stats(100, 100, 100, 100, 100, 100, 100, 100)

		self.statusEffects = []
		self.statusEffectDurations = []

		self.totalStats = Stats()
		self.evaluateTotalStats()
		# self.checkForLevelUp()

		self.maxHP = self.totalStats.hp
		self.curHP = self.maxHP

	def evaluateTotalStats(self):
		healthRatio = self.curHP / self.totalStats.hp

		self.totalStats = Stats(
			round(self.leveledUpStats.hp * (self.buffsDebuffs.hp / 100)),
			1,
			round(self.leveledUpStats.ballisticAttack * (self.buffsDebuffs.ballisticAttack / 100)),
			round(self.leveledUpStats.magicAttack * (self.buffsDebuffs.magicAttack / 100)),
			round(self.leveledUpStats.ballisticDefense * (self.buffsDebuffs.ballisticDefense / 100)),
			round(self.leveledUpStats.magicDefense * (self.buffsDebuffs.magicDefense / 100)),
			round(self.leveledUpStats.accuracy * (self.buffsDebuffs.accuracy / 100)),
			round(self.leveledUpStats.evade * (self.buffsDebuffs.evade / 100))
		)

		self.maxHP = self.totalStats.hp
		self.curHP = superRound(self.totalStats.hp * healthRatio, int)

	def evaluateCurrentPoints(self):
		if (self.curHP > self.maxHP):
			self.curHP = self.maxHP
		elif (self.curHP < 0):
			self.curHP = 0

	# def checkForLevelUp(self):
	# 	self.baseStats = Stats(
	# 		math.ceil(self.baseStats.hp * (self.levelUpStats.hp ** (self.currentLevel - 1))),
	# 		math.ceil(self.baseStats.ballisticAttack * (self.levelUpStats.ballisticAttack ** (self.currentLevel - 1))),
	# 		math.ceil(self.baseStats.magicAttack * (self.levelUpStats.magicAttack ** (self.currentLevel - 1))),
	# 		math.ceil(self.baseStats.ballisticDefense * (self.levelUpStats.ballisticDefense ** (self.currentLevel - 1))),
	# 		math.ceil(self.baseStats.magicDefense * (self.levelUpStats.magicDefense ** (self.currentLevel - 1))),
	# 		math.ceil(self.baseStats.accuracy * (self.levelUpStats.accuracy ** (self.currentLevel - 1))),
	# 		math.ceil(self.baseStats.evade * (self.levelUpStats.evade ** (self.currentLevel - 1)))
	# 	)
	# 	self.evaluateTotalStats()


# Initialize game data #
maxPlayerLevel = 50

gameRegion = 1
regionBattle = 1
battleTurn = 0

partyMoney = 500
partyLevel = 1
partyCurrentXP = 0
partyNextXP = 200 * (1.15 ** (partyLevel - 1))
partyCurrentFocus = 1.00
partyMaxFocus = 1.00

currentPlayers = [None, None, None]
currentEnemies = [None, None, None]

selectedPlayer = -1
selectedEnemy = -1

playersAlive = [None, None, None]
enemiesAlive = [None, None, None]

playersHaveMoved = [None, None, None]
enemiesHaveMoved = [None, None, None]

playerClasses = {
	0: "None",
	1: "Class A",
	2: "Class B",
	3: "Class C",
}

regions = {
	0: "None",
	1: "Green Grasslands",
	2: "Crude Crimson",
	3: "Dark Depths",
}

equipmentSlots = {
	0: "Weapon",
	1: "Armor"
}

skillTypes = {
	0: "–",
	1: "Attack",
	2: "Heal",
	3: "Revive",
	4: "Buff",
	5: "Debuff",
}

statTypes = {
	0: "None",
	1: "Ballistic",
	2: "Magic"
}

targetingTypes = {
	0: "None",
	1: "Self",
	2: "Single Enemy",
	3: "All Enemies",
	4: "Single Ally (Living)",
	5: "All Allies (Living)",
	6: "Single Ally (Dead)",
	7: "All Allies (Dead)",
}

elements = {
	0: "None",
	1: "Non-elemental",
	2: "Fire",
	3: "Water",
	4: "Ice",
	5: "Inherited",
	6: "Heal",
	7: "Revive",
	8: "Buff",
	9: "Debuff"
}

resources = {
	0: "None",
	1: " HP",
	2: " MP",
	3: " HP/MP",
	4: "% HP",
	5: "% MP",
	6: "% HP/MP"
}

flatResources = [
	resources[2],
	resources[3],
	resources[4]
]

percentageResources = [
	resources[5],
	resources[6],
	resources[6]
]

itemTypes = {
	0: "HP Recovery",
	1: "MP Recovery"
}

# Contains the list for status effects.
statusEffectsList = {
	0: StatusEffect("Healthy I",Stats(15,0,0,0,0,0,0,0)),1: StatusEffect("Healthy II",Stats(30,0,0,0,0,0,0,0)),2: StatusEffect("Healthy III",Stats(45,0,0,0,0,0,0,0)),3: StatusEffect("Energetic I",Stats(0,15,0,0,0,0,0,0)),4: StatusEffect("Energetic II",Stats(0,30,0,0,0,0,0,0)),5: StatusEffect("Energetic III",Stats(0,45,0,0,0,0,0,0)),6: StatusEffect("Strengthened I",Stats(0,0,15,0,0,0,0,0)),7: StatusEffect("Strengthened II",Stats(0,0,30,0,0,0,0,0)),8: StatusEffect("Strengthened III",Stats(0,0,45,0,0,0,0,0)),9: StatusEffect("Sharpened I",Stats(0,0,0,15,0,0,0,0)),10: StatusEffect("Sharpened II",Stats(0,0,0,30,0,0,0,0)),11: StatusEffect("Sharpened III",Stats(0,0,0,45,0,0,0,0)),12: StatusEffect("Shielded I",Stats(0,0,0,0,15,0,0,0)),13: StatusEffect("Shielded II",Stats(0,0,0,0,30,0,0,0)),14: StatusEffect("Shielded III",Stats(0,0,0,0,45,0,0,0)),15: StatusEffect("Barriered I",Stats(0,0,0,0,0,15,0,0)),16: StatusEffect("Barriered II",Stats(0,0,0,0,0,30,0,0)),17: StatusEffect("Barriered III",Stats(0,0,0,0,0,45,0,0)),18: StatusEffect("Accurate I",Stats(0,0,0,0,0,0,15,0)),19: StatusEffect("Accurate II",Stats(0,0,0,0,0,0,30,0)),20: StatusEffect("Accurate III",Stats(0,0,0,0,0,0,45,0)),21: StatusEffect("Evasive I",Stats(0,0,0,0,0,0,0,15)),22: StatusEffect("Evasive II",Stats(0,0,0,0,0,0,0,30)),23: StatusEffect("Evasive III",Stats(0,0,0,0,0,0,0,45)),24: StatusEffect("Resourceful I",Stats(15,15,0,0,0,0,0,0)),25: StatusEffect("Resourceful II",Stats(30,30,0,0,0,0,0,0)),26: StatusEffect("Resourceful III",Stats(45,45,0,0,0,0,0,0)),27: StatusEffect("Offensive I",Stats(0,0,15,15,0,0,15,0)),28: StatusEffect("Offensive II",Stats(0,0,30,30,0,0,30,0)),29: StatusEffect("Offensive III",Stats(0,0,45,45,0,0,45,0)),30: StatusEffect("Defensive I",Stats(0,0,0,0,15,15,0,15)),31: StatusEffect("Defensive II",Stats(0,0,0,0,30,30,0,30)),32: StatusEffect("Defensive III",Stats(0,0,0,0,45,45,0,45)),33: StatusEffect("Agile I",Stats(0,0,0,0,0,0,15,15)),34: StatusEffect("Agile II",Stats(0,0,0,0,0,0,30,30)),35: StatusEffect("Agile III",Stats(0,0,0,0,0,0,45,45)),36: StatusEffect("Enhanced I",Stats(15,0,15,0,15,0,0,0)),37: StatusEffect("Enhanced II",Stats(30,0,30,0,30,0,0,0)),38: StatusEffect("Enhanced III",Stats(45,0,45,0,45,0,0,0)),39: StatusEffect("Enchanted I",Stats(0,15,0,15,0,15,0,0)),40: StatusEffect("Enchanted II",Stats(0,30,0,30,0,30,0,0)),41: StatusEffect("Enchanted III",Stats(0,45,0,45,0,45,0,0)),42: StatusEffect("Empowered I",Stats(15,15,15,15,15,15,15,15)),43: StatusEffect("Empowered II",Stats(30,30,30,30,30,30,30,30)),44: StatusEffect("Empowered III",Stats(45,45,45,45,45,45,45,45)),45: StatusEffect("Ill I",Stats(-15,0,0,0,0,0,0,0)),46: StatusEffect("Ill II",Stats(-30,0,0,0,0,0,0,0)),47: StatusEffect("Ill III",Stats(-45,0,0,0,0,0,0,0)),48: StatusEffect("Lethargic I",Stats(0,-15,0,0,0,0,0,0)),49: StatusEffect("Lethargic II",Stats(0,-30,0,0,0,0,0,0)),50: StatusEffect("Lethargic III",Stats(0,-45,0,0,0,0,0,0)),51: StatusEffect("Weakened I",Stats(0,0,-15,0,0,0,0,0)),52: StatusEffect("Weakened II",Stats(0,0,-30,0,0,0,0,0)),53: StatusEffect("Weakened III",Stats(0,0,-45,0,0,0,0,0)),54: StatusEffect("Dulled I",Stats(0,0,0,-15,0,0,0,0)),55: StatusEffect("Dulled II",Stats(0,0,0,-30,0,0,0,0)),56: StatusEffect("Dulled III",Stats(0,0,0,-45,0,0,0,0)),57: StatusEffect("Broken I",Stats(0,0,0,0,-15,0,0,0)),58: StatusEffect("Broken II",Stats(0,0,0,0,-30,0,0,0)),59: StatusEffect("Broken III",Stats(0,0,0,0,-45,0,0,0)),60: StatusEffect("Shattered I",Stats(0,0,0,0,0,-15,0,0)),61: StatusEffect("Shattered II",Stats(0,0,0,0,0,-30,0,0)),62: StatusEffect("Shattered III",Stats(0,0,0,0,0,-45,0,0)),63: StatusEffect("Blinded I",Stats(0,0,0,0,0,0,-15,0)),64: StatusEffect("Blinded II",Stats(0,0,0,0,0,0,-30,0)),65: StatusEffect("Blinded III",Stats(0,0,0,0,0,0,-45,0)),66: StatusEffect("Sluggish I",Stats(0,0,0,0,0,0,0,-15)),67: StatusEffect("Sluggish II",Stats(0,0,0,0,0,0,0,-30)),68: StatusEffect("Sluggish III",Stats(0,0,0,0,0,0,0,-45)),69: StatusEffect("Drained I",Stats(-15,-15,0,0,0,0,0,0)),70: StatusEffect("Drained II",Stats(-30,-30,0,0,0,0,0,0)),71: StatusEffect("Drained III",Stats(-45,-45,0,0,0,0,0,0)),72: StatusEffect("Distracted I",Stats(0,0,-15,-15,0,0,-15,0)),73: StatusEffect("Distracted II",Stats(0,0,-30,-30,0,0,-30,0)),74: StatusEffect("Distracted III",Stats(0,0,-45,-45,0,0,-45,0)),75: StatusEffect("Offguard I",Stats(0,0,0,0,-15,-15,0,-15)),76: StatusEffect("Offguard II",Stats(0,0,0,0,-30,-30,0,-30)),77: StatusEffect("Offguard III",Stats(0,0,0,0,-45,-45,0,-45)),78: StatusEffect("Clumsy I",Stats(0,0,0,0,0,0,-15,-15)),79: StatusEffect("Clumsy II",Stats(0,0,0,0,0,0,-30,-30)),80: StatusEffect("Clumsy III",Stats(0,0,0,0,0,0,-45,-45)),81: StatusEffect("Poisoned I",Stats(-15,0,-15,0,-15,0,0,0)),82: StatusEffect("Poisoned II",Stats(-30,0,-30,0,-30,0,0,0)),83: StatusEffect("Poisoned III",Stats(-45,0,-45,0,-45,0,0,0)),84: StatusEffect("Cursed I",Stats(0,-15,0,-15,0,-15,0,0)),85: StatusEffect("Cursed II",Stats(0,-30,0,-30,0,-30,0,0)),86: StatusEffect("Cursed III",Stats(0,-45,0,-45,0,-45,0,0)),87: StatusEffect("Empowered I",Stats(-15,-15,-15,-15,-15,-15,-15,-15)),88: StatusEffect("Empowered II",Stats(-30,-30,-30,-30,-30,-30,-30,-30)),89: StatusEffect("Empowered III",Stats(-45,-45,-45,-45,-45,-45,-45,-45)),90: StatusEffect("Defending",Stats(0,0,0,0,50,50,0,0)),91: StatusEffect("Evading",Stats(0,0,0,0,0,0,0,50)),92: StatusEffect("Burn",Stats(-1,0,0,0,0,0,0,0)),93: StatusEffect("Blaze",Stats(-2,0,0,0,0,0,0,0)),94: StatusEffect("Scorch",Stats(-3,0,0,0,0,0,0,0)),95: StatusEffect("Wet",Stats(0,0,0,0,-10,-10,0,0)),96: StatusEffect("Soak",Stats(0,0,0,0,-20,-20,0,0)),97: StatusEffect("Drench",Stats(0,0,0,0,-30,-30,0,0)),98: StatusEffect("Frozen",Stats(0,0,0,0,0,0,-2,-2)),99: StatusEffect("Frostbite",Stats(0,0,0,0,0,0,-4,-4)),100: StatusEffect("Frostburn",Stats(0,0,0,0,0,0,-6,-6)),101: StatusEffect("Refreshing",Stats(0,0,0,0,0,0,0,0)),102: StatusEffect("Regrowing",Stats(0,0,0,0,0,0,0,0)),103: StatusEffect("Renewing",Stats(0,0,0,0,0,0,0,0)),104: StatusEffect("Napping",Stats(0,0,0,0,0,0,0,0)),105: StatusEffect("Resting",Stats(0,0,0,0,0,0,0,0)),106: StatusEffect("Relaxing",Stats(0,0,0,0,0,0,0,0)),
}

# Contains the list for skills.
skillsList = {
	0: Skill(),
	1: Skill(
		name = "Skip",
		skillType = 0,
		statType = 0,
		element = 0,
		mpChange = 25,
		targetingTypeA = 1,
		basePowerA = 0.00,
		targetingTypeB = None,
		basePowerB = None,
		accuracyMod = 100,
		critChance = 0.00,
		randomMod = 0.00,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
	2: Skill(
		name = "Defend",
		skillType = 4,
		statType = 0,
		element = 0,
		mpChange = 0,
		targetingTypeA = 1,
		basePowerA = 0.00,
		targetingTypeB = None,
		basePowerB = None,
		accuracyMod = 100.00,
		critChance = 0.00,
		randomMod = 0.00,
		buffDebuff = None,
		statusEffect = 90,
		statusEffectDuration = 3
	),
	3: Skill(
		name = "Evade",
		skillType = 4,
		statType = 0,
		element = 0,
		mpChange = 0,
		targetingTypeA = 1,
		basePowerA = 0.00,
		targetingTypeB = None,
		basePowerB = None,
		accuracyMod = 100.00,
		critChance = 0.00,
		randomMod = 0.00,
		buffDebuff = None,
		statusEffect = 91,
		statusEffectDuration = 3
	),
	4: Skill(
		name = "Basic Attack A",
		skillType = 1,
		statType = 1,
		element = 1,
		mpChange = 10,
		targetingTypeA = 2,
		basePowerA = 1.00,
		targetingTypeB = None,
		basePowerB = None,
		accuracyMod = 1.00,
		critChance = 0.10,
		randomMod = 0.10,
		buffDebuff = Stats(hp = -50, every = 0),
		statusEffect = None,
		statusEffectDuration = 0
	),
	5: Skill(
		name = "Basic Attack B",
		skillType = 1,
		statType = 1,
		element = 1,
		mpChange = -10,
		targetingTypeA = 2,
		basePowerA = 1.50,
		targetingTypeB = 3,
		basePowerB = 0.75,
		accuracyMod = 1.00,
		critChance = 0.10,
		randomMod = 0.10,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
	6: Skill(
		name = "Basic Attack C",
		skillType = 1,
		statType = 2,
		element = 1,
		mpChange = 10,
		targetingTypeA = 2,
		basePowerA = 1.00,
		targetingTypeB = None,
		basePowerB = None,
		accuracyMod = 1.00,
		critChance = 0.10,
		randomMod = 0.10,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
	7: Skill(
		name = "Basic Attack D",
		skillType = 1,
		statType = 2,
		element = 1,
		mpChange = -10,
		targetingTypeA = 2,
		basePowerA = 1.50,
		targetingTypeB = 3,
		basePowerB = 0.75,
		accuracyMod = 1.00,
		critChance = 0.10,
		randomMod = 0.10,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
	8: Skill(
		name = "Self-heal",
		skillType = 2,
		statType = 2,
		element = 1,
		mpChange = 10,
		targetingTypeA = 1,
		basePowerA = 1.00,
		targetingTypeB = None,
		basePowerB = None,
		accuracyMod = 1.00,
		critChance = 0.00,
		randomMod = 0.10,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
	9: Skill(
		name = "Heal A",
		skillType = 2,
		statType = 2,
		element = 1,
		mpChange = 0,
		targetingTypeA = 4,
		basePowerA = 1.00,
		targetingTypeB = None,
		basePowerB = None,
		accuracyMod = 1.00,
		critChance = 0.00,
		randomMod = 0.10,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
	10: Skill(
		name = "Heal B",
		skillType = 2,
		statType = 2,
		element = 1,
		mpChange = -10,
		targetingTypeA = 4,
		basePowerA = 1.50,
		targetingTypeB = 5,
		basePowerB = 0.75,
		accuracyMod = 1.00,
		critChance = 0.00,
		randomMod = 0.10,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
	11: Skill(
		name = "Revive A",
		skillType = 3,
		statType = 2,
		element = 1,
		mpChange = -25,
		targetingTypeA = 6,
		basePowerA = 1.00,
		targetingTypeB = None,
		basePowerB = None,
		accuracyMod = 1.00,
		critChance = 0.00,
		randomMod = 0.10,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
	12: Skill(
		name = "Revive B",
		skillType = 3,
		statType = 2,
		element = 1,
		mpChange = -100,
		targetingTypeA = 6,
		basePowerA = 1.50,
		targetingTypeB = 7,
		basePowerB = 0.75,
		accuracyMod = 1.00,
		critChance = 0.00,
		randomMod = 0.10,
		buffDebuff = None,
		statusEffect = None,
		statusEffectDuration = 0
	),
}

# Contains the list for items.
itemsList = {
	0:Item("Lesser Health Potion",itemTypes[0],400,40,150),1:Item("Health Potion",itemTypes[0],2000,70,750),2:Item("Greater Health Potion",itemTypes[0],10000,100,3750),3:Item("Lesser Mana Potion",itemTypes[1],400,40,150),4:Item("Mana Potion",itemTypes[1],2000,70,750),5:Item("Greater Mana Potion",itemTypes[1],10000,100,3750)
}

# Contains the list for players.
playersList = {
	0: PlayerCharacter(),
	1: PlayerCharacter(
		name = "Monkey A",
		stats = Stats(550, 100, 55, 50, 55, 50, 20, 20),
		skills = [4, 5],
		inventory = "050100050100"
	),
	2: PlayerCharacter(
		name = "Monkey B",
		stats = Stats(450, 100, 50, 50, 50, 50, 25, 25),
		skills = [6, 7],
		inventory = "050100050100"
	),
	3: PlayerCharacter(
		name = "Monkey C",
		stats = Stats(500, 100, 50, 55, 50, 55, 20, 20),
		skills = [8, 9, 10, 11, 12],
		inventory = "050100050100"
	),
}

# Contains the list for enemies.
enemiesList = {
	0: EnemyCharacter(),
	1: EnemyCharacter(
		name = "Bloon A",
		stats = Stats(1500, 1, 50, 55, 50, 20, 20),
		skills = [4, 5]
	),
	2: EnemyCharacter(
		name = "Bloon B",
		stats = Stats(750, 1, 50, 50, 50, 25, 25),
		skills = [6, 7]
	),
	3: EnemyCharacter(
		name = "Bloon C",
		stats = Stats(1000, 1, 55, 50, 55, 20, 20),
		skills = [8, 9, 10]
	),
}

# Contains the list for inn actions.
innActions = [
	"Eat",
	"Dine",
	"Rest",
	"Meditate",
	"Nap",
	"Slumber"
]

# Contains the list for inn power modifiers.
innPowers = [
	50,
	100,
	50,
	100,
	50,
	100
]

# Contains the list for inn recovery resources.
innResources = [
	resources[4],
	resources[4],
	resources[5],
	resources[5],
	resources[6],
	resources[6]
]

# Contains the list for costs of inn actions.
innCosts = [
	0,
	0,
	0,
	0,
	0,
	0
]

# Render the main menu of the game. This menu should give the player the option to start a new game, load a saved game, and quit the game.
def renderMainMenu():
	inMainMenu = True

	while (inMainMenu):
		clearScreen()
		print("Title")
		print("–––––")
		print("1. New Game")
		# print("2. Load Game")
		print("9. Debug")
		print("`. Exit")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (userInput == 1):
					renderNewGameMenu()
				# elif (userInput == 2):
					# renderLoadGameMenu()
				elif (userInput == 9):
					renderDebugMenu()
			elif (userInput == "`"):
				inMainMenu = False
		except:
			continue


def renderDebugMenu():
	global skillsList

	currentLocation = "D:\MEGAsync Downloads\python rpg\python rpg.xlsx"
	currentWorkbook = openpyxl.load_workbook(filename = currentLocation, data_only = True)

	allPlayerNames = []
	for index in playersList:
		allPlayerNames.append(playersList[index][0])

	allEnemyNames = []
	for index in enemiesList:
		allEnemyNames.append(enemiesList[index][0])

	choice = -1

	while (choice != 0):
		clearScreen()
		print("Debug")
		print("-----")
		print("1. Update Skills List")
		print("0. Back")

		try:
			choice = int(input("> "))
			if (choice == 1):
				# print(skillsList[0])
				skillsList = {}

				currentSheet = currentWorkbook["SkillsList"]

				currentRow = 2
				while ((currentSheet.cell(currentRow, 2)).value != None):
					currentSkillID = int(currentSheet.cell(currentRow, 1).value)

					currentSkillForEntity = currentSheet.cell(currentRow, 2).value
					if (currentSkillForEntity in allPlayerNames):
						currentSkillForEntity = allPlayerNames.index(currentSkillForEntity)
					elif (currentSkillForEntity in allEnemyNames):
						currentSkillForEntity = allEnemyNames.index(currentSkillForEntity)
					else:
						currentSkillForEntity = 0

					currentSkillName = currentSheet.cell(currentRow, 3).value

					currentSkillMaxLevel = currentSheet.cell(currentRow, 4).value
					if (currentSkillMaxLevel != "–"):
						currentSkillMaxLevel = int(currentSkillMaxLevel)
					else:
						currentSkillMaxLevel = 0

					currentSkillType = currentSheet.cell(currentRow, 5).value
					for i in range(len(skillTypes)):
						if (currentSkillType == skillTypes[i]):
							currentSkillType = i
							break
						if (i == (len(skillTypes) - 1)):
							currentSkillType = 0
							break

					currentSkillStatType = currentSheet.cell(currentRow, 6).value
					for i in range(len(statTypes)):
						if (currentSkillStatType == statTypes[i]):
							currentSkillStatType = i
							break
						if (i == (len(statTypes) - 1)):
							currentSkillStatType = 0
							break

					currentSkillElement = currentSheet.cell(currentRow, 7).value
					for i in range(len(elements)):
						if (currentSkillElement == elements[i]):
							currentSkillElement = i
							break
						if (i == (len(elements) - 1)):
							currentSkillElement = 0
							break

					currentSkillCost = currentSheet.cell(currentRow, 8).value
					if (currentSkillCost != "–"):
						currentSkillCost = int(currentSkillCost)
					else:
						currentSkillCost = 0

					currentTargetingTypeA = currentSheet.cell(currentRow, 9).value
					validTargetingTypeA = False
					for i in range(len(targetingTypes)):
						if (currentTargetingTypeA == targetingTypes[i] and targetingTypes[i] != "–"):
							currentTargetingTypeA = i
							validTargetingTypeA = True
							break
					if (not validTargetingTypeA):
						currentTargetingTypeA = None

					currentTargetingTypeB = currentSheet.cell(currentRow, 10).value
					validTargetingTypeB = False
					for i in range(len(targetingTypes)):
						if (currentTargetingTypeB == targetingTypes[i] and targetingTypes[i] != "–"):
							currentTargetingTypeB = i
							validTargetingTypeB = True
							break
					if (not validTargetingTypeB):
						currentTargetingTypeB = None

					currentBasePowerA = currentSheet.cell(currentRow, 11).value
					if (type(currentBasePowerA) is int or type(currentBasePowerA) is float):
						currentBasePowerA = float("{:.2f}".format(currentBasePowerA))
					else:
						currentBasePowerA = None

					currentBasePowerB = currentSheet.cell(currentRow, 12).value
					if (type(currentBasePowerB) is int or type(currentBasePowerB) is float):
						currentBasePowerB = float("{:.2f}".format(currentBasePowerB))
					else:
						currentBasePowerB = None

					currentAccuracyMod = currentSheet.cell(currentRow, 13).value
					if (currentAccuracyMod != "–"):
						currentAccuracyMod = float("{:.2f}".format(currentAccuracyMod))
					else:
						currentAccuracyMod = 1.00

					currentCritChance = currentSheet.cell(currentRow, 14).value
					if (currentCritChance != "–"):
						currentCritChance = float("{:.2f}".format(currentCritChance))
					else:
						currentCritChance = 0.00

					currentRandomnessMod = currentSheet.cell(currentRow, 15).value
					if (currentRandomnessMod != "–"):
						currentRandomnessMod = float("{:.2f}".format(currentRandomnessMod))
					else:
						currentRandomnessMod = 0.10

					currentStatusEffect = currentSheet.cell(currentRow, 16).value
					if (currentStatusEffect in statusEffectsList):
						currentStatusEffect = str(statusEffectsList.index(currentStatusEffect))
					else:
						currentStatusEffect = None

					currentStatusEffectDuration = currentSheet.cell(currentRow, 17).value
					if (currentStatusEffectDuration != "–"):
						currentStatusEffectDuration = int(currentStatusEffectDuration)
					else:
						currentStatusEffectDuration = 0

					skillsList[currentSkillID] = [
						currentSkillForEntity,
						currentSkillName,
						currentSkillMaxLevel,
						currentSkillType,
						currentSkillStatType,
						currentSkillElement,
						currentSkillCost,
						currentTargetingTypeA,
						currentTargetingTypeB,
						currentBasePowerA,
						currentBasePowerB,
						currentAccuracyMod,
						currentCritChance,
						currentRandomnessMod,
						currentStatusEffect,
						currentStatusEffectDuration
					]

					currentRow += 1

				print(skillsList)
				input()
				choice = 0
		except ValueError:
			continue


# Render the menu for when the player starts a new game. This menu should allow the player to check out and customize their character (such as their name and class). This menu should also allow the player to officially start a new game.
def renderNewGameMenu():
	inNewGameMenu = True
	# selectedCharacters = [0, 0, 0]
	selectedCharacters = [1, 2, 3]

	while (inNewGameMenu):
		clearScreen()
		print("New Game")
		print("--------")
		print("1. " + playersList[selectedCharacters[0]].name) if selectedCharacters[0] != 0 else print("1. Empty Slot")
		print("2. " + playersList[selectedCharacters[1]].name) if selectedCharacters[1] != 0 else print("2. Empty Slot")
		print("3. " + playersList[selectedCharacters[2]].name) if selectedCharacters[2] != 0 else print("3. Empty Slot")
		if (not all(flag == 0 for flag in selectedCharacters)):
			print("Q. Start Game")
		print("`. Back")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (1 <= userInput <= 3):
					selectedCharacters[userInput - 1] = requestCharacterChange(selectedCharacters[userInput - 1], selectedCharacters)
			elif (userInput.lower() == "q" and not all(flag == 0 for flag in selectedCharacters)):
				for i in range(len(currentPlayers)):
					if (selectedCharacters[i] != 0):
						currentPlayers[i] = copy.deepcopy(playersList[selectedCharacters[i]])
						playersAlive[i] = True
						playersHaveMoved[i] = False
				startGame()
				inNewGameMenu = False
			elif (userInput == "`"):
				inNewGameMenu = False
		except:
			continue


# Render a menu that allows the player to change a character in the party.
def requestCharacterChange(currentCharacter, party):
	changingCharacter = True

	while (changingCharacter):
		clearScreen()
		print("Select Tower")
		print("-------------")
		print("Current Tower in Slot: " + str(playersList[currentCharacter].name))
		for key in playersList:
			if (key != 0):
				print(str(key) + ". " + str(playersList[key].name))
		print("Q. Deselect")
		print("`. Back")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (userInput != 0 and userInput in playersList):
					changingCharacter = False
			elif (userInput.lower() == "q"):
				userInput = 0
				changingCharacter = False
			elif (userInput == "`"):
				userInput = currentCharacter
				changingCharacter = False
		except:
			continue

	return userInput


# Handles what happens inbetween battles and towns.
def startGame():
	gameRegion = 1
	regionBattle = 1

	while (playersAlive.count(True) > 0):
		if (regionBattle % 11 == 0):
			gameRegion += 1
			regionBattle = 1
			clearScreen()
			proceduralPrint("You entered the " + str(regions[gameRegion % 3]) + ".", "")
		if (regionBattle % 5 == 0 or regionBattle % 5 == 1):
			clearScreen()
			proceduralPrint("You came across a town.", "")
			renderTownActionMenu()
		startBattle()
		regionBattle += 1


# Create an enemy character for the player to fight. Also handles the battle system as well.
def startBattle():
	global selectedPlayer
	global selectedEnemy

	# numOfEnemyCharacters = random.randint(1, 3)
	numOfEnemyCharacters = 2
	for i in range(numOfEnemyCharacters):
		currentEnemies[i] = copy.deepcopy(enemiesList[random.randint(1, 3)])
		enemiesAlive[i] = True
		enemiesHaveMoved[i] = False

	clearScreen()
	proceduralPrint("You encountered a group of enemies!", "")
	progressBattleTurn()

	# While both player characters and enemy characters are alive, run the battle sequence.
	while (playersAlive.count(True) > 0 and enemiesAlive.count(True) > 0):
		# Player turn on odd numbers.
		if (battleTurn % 2 == 1):
			# Select the next available player character.
			while (playersHaveMoved.count(True) != (len(currentPlayers) - currentPlayers.count(None)) and enemiesAlive.count(True) > 0):
				selectedPlayer = 0
				while (selectedPlayer < (len(currentPlayers) - currentPlayers.count(None))):
					if (playersHaveMoved[selectedPlayer] == True or playersHaveMoved[selectedPlayer] == None):
						selectedPlayer += 1
					else:
						break
				renderBattleActionMenu()
				evaluateCharacterHP()

		# Enemy turn on even numbers.
		elif (battleTurn % 2 == 0):
			# Select the next available enemy character.
			while (enemiesHaveMoved.count(True) != (len(currentEnemies) - currentEnemies.count(None)) and playersAlive.count(True) > 0):
				selectedEnemy = 0
				while (selectedEnemy < (len(currentEnemies) - currentEnemies.count(None))):
					if (enemiesHaveMoved[selectedEnemy] == True or enemiesHaveMoved[selectedEnemy] == None):
						selectedEnemy += 1
					else:
						break
				initiateEnemyAttack()
				evaluateCharacterHP()
		progressBattleTurn()

	finishBattle()


# Increment the turn in battle by 1.
def progressBattleTurn():
	global battleTurn
	global selectedPlayer
	global selectedEnemy
	global playersHaveMoved
	global enemiesHaveMoved

	battleTurn += 1

	# Enemy-to-player turn transition
	if (battleTurn % 2 == 1):
		selectedPlayer = 0
		selectedEnemy = -1

		for i in range(len(currentPlayers)):
			if (currentPlayers[i] != None):
				if (currentPlayers[i].buffsDebuffs.hp > 100):
					currentPlayers[i].buffsDebuffs.hp -= 5
				if (currentPlayers[i].buffsDebuffs.mp > 100):
					currentPlayers[i].buffsDebuffs.mp -= 5
				if (currentPlayers[i].buffsDebuffs.ballisticAttack > 100):
					currentPlayers[i].buffsDebuffs.ballisticAttack -= 5
				if (currentPlayers[i].buffsDebuffs.magicAttack > 100):
					currentPlayers[i].buffsDebuffs.magicAttack -= 5
				if (currentPlayers[i].buffsDebuffs.ballisticDefense > 100):
					currentPlayers[i].buffsDebuffs.ballisticDefense -= 5
				if (currentPlayers[i].buffsDebuffs.magicDefense > 100):
					currentPlayers[i].buffsDebuffs.magicDefense -= 5
				if (currentPlayers[i].buffsDebuffs.accuracy > 100):
					currentPlayers[i].buffsDebuffs.accuracy -= 5
				if (currentPlayers[i].buffsDebuffs.evade > 100):
					currentPlayers[i].buffsDebuffs.evade -= 5

		for i in range(len(currentEnemies)):
			if (currentEnemies[i] != None):
				if (currentEnemies[i].buffsDebuffs.hp < 100):
					currentEnemies[i].buffsDebuffs.hp += 5
				if (currentEnemies[i].buffsDebuffs.mp < 100):
					currentEnemies[i].buffsDebuffs.mp += 5
				if (currentEnemies[i].buffsDebuffs.ballisticAttack < 100):
					currentEnemies[i].buffsDebuffs.ballisticAttack += 5
				if (currentEnemies[i].buffsDebuffs.magicAttack < 100):
					currentEnemies[i].buffsDebuffs.magicAttack += 5
				if (currentEnemies[i].buffsDebuffs.ballisticDefense < 100):
					currentEnemies[i].buffsDebuffs.ballisticDefense += 5
				if (currentEnemies[i].buffsDebuffs.magicDefense < 100):
					currentEnemies[i].buffsDebuffs.magicDefense += 5
				if (currentEnemies[i].buffsDebuffs.accuracy < 100):
					currentEnemies[i].buffsDebuffs.accuracy += 5
				if (currentEnemies[i].buffsDebuffs.evade < 100):
					currentEnemies[i].buffsDebuffs.evade += 5

	# Player-to-enemy turn transition
	elif (battleTurn % 2 == 0):
		selectedPlayer = -1
		selectedEnemy = 0

		for i in range(len(currentPlayers)):
			if (currentPlayers[i] != None):
				if (currentPlayers[i].buffsDebuffs.hp < 100):
					currentPlayers[i].buffsDebuffs.hp += 5
				if (currentPlayers[i].buffsDebuffs.mp < 100):
					currentPlayers[i].buffsDebuffs.mp += 5
				if (currentPlayers[i].buffsDebuffs.ballisticAttack < 100):
					currentPlayers[i].buffsDebuffs.ballisticAttack += 5
				if (currentPlayers[i].buffsDebuffs.magicAttack < 100):
					currentPlayers[i].buffsDebuffs.magicAttack += 5
				if (currentPlayers[i].buffsDebuffs.ballisticDefense < 100):
					currentPlayers[i].buffsDebuffs.ballisticDefense += 5
				if (currentPlayers[i].buffsDebuffs.magicDefense < 100):
					currentPlayers[i].buffsDebuffs.magicDefense += 5
				if (currentPlayers[i].buffsDebuffs.accuracy < 100):
					currentPlayers[i].buffsDebuffs.accuracy += 5
				if (currentPlayers[i].buffsDebuffs.evade < 100):
					currentPlayers[i].buffsDebuffs.evade += 5

		for i in range(len(currentEnemies)):
			if (currentEnemies[i] != None):
				if (currentEnemies[i].buffsDebuffs.hp > 100):
					currentEnemies[i].buffsDebuffs.hp -= 5
				if (currentEnemies[i].buffsDebuffs.mp > 100):
					currentEnemies[i].buffsDebuffs.mp -= 5
				if (currentEnemies[i].buffsDebuffs.ballisticAttack > 100):
					currentEnemies[i].buffsDebuffs.ballisticAttack -= 5
				if (currentEnemies[i].buffsDebuffs.magicAttack > 100):
					currentEnemies[i].buffsDebuffs.magicAttack -= 5
				if (currentEnemies[i].buffsDebuffs.ballisticDefense > 100):
					currentEnemies[i].buffsDebuffs.ballisticDefense -= 5
				if (currentEnemies[i].buffsDebuffs.magicDefense > 100):
					currentEnemies[i].buffsDebuffs.magicDefense -= 5
				if (currentEnemies[i].buffsDebuffs.accuracy > 100):
					currentEnemies[i].buffsDebuffs.accuracy -= 5
				if (currentEnemies[i].buffsDebuffs.evade > 100):
					currentEnemies[i].buffsDebuffs.evade -= 5

	for i in range(len(playersHaveMoved)):
		if (playersAlive[i]):
			playersHaveMoved[i] = False
		elif (not playersAlive[i] and playersAlive[i] != None):
			playersHaveMoved[i] = True
	for i in range(len(enemiesHaveMoved)):
		if (enemiesAlive[i]):
			enemiesHaveMoved[i] = False
		elif (not enemiesAlive[i] and enemiesAlive[i] != None):
			enemiesHaveMoved[i] = True
		else:
			continue

	# for i in range(len(currentPlayers)):
	# 	if (currentPlayers[i] != None):
	# 		expiredPlayerStatusEffects = []
	# 		for j in range(len(currentPlayers[i].statusEffects)):
	# 			currentPlayers[i].statusEffectDurations[j] -= 1
	# 			if (currentPlayers[i].statusEffectDurations[j] == 0):
	# 				expiredPlayerStatusEffects.append(j)
	# 		expiredPlayerStatusEffects.reverse()
	# 		for j in expiredPlayerStatusEffects:
	# 			currentPlayers[i].statusEffects.pop(j)
	# 			currentPlayers[i].statusEffectDurations.pop(j)
	# 		currentPlayers[i].evaluateTotalStats()
	# 	else:
	# 		continue

	# for i in range(len(currentEnemies)):
	# 	if (currentEnemies[i] != None):
	# 		expiredEnemyStatusEffects = []
	# 		for j in range(len(currentEnemies[i].statusEffects)):
	# 			currentEnemies[i].statusEffectDurations[j] -= 1
	# 			if (currentEnemies[i].statusEffectDurations[j] == 0):
	# 				expiredEnemyStatusEffects.append(j)
	# 		expiredEnemyStatusEffects.reverse()
	# 		for j in expiredEnemyStatusEffects:
	# 			currentEnemies[i].statusEffects.pop(j)
	# 			currentEnemies[i].statusEffectDurations.pop(j)
	# 		currentEnemies[i].evaluateTotalStats()
	# 	else:
	# 		continue

	evaluateCharacterHP()


# Determines what happens when a battle is finished.
def finishBattle():
	global partyCurrentXP
	global partyMoney

	clearScreen()

	renderBattleStatusMenu()

	if (playersAlive.count(True) == 0):
		proceduralPrint("\nYour party was killed.", "")
	elif (enemiesAlive.count(True) == 0):
		proceduralPrint("\nYou've killed your enemies.", "")

		gainedXP = 0
		for i in range(len(currentEnemies)):
			if (currentEnemies[i] != None):
				gainedXP += round(partyNextXP * (1 + 0.5 * (currentEnemies[i].currentLevel - partyLevel)))
		partyCurrentXP += gainedXP
		proceduralPrint("\nYour party gained " + str(gainedXP) + " XP.", "")

		gainedMoney = 0
		for i in range(len(currentEnemies)):
			if (currentEnemies[i] != None):
				gainedMoney = round(100 * (1.05 ** currentEnemies[i].currentLevel))
		partyMoney += gainedMoney
		proceduralPrint("\nYour party gained $" + str(gainedMoney) + ".", "")

		checkForPartyLevelUp()


# Checks if the party has leveled up. If true, increase each party member's stats.
def checkForPartyLevelUp():
	global partyLevel
	global partyCurrentXP
	global partyNextXP
	global innCosts

	partyLeveledUp = False

	initialPartyLevel = partyLevel
	initialStats = []
	healthRatio = []
	manaRatio = []
	for i in range(len(currentPlayers)):
		if (currentPlayers[i] != None):
			initialStats.append(currentPlayers[i].totalStats)
			healthRatio.append(currentPlayers[i].curHP / currentPlayers[i].maxHP)
			manaRatio.append(currentPlayers[i].curMP / currentPlayers[i].maxMP)

	while (partyCurrentXP >= partyNextXP and partyLevel < maxPlayerLevel):
		partyLeveledUp = True
		partyLevel += 1
		partyCurrentXP -= partyNextXP
		partyNextXP *= 1.15
		for i in range(len(currentPlayers)):
			if (currentPlayers[i] != None):
				currentPlayers[i].leveledUpStats = Stats(
					round(currentPlayers[i].baseStats.hp * (1.05 ** (partyLevel - 1))),
					round(currentPlayers[i].baseStats.mp * (1.01 ** (partyLevel - 1))),
					round(currentPlayers[i].baseStats.ballisticAttack * (1.05 ** (partyLevel - 1))),
					round(currentPlayers[i].baseStats.magicAttack * (1.05 ** (partyLevel - 1))),
					round(currentPlayers[i].baseStats.ballisticDefense * (1.05 ** (partyLevel - 1))),
					round(currentPlayers[i].baseStats.magicDefense * (1.05 ** (partyLevel - 1))),
					round(currentPlayers[i].baseStats.accuracy * (1.05 ** (partyLevel - 1))),
					round(currentPlayers[i].baseStats.evade * (1.05 ** (partyLevel - 1)))
				)
				currentPlayers[i].evaluateTotalStats()

	innCosts = [
		100 * partyLevel,
		200 * partyLevel,
		100 * partyLevel,
		200 * partyLevel,
		200 * partyLevel,
		400 * partyLevel
	]

	newPartyLevel = partyLevel
	newStats = []
	for i in range(len(currentPlayers)):
		if (currentPlayers[i] != None):
			newStats.append(currentPlayers[i].totalStats)

	if (partyLeveledUp):
		changeInStats = []
		for i in range(len(currentPlayers)):
			if (currentPlayers[i] != None):
				changeInStats.append(newStats[i] - initialStats[i])
				currentPlayers[i].curHP = superRound(currentPlayers[i].maxHP * healthRatio[i], int)
				currentPlayers[i].curMP = superRound(currentPlayers[i].maxMP * manaRatio[i], int)

		print("\n+–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+")
		print(levelUpUIRow("Level Up! LVL " + str(initialPartyLevel) + " -> LVL " + str(newPartyLevel), 0))
		print("+–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+")
		for i in range(3):
			if (currentPlayers[i] != None):
				print(levelUpUIRow(str(currentPlayers[i].name), 0))
				print(levelUpUIRow("", 1))
				print(levelUpUIRow(initialStats[i], 2))
				print(levelUpUIRow(changeInStats[i], 3))
			else:
				print(levelUpUIRow("", 0))
				print(levelUpUIRow("", 0))
				print(levelUpUIRow("", 0))
				print(levelUpUIRow("", 0))

			if (i < 2):
				print("|\t––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\t|")
		print("+–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+")
		proceduralPrint("", "")


# Render a menu that prints out the status of players and enemies when in battle (such as level, HP, and MP).
def renderBattleStatusMenu():
	clearScreen()

	if (partyCurrentFocus >= partyMaxFocus):
		playerFocusBar = "❇  " + superRound(partyCurrentFocus, str) + " />> MAX " + generalUIBar(30, 0, ">", 1, 1)[8:32]
	else:
		playerFocusBar = "❇  " + superRound(partyCurrentFocus, str) + " " + generalUIBar(30, 0, ">", (partyCurrentFocus % 1), 1.00)
	playerProgressText = str(regions[gameRegion % 3]) + " \\ Battle " + str(regionBattle) + " \\ Turn " + str(battleTurn)

	allPlayerTexts = []
	allPlayerBars = []
	allEnemyTexts = []
	allEnemyBars = []
	for i in range(3):
		if (currentPlayers[i] != None):
			currentPlayerName = currentPlayers[i].name
			currentPlayerCurHP = currentPlayers[i].curHP
			currentPlayerCurMP = currentPlayers[i].curMP
			currentPlayerMaxHP = currentPlayers[i].maxHP
			currentPlayerMaxMP = currentPlayers[i].maxMP

			if (len(currentPlayerName) > 14):
				currentPlayerName = currentPlayerName[0:11] + "..."
			# currentPlayerText = "/ " + "{:<14}".format(str(currentPlayerName)) + " / HP " + "{:^4}".format(str(currentPlayerCurHP)) + " MP " + "{:^3}".format(str(currentPlayerCurMP)) + " /"
			currentPlayerText = "/ " + "{:<14}".format(str(currentPlayerName)) + " / ❤  " + "{:^4}".format(str(currentPlayerCurHP)) + " 🗲  " + "{:^3}".format(str(currentPlayerCurMP)) + " /"
			if (i == selectedPlayer):
				currentPlayerText = "> " + currentPlayerText
			else:
				currentPlayerText = "  " + currentPlayerText
			currentPlayerBar = generalUIBar(22, 0, "=", currentPlayerCurHP, currentPlayerMaxHP) + generalUIBar(10, 0, "—", currentPlayerCurMP, currentPlayerMaxMP)
		else:
			currentPlayerText = ""
			currentPlayerBar = ""

		if (currentEnemies[i] != None and enemiesAlive[i]):
			currentEnemyName = "LV " + str(currentEnemies[i].currentLevel) + " " + currentEnemies[i].name
			currentEnemyCurHP = currentEnemies[i].curHP
			currentEnemyMaxHP = currentEnemies[i].maxHP

			if (len(currentEnemyName) > 20):
				currentEnemyName = currentEnemyName[0:17] + "..."
			# currentEnemyText = "\\ HP " + "{:^5}".format(str(currentEnemyCurHP)) + " \\ " + "{:>20}".format(str(currentEnemyName)) + " \\"
			currentEnemyText = "\\ ❤  " + "{:^5}".format(str(currentEnemyCurHP)) + " \\ " + "{:>20}".format(str(currentEnemyName)) + " \\"
			if (i == selectedEnemy):
				currentEnemyText += " <"
			else:
				currentEnemyText += "  "
			currentEnemyBar = generalUIBar(34, 1, "=", currentEnemyCurHP, currentEnemyMaxHP)
		else:
			currentEnemyText = ""
			currentEnemyBar = ""

		allPlayerTexts.append(currentPlayerText)
		allPlayerBars.append(currentPlayerBar)
		allEnemyTexts.append(currentEnemyText)
		allEnemyBars.append(currentEnemyBar)

	print(battleUIRowDivider())

	print(battleUIRow(playerFocusBar, 0) + battleUIRow(playerProgressText, 1))

	print(battleUIRowDivider())

	print(battleUIRow(allPlayerTexts[0], 0) + battleUIRow(allEnemyTexts[0], 1))
	print(battleUIRow(allPlayerBars[0], 0) + battleUIRow(allEnemyBars[0], 1))
	# print("|\t–––––––––––––––––––––––––\t|\t–––––––––––––––––––––––––\t|")
	print(battleUIRow(allPlayerTexts[1], 0) + battleUIRow(allEnemyTexts[1], 1))
	print(battleUIRow(allPlayerBars[1], 0) + battleUIRow(allEnemyBars[1], 1))
	# print("|\t–––––––––––––––––––––––––\t|\t–––––––––––––––––––––––––\t|")
	print(battleUIRow(allPlayerTexts[2], 0) + battleUIRow(allEnemyTexts[2], 1))
	print(battleUIRow(allPlayerBars[2], 0) + battleUIRow(allEnemyBars[2], 1))

	print(battleUIRowDivider())
	print(str(currentEnemies[0].buffsDebuffs.hp) + "%", str(currentEnemies[0].maxHP) + " HP")
	print("|\t|\t|\t|\t|\t|\t|\t|\t|\t|\t|\t|")


# Render a menu that shows the player their general actions when in battle (such as use a skill or an item).
def renderBattleActionMenu():
	global selectedPlayer

	quickSwitchButtons = ["q", "w", "e"]

	while (playersHaveMoved[selectedPlayer] != True):
		renderBattleStatusMenu()

		print("\n" + str(currentPlayers[selectedPlayer].name))
		print("-" * len(currentPlayers[selectedPlayer].name))
		print("1. Attack")
		# print("1. Skills")
		print("2. Items")
		print("3. Scan")
		print("8. Defend")
		print("9. Evade")
		for i in range(len(currentPlayers)):
			if (not (selectedPlayer == i) and currentPlayers[i] != None and not playersHaveMoved[i]):
				print(quickSwitchButtons[i].upper() + ". Switch to " + currentPlayers[i].name)
		print("`. " + skillsList[1].name + " (+" + str(skillsList[1].mpChange) + " MP)")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (userInput == 1):
					renderAttackMenu()
				elif (userInput == 2):
					renderItemMenu()
				elif (userInput == 3):
					renderScanMenu()
				elif (userInput == 8):
					castSkill([currentPlayers[selectedPlayer]], currentPlayers[selectedPlayer], skillsList[2], 0)
				elif (userInput == 9):
					castSkill([currentPlayers[selectedPlayer]], currentPlayers[selectedPlayer], skillsList[3], 0)
			elif (userInput.lower() in quickSwitchButtons):
				for i in range(len(currentPlayers)):
					if (userInput.lower() == quickSwitchButtons[i] and not (selectedPlayer == i) and currentPlayers[i] != None and not playersHaveMoved[i]):
						selectedPlayer = i
						break
			elif (userInput == "`"):
				castSkill([currentPlayers[selectedPlayer]], currentPlayers[selectedPlayer], skillsList[1], 0)
		except:
			continue


# Render a menu that shows the player their available skills.
def renderAttackMenu():
	pickingSkill = True

	while (pickingSkill):
		renderBattleStatusMenu()

		print("\n" + currentPlayers[selectedPlayer].name + " > Attack")
		print("-" * len(currentPlayers[selectedPlayer].name) + "---------")
		for i in range(len(currentPlayers[selectedPlayer].skills)):
			count = i + 1
			currentSkill = skillsList[currentPlayers[selectedPlayer].skills[i]]

			currentSkillResource = currentPlayers[selectedPlayer].maxMP

			currentSkillMPChange = currentSkill.mpChange

			if (currentSkill == skillsList[0]):
				continue
			elif (currentSkill.mpChange < 0):
				print(str(count) + ". " + currentSkill.name + " (" + str(currentSkillMPChange) + " MP)")
			else:
				print(str(count) + ". " + currentSkill.name + " (+" + str(currentSkillMPChange) + " MP)")
		print("`. Back")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (1 <= userInput <= len(currentPlayers[selectedPlayer].skills) and currentPlayers[selectedPlayer].skills[userInput - 1] != skillsList[0]):
					userInput -= 1
					chosenSkill = skillsList[currentPlayers[selectedPlayer].skills[userInput]]

					currentPlayerResource = currentPlayers[selectedPlayer].curMP
					chosenSkillResource = currentPlayers[selectedPlayer].maxMP

					chosenSkillMPChange = chosenSkill.mpChange

					if (currentPlayerResource == currentPlayers[selectedPlayer].curMP and currentPlayerResource + chosenSkillMPChange >= 0):
						renderAttackDetails(chosenSkill)
						if (playersHaveMoved[selectedPlayer]):
							pickingSkill = False
			elif (userInput == "`"):
				pickingSkill = False
		except:
			continue


# Render a menu that shows the player more details about the skill they just selected when in battle.
def renderAttackDetails(skill):
	viewingSkillDetails = True

	while (viewingSkillDetails):
		renderBattleStatusMenu()

		print("\n" + currentPlayers[selectedPlayer].name + " > Attack > Targeting")
		print("-" * len(currentPlayers[selectedPlayer].name) + "---------------------")
		print(skill)

		hasAvailableTarget = False

		targetAButtons = ["1", "2", "3"]
		if (skill.targetingTypeA == targetingTypes[1]):
			print(targetAButtons[0].upper() + ". " + targetingTypes[1])
			hasAvailableTarget = True

		elif (skill.targetingTypeA == targetingTypes[2]):
			for i in range(len(currentEnemies) - enemiesAlive.count(None)):
				if (enemiesAlive[i]):
					print(targetAButtons[i].upper() + ". " + currentEnemies[i].name)
					hasAvailableTarget = True

		elif (skill.targetingTypeA == targetingTypes[3]):
			print(targetAButtons[0].upper() + ". " + targetingTypes[3])
			hasAvailableTarget = True

		elif (skill.targetingTypeA == targetingTypes[4]):
			for i in range(len(currentPlayers) - playersAlive.count(None)):
				if (playersAlive[i]):
					print(targetAButtons[i].upper() + ". " + currentPlayers[i].name)
					hasAvailableTarget = True

		elif (skill.targetingTypeA == targetingTypes[5]):
			print(targetAButtons[0].upper() + ". " + targetingTypes[5])
			hasAvailableTarget = True

		elif (skill.targetingTypeA == targetingTypes[6]):
			for i in range(len(currentPlayers) - playersAlive.count(None)):
				if (not playersAlive[i]):
					print(targetAButtons[i].upper() + ". " + currentPlayers[i].name)
					hasAvailableTarget = True

		elif (skill.targetingTypeA == targetingTypes[7]):
			if (playersAlive.count(False) >= 1):
				print(targetAButtons[0].upper() + ". " + targetingTypes[7])
				hasAvailableTarget = True

		targetBButtons = ["q", "w", "e"]
		if (skill.targetingTypeB == targetingTypes[1]):
			print(targetBButtons[0].upper() + ". " + targetingTypes[1])
			hasAvailableTarget = True

		elif (skill.targetingTypeB == targetingTypes[2]):
			for i in range(len(currentEnemies) - enemiesAlive.count(None)):
				if (enemiesAlive[i]):
					print(targetBButtons[i].upper() + ". " + currentEnemies[i].name)
					hasAvailableTarget = True

		elif (skill.targetingTypeB == targetingTypes[3]):
			print(targetBButtons[0].upper() + ". " + targetingTypes[3])
			hasAvailableTarget = True

		elif (skill.targetingTypeB == targetingTypes[4]):
			for i in range(len(currentPlayers) - playersAlive.count(None)):
				if (playersAlive[i]):
					print(targetBButtons[i].upper() + ". " + currentPlayers[i].name)
					hasAvailableTarget = True

		elif (skill.targetingTypeB == targetingTypes[5]):
			print(targetBButtons[0].upper() + ". " + targetingTypes[5])
			hasAvailableTarget = True

		elif (skill.targetingTypeB == targetingTypes[6]):
			for i in range(len(currentPlayers) - playersAlive.count(None)):
				if (not playersAlive[i]):
					print(targetBButtons[i].upper() + ". " + currentPlayers[i].name)
					hasAvailableTarget = True

		elif (skill.targetingTypeB == targetingTypes[7]):
			if (playersAlive.count(False) >= 1):
				print(targetBButtons[0].upper() + ". " + targetingTypes[7])
				hasAvailableTarget = True

		if (not hasAvailableTarget):
			print("No targets available.")

		print("`. Cancel")

		try:
			userInput = input("> ")
			if (userInput in targetAButtons or userInput in targetBButtons):
				if (userInput in targetAButtons and skill.targetingTypeA != None):
					skillVersion = 0

					if (skill.targetingTypeA == targetingTypes[1]):
						if (userInput == targetAButtons[0]):
							userInput = targetAButtons.index(userInput)
							chosenTarget = [currentPlayers[selectedPlayer]]

					elif (skill.targetingTypeA == targetingTypes[2]):
						userInput = targetAButtons.index(userInput)
						if (enemiesAlive[userInput]):
							chosenTarget = [currentEnemies[userInput]]

					elif (skill.targetingTypeA == targetingTypes[3]):
						if (userInput == targetAButtons[0]):
							userInput = targetAButtons.index(userInput)
							chosenTarget = []
							for i in range(len(currentEnemies)):
								if (enemiesAlive[i] and currentEnemies[i] != None):
									chosenTarget.append(currentEnemies[i])

					elif (skill.targetingTypeA == targetingTypes[4]):
						userInput = targetAButtons.index(userInput)
						if (playersAlive[userInput]):
							chosenTarget = [currentPlayers[userInput]]

					elif (skill.targetingTypeA == targetingTypes[5]):
						if (userInput == targetAButtons[0]):
							userInput = targetAButtons.index(userInput)
							chosenTarget = []
							for i in range(len(currentPlayers)):
								if (playersAlive[i] and currentPlayers[i] != None):
									chosenTarget.append(currentPlayers[i])

					elif (skill.targetingTypeA == targetingTypes[6]):
						userInput = targetAButtons.index(userInput)
						if (not playersAlive[userInput]):
							chosenTarget = [currentPlayers[userInput]]

					elif (skill.targetingTypeA == targetingTypes[7]):
						if (userInput == targetAButtons[0]):
							userInput = targetAButtons.index(userInput)
							if (playersAlive.count(False) >= 1):
								chosenTarget = []
								for i in range(len(currentPlayers)):
									if (not playersAlive[i] and currentPlayers[i] != None):
										chosenTarget.append(currentPlayers[i])

					else:
						chosenTarget = []

				elif (userInput in targetBButtons and skill.targetingTypeB != None):
					skillVersion = 1

					if (skill.targetingTypeB == targetingTypes[1]):
						if (userInput == targetBButtons[0]):
							userInput = targetBButtons.index(userInput)
							chosenTarget = [currentPlayers[selectedPlayer]]

					elif (skill.targetingTypeB == targetingTypes[2]):
						userInput = targetBButtons.index(userInput)
						if (enemiesAlive[userInput]):
							chosenTarget = [currentEnemies[userInput]]

					elif (skill.targetingTypeB == targetingTypes[3]):
						if (userInput == targetBButtons[0]):
							userInput = targetBButtons.index(userInput)
							chosenTarget = []
							for i in range(len(currentEnemies)):
								if (enemiesAlive[i] and currentEnemies[i] != None):
									chosenTarget.append(currentEnemies[i])

					elif (skill.targetingTypeB == targetingTypes[4]):
						userInput = targetBButtons.index(userInput)
						if (playersAlive[userInput]):
							chosenTarget = [currentPlayers[userInput]]

					elif (skill.targetingTypeB == targetingTypes[5]):
						if (userInput == targetBButtons[0]):
							userInput = targetBButtons.index(userInput)
							chosenTarget = []
							for i in range(len(currentPlayers)):
								if (playersAlive[i] and currentPlayers[i] != None):
									chosenTarget.append(currentPlayers[i])

					elif (skill.targetingTypeB == targetingTypes[6]):
						userInput = targetBButtons.index(userInput)
						if (not playersAlive[userInput]):
							chosenTarget = [currentPlayers[userInput]]

					elif (skill.targetingTypeB == targetingTypes[7]):
						if (userInput == targetBButtons[0]):
							userInput = targetBButtons.index(userInput)
							if (playersAlive.count(False) >= 1):
								chosenTarget = []
								for i in range(len(currentPlayers)):
									if (not playersAlive[i] and currentPlayers[i] != None):
										chosenTarget.append(currentPlayers[i])

					else:
						chosenTarget = []

				castSkill(chosenTarget, currentPlayers[selectedPlayer], skill, skillVersion)
				viewingSkillDetails = False

			elif (userInput == "`"):
				viewingSkillDetails = False
		except:
			continue


# Render a menu that shows the player all the items.
def renderItemMenu():
	pickingItem = True

	while (pickingItem):
		renderBattleStatusMenu()

		print("\n" + currentPlayers[selectedPlayer].name + " > Items")
		print("-" * len(currentPlayers[selectedPlayer].name) + "--------")
		for i in range(len(itemsList)):
			currentItemAmount = currentPlayers[selectedPlayer].itemInventory[i]
			if (currentItemAmount > 0):
				print(str(i + 1) + ". ", end="")
				print(itemsList[i].name + " (" + str(currentItemAmount) + ")")
		print("`. Back")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (1 <= userInput <= len(itemsList) and sum(currentPlayers[selectedPlayer].itemInventory) > 0):
					userInput -= 1
					chosenItemAmount = currentPlayers[selectedPlayer].itemInventory[userInput]

					if (chosenItemAmount > 0):
						renderItemDetails(userInput)
						if (playersHaveMoved[selectedPlayer]):
							pickingItem = False
			elif (userInput == "`"):
				pickingItem = False
		except:
			continue


# Render a menu that shows the player more details about the item they just selected when in battle.
def renderItemDetails(itemIndex):
	viewingItemDetails = True
	chosenItem = itemsList[itemIndex]

	while (viewingItemDetails):
		renderBattleStatusMenu()

		print("\n" + currentPlayers[selectedPlayer].name + " > Items > Use")
		print("-" * len(currentPlayers[selectedPlayer].name) + "--------------")
		print(chosenItem)
		print("1. Confirm")
		print("`. Back")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (userInput == 1):
					useItem(currentPlayers[selectedPlayer], currentPlayers[selectedPlayer], itemIndex)
					viewingItemDetails = False
			elif (userInput == "`"):
				viewingItemDetails = False
		except:
			continue


# Render a menu that shows the player who they can scan.
def renderScanMenu():
	scanningCharacters = True

	while (scanningCharacters):
		renderBattleStatusMenu()
		print("\n" + currentPlayers[selectedPlayer].name + " > Scan")
		print("-" * len(currentPlayers[selectedPlayer].name) + "-------")
		print("1. " + str(currentPlayers[0].name))
		print("2. " + str(currentEnemies[0].name))
		print("`. Back")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (userInput == 1):
					renderPlayerScanMenu()
				elif (userInput == 2):
					print(currentEnemies[0])
			elif (userInput == "`"):
				scanningCharacters = False
		except:
			continue


# Render a menu that allows the player to scan themselves.
def renderPlayerScanMenu():
	scanningPlayerCharacter = True

	while (scanningPlayerCharacter):
		renderBattleStatusMenu()

		print("\n" + currentPlayers[selectedPlayer].name + " > Scan > " + currentPlayers[selectedPlayer].name)
		print("-" * len(currentPlayers[selectedPlayer].name) + "----------" + "-" * len(currentPlayers[selectedPlayer].name))
		print("1. Base Stats")
		print("2. Status Effects")
		print("`. Back")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (userInput == 1):
					proceduralPrint("\nBase Stats\n" + str(currentPlayers[0].baseStats), "\n")
					scanningPlayerCharacter = False
				elif (userInput == 2):
					statusEffectsString = ""
					if (len(currentPlayers[0].statusEffects) > 0):
						for i in range(len(currentPlayers[0].statusEffects)):
							statusEffectsString += "\n" + str(currentPlayers[0].statusEffects[i]) + " (" + str(currentPlayers[0].statusEffectDurations[i]) + ")"
							# statusEffectsString += str(currentPlayers[0].statusEffects[i])
							# statusEffectsString += " ("
							# statusEffectsString += str(currentPlayers[0].statusEffectDurations[i])
							# statusEffectsString += ")"
					else:
						statusEffectsString = "\nN/A"

					proceduralPrint(statusEffectsString, "\n")
					scanningPlayerCharacter = False
		except:
			continue


# Have the enemy perform an action, such as casting a skill or using an item.
def initiateEnemyAttack():
	global currentPlayers
	global currentEnemies

	renderBattleStatusMenu()

	possibleSkills = []
	for i in range(len(currentEnemies[selectedEnemy].skills)):
		possibleSkill = skillsList[currentEnemies[selectedEnemy].skills[i]]
		if (possibleSkill.name != "Empty" and possibleSkill.name != "Struggle"):
			possibleSkills.append(possibleSkill)

	# if (len(possibleSkills) == 0):
	# 	for currentKey in skillsList:
	# 		if (skillsList[currentKey].name == "Struggle"):
	# 			possibleSkills.append(str(skillsList[currentKey]))
	# 			break

	randomSkill = random.choice(possibleSkills)
	if (randomSkill.targetingTypeA == targetingTypes[1]):
		castSkill([currentEnemies[selectedEnemy]], currentEnemies[selectedEnemy], randomSkill, 0)

	elif (randomSkill.targetingTypeA == targetingTypes[2]):
		availableTargets = []
		for i in range(len(playersAlive)):
			if (playersAlive[i]):
				availableTargets.append(currentPlayers[i])
		randomTarget = random.choice(availableTargets)
		castSkill([randomTarget], currentEnemies[selectedEnemy], randomSkill, 0)

	elif (randomSkill.targetingTypeA == targetingTypes[3]):
		availableTargets = []
		for i in range(len(currentPlayers)):
			if (playersAlive[i] and currentPlayers[i] != None):
				availableTargets.append(currentPlayers[i])
		castSkill(availableTargets, currentEnemies[selectedEnemy], randomSkill, 0)

	elif (randomSkill.targetingTypeA == targetingTypes[4]):
		availableTargets = []
		for i in range(len(enemiesAlive)):
			if (enemiesAlive[i]):
				availableTargets.append(currentEnemies[i])
		randomTarget = random.choice(availableTargets)
		castSkill([randomTarget], currentEnemies[selectedEnemy], randomSkill, 0)

	elif (randomSkill.targetingTypeA == targetingTypes[5]):
		availableTargets = []
		for i in range(len(currentEnemies)):
			if (enemiesAlive[i] and currentEnemies[i] != None):
				availableTargets.append(currentEnemies[i])
		castSkill(availableTargets, currentEnemies[selectedEnemy], randomSkill, 0)

	else:
		castSkill([currentEnemies[selectedEnemy]], currentEnemies[selectedEnemy], randomSkill, 0)


# Check the status of all players and enemies.
def evaluateCharacterHP():
	global currentPlayers
	global currentEnemies
	global playersAlive
	global enemiesAlive

	for i in range(len(currentPlayers)):
		if (currentPlayers[i] != None):
			playersAlive[i] = currentPlayers[i].curHP > 0
	for i in range(len(currentEnemies)):
		if (currentEnemies[i] != None):
			enemiesAlive[i] = currentEnemies[i].curHP > 0


# Render a menu that prints out the status of the player when in town (such as level, HP, MP, and money).
def renderTownStatusMenu():
	clearScreen()
	print("+–––––––––––––––––––––––––––––––––––––––+")
	print("| " + str(regions[gameRegion % 3]) + " | Town")
	print("+–––––––––––––––––––––––––––––––––––––––+")
	print("| " + str(currentPlayers[0].name) + " | LV " + str(partyLevel))
	print("| HP | " + str(currentPlayers[0].curHP) + "/" + str(currentPlayers[0].maxHP))
	print("| MP | " + str(currentPlayers[0].curMP) + "/" + str(currentPlayers[0].maxMP))
	print("| $$ | " + str(partyMoney))
	print("+–––––––––––––––––––––––––––––––––––––––+")


# Render a menu that shows the player their general actions when in town (go to the shop or enter the inn).
def renderTownActionMenu():
	inTownMenu = True

	while (inTownMenu):
		renderTownStatusMenu()

		print("\nTown")
		print("----")
		print("1. Shop")
		print("2. Inn")
		# print("9. Save Game")
		print("`. Leave")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				if (userInput == 1):
					renderShopMenu()
				elif (userInput == 2):
					renderInnMenu()
			elif (userInput == "`"):
				inTownMenu = False
		except:
			continue


# Render a menu that shows the player the shop in town.
def renderShopMenu():
	inShop = True

	while (inShop):
		renderTownStatusMenu()

		print("\nTown > Shop")
		print("-----------")
		for i in range(len(currentPlayers[0].itemInventory)):
			currentItemAmount = currentPlayers[0].itemInventory[i]
			print(str(i + 1) + ". ", end="")
			print(itemsList[i].name + " (" + str(currentItemAmount) + ") ($" + str(itemsList[i].value) + ")")
		print("`. Leave")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (1 <= userInput <= len(itemsList)):
					userInput -= 1
					chosenItemAmount = currentPlayers[0].itemInventory[userInput]

					if (chosenItemAmount > 0):
						renderShopDetails(userInput)
			elif (userInput == "`"):
				inShop = False
		except:
			continue


# Render a menu that shows the player more details about the item they just selected when in town.
def renderShopDetails(itemIndex):
	viewingItemDetails = True
	chosenItem = itemsList[itemIndex]

	while (viewingItemDetails):
		renderTownStatusMenu()

		print("\nTown > Shop > Item Details")
		print("--------------------------")
		print(chosenItem)
		print(">0. Buy current item at 100% value")
		print("<0. Sell current item at 20% value")
		print("`. Back")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (userInput > 0):
					totalCost = chosenItem.value * userInput
					if (partyMoney >= totalCost):
						partyMoney -= totalCost
						currentPlayers[0].itemInventory[itemIndex] += userInput
						if (userInput == 1):
							proceduralPrint("\n" + str(currentPlayers[0].name) + " spent $" + str(totalCost) + " to buy 1 " + str(chosenItem.name) + ".", "")
						else:
							proceduralPrint("\n" + str(currentPlayers[0].name) + " spent $" + str(totalCost) + " to buy " + str(userInput) + " " + str(chosenItem.name) + "s.", "")
						viewingItemDetails = False
				elif (userInput < 0):
					userInput = abs(userInput)
					if (currentPlayers[0].itemInventory[itemIndex] >= userInput):
						totalProfit = (chosenItem.value * (20/100)) * userInput
						totalProfit = superRound(totalProfit, int)
						partyMoney += totalProfit
						currentPlayers[0].itemInventory[itemIndex] -= userInput
						if (userInput == 1):
							proceduralPrint("\n" + str(currentPlayers[0].name) + " sold 1 " + str(chosenItem.name) + " for $" + str(totalProfit) + ".", "")
						else:
							proceduralPrint("\n" + str(currentPlayers[0].name) + " sold " + str(userInput) + " " + str(chosenItem.name) + "s for $" + str(totalProfit) + ".", "")
						viewingItemDetails = False
			elif (userInput == "`"):
				viewingItemDetails = False
		except:
			continue


# Render a menu that shows the player the inn in town.
def renderInnMenu():
	inInn = True

	while (inInn):
		renderTownStatusMenu()

		print("\nTown > Inn")
		print("----------")
		print("1. " + str(innActions[0]) + " (50% HP) ($" + str(innCosts[0]) + ")")
		print("2. " + str(innActions[1]) + " (100% HP) ($" + str(innCosts[1]) + ")")
		print("3. " + str(innActions[2]) + " (50% MP) ($" + str(innCosts[2]) + ")")
		print("4. " + str(innActions[3]) + " (100% MP) ($" + str(innCosts[3]) + ")")
		print("5. " + str(innActions[4]) + " (50% HP/MP) ($" + str(innCosts[4]) + ")")
		print("6. " + str(innActions[5]) + " (100% HP/MP) ($" + str(innCosts[5]) + ")")
		print("`. Leave")

		try:
			userInput = input("> ")
			if (userInput.isdecimal()):
				userInput = int(userInput)
				if (1 <= userInput <= 6):
					userInput -= 1
					chosenInnCosts = innCosts[userInput]

					if (partyMoney >= chosenInnCosts):
						renderInnDetails(userInput)
						inInn = False
			elif (userInput == "`"):
				inInn = False
		except:
			continue


# Render a menu that shows the player more details about the inn action they just selected when in town.
def renderInnDetails(action):
	viewingActionDetails = True

	while (viewingActionDetails):
		renderTownStatusMenu()
		print("\nTown > Inn > Action Details")
		print("---------------------------")
		print("+–––––––+–––––––––––––––––––––––––––––––+")
		print("|Action\t| " + str(innActions[action]))
		print("|Power\t| " + str(innPowers[action]) + str(innResources[action]))
		print("|Cost\t| " + str(innCosts[action]))
		print("+–––––––+–––––––––––––––––––––––––––––––+")
		print("\n1. Confirm")
		print("`. Cancel")

		try:
			userInput = int(input("> "))
			if (userInput.isdecimal()):
				if (userInput == 1):
					chosenInnPower = innPowers[action]
					chosenInnResource = innResources[action]
					chosenInnCosts = innCosts[action]

					partyMoney -= chosenInnCosts

					if (chosenInnResource in flatResources):
						currentHPRecovery = superRound(chosenInnPower, int)
						currentMPRecovery = superRound(chosenInnPower, int)
					elif (chosenInnResource in percentageResources):
						currentHPRecovery = currentPlayers[0].maxHP * (chosenInnPower / 100)
						currentMPRecovery = currentPlayers[0].maxMP * (chosenInnPower / 100)
						currentHPRecovery = superRound(currentHPRecovery, int)
						currentMPRecovery = superRound(currentMPRecovery, int)
					else:
						currentHPRecovery = superRound(chosenInnPower, int)
						currentMPRecovery = superRound(chosenInnPower, int)

					if (chosenInnResource == resources[1] or chosenInnResource == resources[4]):
						currentPlayers[0].curHP += currentHPRecovery
						currentPlayers[0].evaluateCurrentPoints()

						proceduralPrint("\n" + str(currentPlayers[0].name) + " has recovered " + str(currentHPRecovery) + " HP.", "")
						viewingActionDetails = False
					elif (chosenInnResource == resources[2] or chosenInnResource == resources[5]):
						currentPlayers[0].curMP += currentMPRecovery
						currentPlayers[0].evaluateCurrentPoints()

						proceduralPrint("\n" + str(currentPlayers[0].name) + " has recovered " + str(currentMPRecovery) + " MP.", "")
						viewingActionDetails = False
					elif (chosenInnResource == resources[3] or chosenInnResource == resources[6]):
						currentPlayers[0].curHP += currentHPRecovery
						currentPlayers[0].curMP += currentMPRecovery
						currentPlayers[0].evaluateCurrentPoints()

						proceduralPrint("\n" + str(currentPlayers[0].name) + " has recovered " + str(currentHPRecovery) + " HP and " + str(currentMPRecovery) + " MP.", "")
						viewingActionDetails = False
			elif (userInput == "`"):
				viewingActionDetails = False
		except:
			continue


# The user applies a specified status effect onto the target for a specified amount of turns.
def applyStatusEffect(target, user, statusEffect, statusEffectDuration):
	for i in range(len(target)):
		# If the target already has the status effect, reset the duration.
		if (statusEffect in target[i].statusEffects):
			statusEffectIndex = target[i].statusEffects.index(statusEffect)
			target[i].statusEffectDurations[statusEffectIndex] = statusEffectDuration + 1

		# Otherwise, the status effect is applied onto the target.
		else:
			target[i].statusEffects.append(statusEffect)
			target[i].statusEffectDurations.append(statusEffectDuration + 1)
		target[i].evaluateTotalStats()

		proceduralPrint(str(target[i].name) + " received " + str(statusEffect.name) + ".", "")


# The user casts a specified skill onto the target.
def castSkill(target, user, skill, version):
	global battleTurn
	global playersHaveMoved
	global enemiesHaveMoved

	clearScreen()
	renderBattleStatusMenu()

	# Get user text for strings
	userName = user.name
	targetName = []
	for i in range(len(target)):
		targetName.append(target[i].name)

	if (type(user) is PlayerCharacter):
		skillMPChange = skill.mpChange
		user.curMP += skillMPChange

	if (version == 0):
		skillPower = skill.basePowerA
	elif (version == 1):
		skillPower = skill.basePowerB
	else:
		skillPower = 1

	userAccuracyStat = user.totalStats.accuracy
	targetEvadeStat = []
	for i in range(len(target)):
		targetEvadeStat.append(target[i].totalStats.evade)

	proceduralPrint("\n" + userName + " casted " + skill.name + ".", "")

	if (skill.skillType == skillTypes[1]):
		damageMod = 1

		userAttackStat = None
		targetDefenseStat = []

		if (skill.statType == statTypes[1]):
			userAttackStat = user.totalStats.ballisticAttack
			for i in range(len(target)):
				targetDefenseStat.append(target[i].totalStats.ballisticDefense)
		elif (skill.statType == statTypes[2]):
			userAttackStat = user.totalStats.magicAttack
			for i in range(len(target)):
				targetDefenseStat.append(target[i].totalStats.magicDefense)
		else:
			userAttackStat = 1
			for i in range(len(target)):
				targetDefenseStat.append(1)

		totalPotentialDamage = []
		totalHitRequirement = []
		totalCritRequirement = []
		for i in range(len(target)):
			currentPotentialDamage = math.ceil(4 * (userAttackStat ** 2) / (userAttackStat + targetDefenseStat[i]) * skillPower)
			if (currentPotentialDamage <= 0):
				currentPotentialDamage = 1
			totalPotentialDamage.append(currentPotentialDamage)

			hitRequirement = random.randint(0, 99)
			totalHitRequirement.append(hitRequirement)

			critRequirement = random.randint(0, 99)
			totalCritRequirement.append(critRequirement)

		currentAccuracy = []
		for i in range(len(target)):
			currentAccuracy.append(userAccuracyStat / targetEvadeStat[i] * skill.accuracyMod * 100)

		criticalAccuracy = []
		for i in range(len(target)):
			criticalAccuracy.append(skill.critChance * 100)

		totalDealtDamage = []
		for i in range(len(target)):
			currentDamage = round(totalPotentialDamage[i] * random.uniform((1.00 - (skill.randomMod / 2)), (1.00 + (skill.randomMod / 2))))

			if (currentAccuracy[i] > totalHitRequirement[i]):
				if (criticalAccuracy[i] > totalCritRequirement[i]):
					currentDamage = round(currentDamage * 1.5)
					criticalString = " critical"
				else:
					criticalString = ""

				target[i].curHP -= currentDamage

				totalDealtDamage.append(currentDamage)
			else:
				totalDealtDamage.append(None)

		for i in range(len(target)):
			if (totalDealtDamage[i] != None):
				if (i == 0 and len(target) == 1):
					proceduralPrint(str(userName) + " dealt " + str(totalDealtDamage[i]) + str(criticalString) + " damage to " + str(targetName[i]) + ".", "")
				elif (i == 0 and len(target) > 1):
					print(str(userName) + " dealt " + str(totalDealtDamage[i]) + str(criticalString) + " damage to " + str(targetName[i]) + ",")
				elif (i > 0 and i < (len(target) - 1)):
					print((" " * len(userName)) + " dealt " + str(totalDealtDamage[i]) + str(criticalString) + " damage to " + str(targetName[i]) + ",")
				else:
					proceduralPrint((" " * len(userName)) + " dealt " + str(totalDealtDamage[i]) + str(criticalString) + " damage to " + str(targetName[i]) + ".", "")

				if (skill.buffDebuff != None):
					# target[i].buffsDebuffs += skill.buffDebuff
					target[i].buffsDebuffs.hp = min(max(target[i].buffsDebuffs.hp + skill.buffDebuff.hp, 50), 200)
					target[i].buffsDebuffs.mp = min(max(target[i].buffsDebuffs.mp + skill.buffDebuff.mp, 50), 200)
					target[i].buffsDebuffs.ballisticAttack = min(max(target[i].buffsDebuffs.ballisticAttack + skill.buffDebuff.ballisticAttack, 50), 200)
					target[i].buffsDebuffs.magicAttack = min(max(target[i].buffsDebuffs.magicAttack + skill.buffDebuff.magicAttack, 50), 200)
					target[i].buffsDebuffs.ballisticDefense = min(max(target[i].buffsDebuffs.ballisticDefense + skill.buffDebuff.ballisticDefense, 50), 200)
					target[i].buffsDebuffs.magicDefense = min(max(target[i].buffsDebuffs.magicDefense + skill.buffDebuff.magicDefense, 50), 200)
					target[i].buffsDebuffs.accuracy = min(max(target[i].buffsDebuffs.accuracy + skill.buffDebuff.hp, 50), 200)
					target[i].buffsDebuffs.evade = min(max(target[i].buffsDebuffs.evade + skill.buffDebuff.evade, 50), 200)
				if (skill.statusEffect != None):
					applyStatusEffect(target[i], user, skill.statusEffect, skill.statusEffectDuration)
				target[i].evaluateTotalStats()
			else:
				if (i == 0 and len(target) == 1):
					proceduralPrint(str(userName) + " missed their attack on " + str(targetName[i]) + ".", "")
				elif (i == 0 and len(target) > 1):
					print(str(userName) + " missed their attack on " + str(targetName[i]) + ",")
				elif (i > 0 and i < (len(target) - 1)):
					print((" " * len(userName)) + " missed their attack on " + str(targetName[i]) + ",")
				else:
					proceduralPrint((" " * len(userName)) + " missed their attack on " + str(targetName[i]) + ".", "")

	elif (skill.skillType == skillTypes[2]):
		if (skill.statType == statTypes[1]):
			userHealStat = user.totalStats.ballisticAttack
		elif (skill.statType == statTypes[2]):
			userHealStat = user.totalStats.magicAttack
		else:
			userHealStat = 1

		totalPotentialHealing = []
		for i in range(len(target)):
			currentPotentialHealing = math.ceil((userHealStat ** 2) / (userHealStat) * skillPower)
			if (type(target[0]) is PlayerCharacter):
				currentPotentialHealing *= 4
			else:
				currentPotentialHealing *= 1.5
			if currentPotentialHealing < 0:
				currentPotentialHealing = 1
			totalPotentialHealing.append(currentPotentialHealing)

		totalDealtHealing = []
		for i in range(len(target)):
			currentHealing = round(totalPotentialHealing[i] * random.uniform((1.00 - (skill.randomMod / 2)), (1.00 + (skill.randomMod / 2))))

			target[i].curHP += currentHealing

			totalDealtHealing.append(currentHealing)

		for i in range(len(target)):
			if (i == 0 and len(target) == 1):
				proceduralPrint(str(userName) + " dealt " + str(totalDealtHealing[i]) + " healing to " + str(targetName[i]) + ".", "")
			elif (i == 0 and len(target) > 1):
				print(str(userName) + " dealt " + str(totalDealtHealing[i]) + " healing to " + str(targetName[i]) + ",")
			elif (i > 0 and i < (len(target) - 1)):
				print((" " * len(userName)) + " dealt " + str(totalDealtHealing[i]) + " healing to " + str(targetName[i]) + ",")
			else:
				proceduralPrint((" " * len(userName)) + " dealt " + str(totalDealtHealing[i]) + " healing to " + str(targetName[i]) + ".", "")

		for i in range(len(target)):
			if (skill.statusEffect != None):
				applyStatusEffect(target[i], user, skill.statusEffect, skill.statusEffectDuration)

	elif (skill.skillType == skillTypes[3]):
		for i in range(len(target)):
			if (target[i].curHP > 0):
				target.pop(target[i])
				targetName.pop(targetName[i])
				targetEvadeStat.pop(targetEvadeStat[i])

		if (skill.statType == statTypes[1]):
			userHealStat = user.totalStats.ballisticAttack
		elif (skill.statType == statTypes[2]):
			userHealStat = user.totalStats.magicAttack
		else:
			userHealStat = 1

		totalPotentialHealing = []
		for i in range(len(target)):
			currentPotentialHealing = round(((userHealStat ** 2) / (userHealStat)) * skillPower)
			if currentPotentialHealing < 0:
				currentPotentialHealing = 0
			totalPotentialHealing.append(currentPotentialHealing)

		totalDealtHealing = []
		for i in range(len(target)):
			currentHealing = round(totalPotentialHealing[i] * random.uniform((1.00 - (skill.randomMod / 2)), (1.00 + (skill.randomMod / 2))))

			target[i].curHP += currentHealing
			if (user in currentPlayers):
				playersHaveMoved[currentPlayers.index(target[i])] = False
			elif (user in currentEnemies):
				enemiesHaveMoved[currentEnemies.index(target[i])] = False

			totalDealtHealing.append(currentHealing)

		for i in range(len(target)):
			if (i == 0 and len(target) == 1):
				proceduralPrint(str(userName) + " revived " + str(targetName[i]) + " with " +  str(totalDealtHealing[i]) + " healing.", "")
			elif (i == 0 and len(target) > 1):
				print(str(userName) + " revived " + str(targetName[i]) + " with " +  str(totalDealtHealing[i]) + " healing,")
			elif (i > 0 and i < (len(target) - 1)):
				print((" " * len(userName)) + " revived " + str(targetName[i]) + " with " +  str(totalDealtHealing[i]) + " healing,")
			else:
				proceduralPrint((" " * len(userName)) + " revived " + str(targetName[i]) + " with " +  str(totalDealtHealing[i]) + " healing.", "")

	elif (skill.skillType == skillTypes[4]):
		applyStatusEffect(target, user, skill.statusEffect, skill.statusEffectDuration)

	elif (skill.skillType == skillTypes[5]):
		hitChance = random.randint(1, 100)
		normalAccuracy = userAccuracyStat / targetEvadeStat * skill.accuracyMod * 100

		if (normalAccuracy >= hitChance):
			applyStatusEffect(target, user, skill.statusEffect, skill.statusEffectDuration)
		else:
			proceduralPrint(userName + " missed.", "")

	user.evaluateCurrentPoints()
	for i in range(len(target)):
		target[i].evaluateCurrentPoints()

	if (user in currentPlayers):
		playersHaveMoved[selectedPlayer] = True
	elif (user in currentEnemies):
		enemiesHaveMoved[selectedEnemy] = True


# The user uses an item onto the target (usually on itself).
def useItem(user, target, itemIndex):
	global battleTurn
	global playersHaveMoved
	global enemiesHaveMoved

	# Get user text for strings
	userName = user.name

	chosenItem = itemsList[itemIndex]

	# Reduce item amount by 1
	user.itemInventory[itemIndex] -= 1

	# String error checking
	if chosenItem.name[0].lower() in ["a", "e", "i", "o", "u"]:
		print("\n" + userName + " used an " + chosenItem.name + ".", end="")
	else:
		print("\n" + userName + " used a " + chosenItem.name + ".", end="")
	input()

	# If item is of health type
	if chosenItem.itemType == itemTypes[0]:
		currentHealing = max(chosenItem.primaryPower, int(round(((chosenItem.secondaryPower / 100) * user.maxHP), 0)))
		user.curHP += currentHealing
		print(userName + " recovered " + str(currentHealing) + " HP.", end="")

	# Else, if item is of mana type
	elif chosenItem.itemType == itemTypes[1]:
		currentHealing = max(chosenItem.primaryPower, int(round(((chosenItem.secondaryPower / 100) * user.maxMP), 0)))
		user.curMP += currentHealing
		print(userName + " recovered " + str(currentHealing) + " MP.", end="")

	# # Else, item is of damage type
	# else:
	# 	damageMod = 1

	# 	if skill.statType == statTypes[1]:
	# 		userAttackStat = user.totalStats.ballisticAttack
	# 		targetDefenseStat = target.totalStats.ballisticDefense
	# 	elif skill.statType == statTypes[2]:
	# 		userAttackStat = user.totalStats.magicAttack
	# 		targetDefenseStat = target.totalStats.magicDefense
	input()

	user.evaluateCurrentPoints()
	target.evaluateCurrentPoints()

	if (user in currentPlayers):
		playersHaveMoved[selectedPlayer] = True
	elif (user in currentEnemies):
		enemiesHaveMoved[selectedEnemy] = True


renderMainMenu()
sys.exit()