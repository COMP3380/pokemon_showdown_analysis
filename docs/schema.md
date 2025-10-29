# Table Schemas

DDL for the tables used in this project.

"Pokémon" is typed as "Pokemon" in code to make developers' life easier. All strings are unamiously stored as `VARCHAR(255)` regardless of realistically required length to store the information for the same reason.

## Pokémon

Stores data about Pokémon species. 

```sql
CREATE TABLE Pokemon (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  name VARCHAR(255) NOT NULL CHECK(name <> ''),
  form VARCHAR(255) NOT NULL CHECK(form <> ''),
  type1 VARCHAR(255) NOT NULL REFERENCES Type(name) ON DELETE CASCADE,
  type2 VARCHAR(255) REFERENCES Type(name) CHECK(type2 <> type1) ON DELETE CASCADE,
  hp INTEGER NOT NULL CHECK(hp > 0),
  attack INTEGER NOT NULL CHECK(attack > 0),
  defense INTEGER NOT NULL CHECK(defense > 0),
  spattack INTEGER NOT NULL CHECK(spattack > 0),
  spdefense INTEGER NOT NULL CHECK(spdefense > 0),
  speed INTEGER NOT NULL CHECK(speed > 0),
  tier VARCHAR(255) REFERENCES Metagame(name) ON DELETE SET NULL
);
```

## Ability

Stores data about Pokémon abilities.

```sql
CREATE TABLE Ability (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  name VARCHAR(255) NOT NULL CHECK(name <> '')
);
```

## Item

Stores data about Pokémon holdable items.

```sql
CREATE TABLE Item (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  name VARCHAR(255) NOT NULL CHECK(name <> '')
);
```

## Move

Stores data about Pokémon moves. As a convention, `accuracy = NULL` is equivalent to a move without accuracy (it is unaffected whatsoever by accuracy), usually status moves.

```sql
CREATE TABLE Move (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  name VARCHAR(255) NOT NULL CHECK(name <> ''),
  type VARCHAR(255) NOT NULL REFERENCES Type(name) ON DELETE CASCADE,
  power INTEGER NOT NULL CHECK(power > 0),
  category VARCHAR(8) NOT NULL CHECK(category = 'Physical' OR category = 'Special' OR category = 'Status'),
  pp INTEGER NOT NULL CHECK(pp > 0),
  accuracy INTEGER CHECK(accuracy > 0)
);
```

## Type

Stores data about Pokémon types.

```sql
CREATE TABLE Type (
  name VARCHAR(255) PRIMARY KEY CHECK(name <> '')
);
```

## Metagame

Stores data about various *Pokémon Showdown!* metagames played and had stats recorded. Currently only supporting Ubers, OU, UU, RU, NU, PU, ZU.

```sql
CREATE TABLE Metagame (
  name VARCHAR(255) PRIMARY KEY CHECK(name <> '')
);
```

## Cutoff

Stores data about elo cutoffs *Smogon*'s data files are separated into.

* OU: 0, 1500, 1695, 1825
* Other metagames: 0, 1500, 1630, 1760

```sql
CREATE TABLE Cutoff (
  elo INTEGER PRIMARY KEY CHECK(elo >= 0)
);
```

## Period

Stores data about the different periods of play *Smogon* record aggregated statistics over.

```sql
CREATE TABLE Period (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  startDate DATETIME NOT NULL,
  endDate DATETIME NOT NULL CHECK(endDate > startDate)
);
```

## PokémonHasAbility

Stores data about each Pokémon's available abilities.

```sql
CREATE TABLE PokemonHasAbility (
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  ability VARCHAR(255) REFERENCES Ability(id) ON DELETE CASCADE,
  PRIMARY KEY (pokemon, ability)
);
```

## PokémonLearnsMove

Stores data about each Pokémon's learnset. Method of learning is omitted.

```sql
CREATE TABLE PokemonLearnsMove (
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  move VARCHAR(255) REFERENCES Move(id) ON DELETE CASCADE,
  PRIMARY KEY (pokemon, move)
);
```

## TypeEffectiveness

Stores data about the effectiveness of types on each other.

* 0 is 1x effectiveness.
* 1 is super effective, or 2x effectiveness.
* 2 is not very effective, or 0.5x effectiveness.
* 3 is immune to, or 0x effectiveness.

