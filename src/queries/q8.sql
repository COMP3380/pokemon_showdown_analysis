with
    latestperiod as (select top 1 id from period order by enddate desc),

    highestcutoffmetagame as (
        select metagame, max(cutoff) as maxcutoff from pokemonusage group by metagame
    ),

    rankedtype2pokemonusage as (
        select
            pokemonusage.metagame,
            pokemonusage.pokemon,
            pokemonusage.usage,
            row_number() over (
                partition by pokemonusage.metagame order by pokemonusage.usage desc
            ) as rn
        from pokemonusage
        inner join pokemon on pokemonusage.pokemon = pokemon.id
        inner join latestperiod on pokemonusage.period = latestperiod.id
        inner join
            highestcutoffmetagame
            on pokemonusage.metagame = highestcutoffmetagame.metagame
            and pokemonusage.cutoff = highestcutoffmetagame.maxcutoff
        where (pokemon.type1 = %s or pokemon.type2 = %s)
    ),

    top10type2pokemon as (
        select metagame, pokemon from rankedtype2pokemonusage where rn <= 10
    ),

    filteredcounters as (
        select pokemonopposing, occurrence, korate, switchrate
        from checkandcounter
        inner join
            top10type2pokemon
            on checkandcounter.pokemoncurrent = top10type2pokemon.pokemon
            and checkandcounter.metagame = top10type2pokemon.metagame
        inner join latestperiod on checkandcounter.period = latestperiod.id
        inner join
            highestcutoffmetagame
            on checkandcounter.metagame = highestcutoffmetagame.metagame
            and checkandcounter.cutoff = highestcutoffmetagame.maxcutoff
    )

select
    'Type 1 (' + %s + ') Counters' as analysis_type,
    sum(occurrence) as total_occurrence,
    avg(korate) as avg_ko_rate,
    avg(switchrate) as avg_switch_rate
from filteredcounters
inner join pokemon on filteredcounters.pokemonopposing = pokemon.id
where (pokemon.type1 = %s or pokemon.type2 = %s)

union all

select
    'All Counters Average' as analysis_type,
    sum(occurrence) as total_occurrence,
    avg(korate) as avg_ko_rate,
    avg(switchrate) as avg_switch_rate
from filteredcounters
;

