DROP TABLE IF EXISTS RawPokemonCount;
DROP TABLE IF EXISTS PokemonUsage;
DROP TABLE IF EXISTS AbilityUsage;
DROP TABLE IF EXISTS ItemUsage;
DROP TABLE IF EXISTS MoveUsage;
DROP TABLE IF EXISTS SpreadUsage;
DROP TABLE IF EXISTS TeraUsage;
DROP TABLE IF EXISTS TeammateUsage;
DROP TABLE IF EXISTS CheckAndCounter;

DROP TABLE IF EXISTS PokemonHasAbility;
DROP TABLE IF EXISTS PokemonLearnsMove;
DROP TABLE IF EXISTS TypeEffectiveness;
DROP TABLE IF EXISTS MetagameAllowsPokemonFrom;

DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Ability;
DROP TABLE IF EXISTS Move;
DROP TABLE IF EXISTS Pokemon;
DROP TABLE IF EXISTS Type;

DROP TABLE IF EXISTS Cutoff;
DROP TABLE IF EXISTS Period;
DROP TABLE IF EXISTS Metagame;

CREATE TABLE Metagame (
  name VARCHAR(255) PRIMARY KEY CHECK(name <> '')
);

CREATE TABLE Period (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  startDate DATETIME NOT NULL,
  endDate DATETIME NOT NULL,
  CHECK(endDate > startDate)
);

CREATE TABLE Cutoff (
  elo INTEGER PRIMARY KEY CHECK(elo >= 0)
);

CREATE TABLE Type (
  name VARCHAR(255) PRIMARY KEY CHECK(name <> '')
);

CREATE TABLE Pokemon (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  name VARCHAR(255) NOT NULL CHECK(name <> ''),
  type1 VARCHAR(255) NOT NULL REFERENCES Type(name) ON DELETE CASCADE,
  type2 VARCHAR(255) REFERENCES Type(name) ON DELETE NO ACTION,
  hp INTEGER NOT NULL CHECK(hp > 0),
  attack INTEGER NOT NULL CHECK(attack > 0),
  defense INTEGER NOT NULL CHECK(defense > 0),
  spattack INTEGER NOT NULL CHECK(spattack > 0),
  spdefense INTEGER NOT NULL CHECK(spdefense > 0),
  speed INTEGER NOT NULL CHECK(speed > 0),
  tier VARCHAR(255) REFERENCES Metagame(name) ON DELETE SET NULL,
  CHECK(type2 IS NULL OR type2 <> type1) 
);

CREATE TABLE Move (
  id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL CHECK(name <> ''),
  type VARCHAR(255) NOT NULL REFERENCES Type(name) ON DELETE CASCADE,
  power INTEGER NOT NULL CHECK(power >= 0),
  category VARCHAR(8) NOT NULL CHECK(category = 'Physical' OR category = 'Special' OR category = 'Status'),
  pp INTEGER NOT NULL CHECK(pp > 0),
  accuracy INTEGER CHECK(accuracy > 0)
);

CREATE TABLE Ability (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  name VARCHAR(255) NOT NULL CHECK(name <> '')
);

CREATE TABLE Item (
  id VARCHAR(255) PRIMARY KEY CHECK(id <> ''),
  name VARCHAR(255) NOT NULL CHECK(name <> '')
);

CREATE TABLE PokemonHasAbility (
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  ability VARCHAR(255) REFERENCES Ability(id) ON DELETE CASCADE,
  PRIMARY KEY (pokemon, ability)
);

CREATE TABLE PokemonLearnsMove (
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  move VARCHAR(255) REFERENCES Move(id) ON DELETE NO ACTION,
  PRIMARY KEY (pokemon, move)
);

CREATE TABLE TypeEffectiveness (
  attackingType VARCHAR(255) REFERENCES Type(name) ON DELETE CASCADE,
  defendingType VARCHAR(255) REFERENCES Type(name) ON DELETE NO ACTION,
  effectiveness INTEGER NOT NULL CHECK(effectiveness >= 0 AND effectiveness <= 3),
  PRIMARY KEY (attackingType, defendingType)
);

CREATE TABLE MetagameAllowsPokemonFrom (
  parentMetagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  childMetagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE NO ACTION,
  PRIMARY KEY (parentMetagame, childMetagame),
  CHECK(childMetagame <> parentMetagame)
);

CREATE TABLE RawPokemonCount (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  rawCount INTEGER NOT NULL CHECK(rawCount > 0),
  numberPlayers INTEGER NOT NULL CHECK(numberPlayers > 0),
  topGXE INTEGER NOT NULL,
  p99thGXE INTEGER NOT NULL,
  p95thGXE INTEGER NOT NULL,
  PRIMARY KEY (metagame, period, pokemon),
  CHECK(topGXE >= 0 AND topGXE <= 100),
  CHECK(p99thGXE >= 0 AND p99thGXE <= topGXE),
  CHECK(p95thGXE >= 0 AND p95thGXE <= p99thGXE)
);

CREATE TABLE PokemonUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0 AND usage <= 100.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon)
);

CREATE TABLE AbilityUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  ability VARCHAR(255) REFERENCES Ability(id) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, ability)
);

CREATE TABLE ItemUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  item VARCHAR(255) REFERENCES Item(id) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, item)
);

CREATE TABLE MoveUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  move VARCHAR(255) REFERENCES Move(id) ON DELETE NO ACTION,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, move)
);

CREATE TABLE SpreadUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  spread VARCHAR(255) CHECK(spread LIKE '%:%/%/%/%/%/%'),
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, spread)
);

CREATE TABLE TeraUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemon VARCHAR(255) REFERENCES Pokemon(id) ON DELETE NO ACTION,
  type VARCHAR(255) REFERENCES Type(name) ON DELETE CASCADE,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemon, type)
);

CREATE TABLE TeammateUsage (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemonCurrent VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  pokemonTeammate VARCHAR(255) REFERENCES Pokemon(id) ON DELETE NO ACTION,
  usage FLOAT NOT NULL CHECK(usage >= 0.0),
  PRIMARY KEY (metagame, period, cutoff, pokemonCurrent, pokemonTeammate),
  CHECK(pokemonTeammate <> pokemonCurrent)
);

CREATE TABLE CheckAndCounter (
  metagame VARCHAR(255) REFERENCES Metagame(name) ON DELETE CASCADE,
  period VARCHAR(255) REFERENCES Period(id) ON DELETE CASCADE,
  cutoff INTEGER REFERENCES Cutoff(elo) ON DELETE CASCADE,
  pokemonCurrent VARCHAR(255) REFERENCES Pokemon(id) ON DELETE CASCADE,
  pokemonOpposing VARCHAR(255) REFERENCES Pokemon(id) ON DELETE NO ACTION,
  occurrence FLOAT NOT NULL CHECK(occurrence >= 0.0),
  koRate FLOAT NOT NULL CHECK(koRate >= 0.0 AND koRate <= 100.0),
  switchRate FLOAT NOT NULL CHECK(switchRate >= 0.0 AND switchRate <= 100.0),
  PRIMARY KEY (metagame, period, cutoff, pokemonCurrent, pokemonOpposing)
);