```sql
CREATE TABLE TypeEffectiveness (
  attackingType VARCHAR(255) REFERENCES Type(name) ON DELETE CASCADE,
  defendingType VARCHAR(255) REFERENCES Type(name) ON DELETE CASCADE,
  effectiveness INTEGER NOT NULL CHECK(effectiveness >= 0 AND effectiveness <= 3),
  PRIMARY KEY (attackingType, defendingType)
);
```

## MetagameAllowsPokémonFrom

Stores data about which metagame's entire Pokémon set is allowed in another metagame.

```sql
CREATE TABLE MetagameAllowsPokemonFrom (
  parentMetagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  childMetagame VARCHAR(255) REFERENCES Metagame(name) CHECK(childMetagame <> parentMetagame) ON DELETE CASCADE,
  PRIMARY KEY (parentMetagame, childMetagame)
);
```

## RawPokémonCount

Stores data about the raw number of Pokémon appearance in a metagame over a period, how many players use them, and the players' GXE percentiles.

```sql
CREATE TABLE RawPokemonCount (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  rawCount INTEGER NOT NULL CHECK(rawCount > 0),
  numberPlayers INTEGER NOT NULL CHECK(numberPlayers > 0),
  topGXE INTEGER NOT NULL CHECK(topGXE >= 0 AND topGXE <= 100),
  p99thGXE INTEGER NOT NULL CHECK(p99thGXE >= 0 AND p99thGXE <= topGXE),
  p95thGXE INTEGER NOT NULL CHECK(p95thGXE >= 0 AND p95thGXE <= p99thGXE),
  PRIMARY KEY (metagame, period, pokemon)
);
```

## PokemonUsage

Stores data about the usage rate of a Pokémon in a metagame over a period, weighted by games including players with at least a certain elo.

```sql
CREATE TABLE PokemonUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0 AND usage <= 100.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon)
);
```

## AbilityUsage

Stores data about the usage count of an ability for a Pokémon in a metagame over a period, weighted by games including players with at least a certain elo.

```sql
CREATE TABLE AbilityUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  ability VARCHAR(255) REFERENCES Ability(id) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, ability)
);
```

## ItemUsage

Stores data about the usage count of an item for a Pokémon in a metagame over a period, weighted by games including players with at least a certain elo.

```sql
CREATE TABLE ItemUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  item VARCHAR(255) REFERENCES Item(id) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, item)
);
```

## MoveUsage

Stores data about the usage count of a move for a Pokémon in a metagame over a period, weighted by games including players with at least a certain elo.

```sql
CREATE TABLE MoveUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  move VARCHAR(255) REFERENCES Move(id) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, move)
);
```

## SpreadUsage

Stores data about the usage count of a stat spread for a Pokémon in a metagame over a period, weighted by games including players with at least a certain elo.

```sql
CREATE TABLE SpreadUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  spread VARCHAR(255) CHECK(spread LIKE '%:%/%/%/%/%/%'),
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, spread)
);
```

## TeraUsage

Stores data about the usage count of a Tera type for a Pokémon in a metagame over a period, weighted by games including players with at least a certain elo.

```sql
CREATE TABLE TeraUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  type VARCHAR(255) REFERENCES Type(name) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, type)
);
```

## TeammateUsage

Stores data about the usage count of a Pokémon given another Pokémon in a metagame over a period, weighted by games including players with at least a certain elo.

```sql
CREATE TABLE TeammateUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemonCurrent VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  pokemonTeammate VARCHAR(255) REFERENCES Pokemon(id) CHECK(pokemonTeammate <> pokemonCurrent) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemonCurrent, pokemonTeammate)
);
```

## CheckAndCounter

Stores data about the occurence count, percentage of being knocked out, percentage of switching out of a Pokémon facing another Pokémon in a metagame over a period, weighted by games including players with at least a certain elo.

```sql
CREATE TABLE CheckAndCounter (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemonCurrent VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  pokemonOpposing VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  occurrence FLOAT NOT NULL CHECK(occurrence >= 0.0),
  koRate FLOAT NOT NULL CHECK(koRate >= 0.0 AND koRate <= 100.0),
  switchRate FLOAT NOT NULL CHECK(switchRate >= 0.0 AND switchRate <= 100.0),
  PRIMARY KEY (metagame, period, cutoff, pokemonCurrent, pokemonOpposing)
);
```
