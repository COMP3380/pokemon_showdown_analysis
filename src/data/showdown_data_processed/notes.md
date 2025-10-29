# Some Notes

## Typechart Number Meanings

Fire: 1   → takes double damage from Fire
Grass: 2  → takes half damage from Grass
Normal: 0 → neutral (×1)
Ghost: 3  → immune (×0)

## Pokedex

I noticed that only cosmetic pokemon don't have types, and that they aren't
tracked in smogun stats. So I ignored them.

## Abilities

/*

Ratings and how they work:

-1: Detrimental
	  An ability that severely harms the user.
	ex. Defeatist, Slow Start

 0: Useless
	  An ability with no overall benefit in a singles battle.
	ex. Color Change, Plus

 1: Ineffective
	  An ability that has minimal effect or is only useful in niche situations.
	ex. Light Metal, Suction Cups

 2: Useful
	  An ability that can be generally useful.
	ex. Flame Body, Overcoat

 3: Effective
	  An ability with a strong effect on the user or foe.
	ex. Chlorophyll, Sturdy

 4: Very useful
	  One of the more popular abilities. It requires minimal support to be effective.
	ex. Adaptability, Magic Bounce

 5: Essential
	  The sort of ability that defines metagames.
	ex. Imposter, Shadow Tag

*/


## Learnsets

- sometimes a forme inherits all base form learnset 1:1
    - no entry in learnsets.ts OR entry has no learnset
    - e.g: shaymin
    - so use base learnset
- sometimes a forme inherits all base form learnset and then adds some
    - entry in learnsets.ts with just added moves
    - e.g: rotom
    - so do base learnset + new moves
- sometimes a forme cannot have all moves that its base has
    - entry in learnsets.ts with entire learnset
    - e.g: mrmime
    - so just to forme learnset

Issue: There is no apparent indication if a forme entry in learnsets.ts or in
pokedex.ts will inherit all moves from its base.

Options to remedy this:

1. Use number of moves in learnset as a measure of if it seems like just additional moves
    - Small learnset => probably additional moves. Big learnset => probably unique learnset
    - Issues: Outliers could ruin this. But still plausible
2. Check if forme learnset has any moves overlap with base learnset
    - If no overlap => probably additonal moves. If overlap => probably unique learnset
    - Issues: Are any outliers possible? Could be expensive considering the shear number of mons and moves per mon.

A second issue has hit the towers: 
    - *Some* cosmetic forms (e.g: gastrodoneast) have different learnsets...
