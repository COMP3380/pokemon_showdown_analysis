with
    metagamehighestcutoff as (
        select metagame, max(cutoff) as maxcutoff from pokemonusage group by metagame
    ),

    metagamelowestcutoff as (
        select metagame, min(cutoff) as mincutoff from pokemonusage group by metagame
    ),

    pokemonusageatperiod as (
        select metagame, cutoff, pokemon, usage from pokemonusage where period = %s
    ),

    highestcutoffusage as (
        select pokemonusageatperiod.metagame, maxcutoff, pokemon, usage
        from pokemonusageatperiod
        inner join
            metagamehighestcutoff
            on pokemonusageatperiod.metagame = metagamehighestcutoff.metagame
            and pokemonusageatperiod.cutoff = metagamehighestcutoff.maxcutoff
    ),

    lowestcutoffusage as (
        select pokemonusageatperiod.metagame, mincutoff, pokemon, usage
        from pokemonusageatperiod
        inner join
            metagamelowestcutoff
            on pokemonusageatperiod.metagame = metagamelowestcutoff.metagame
            and pokemonusageatperiod.cutoff = metagamelowestcutoff.mincutoff
    ),

    diffusage as (
        select
            highestcutoffusage.metagame,
            highestcutoffusage.pokemon,
            lowestcutoffusage.usage - highestcutoffusage.usage as usagediff
        from highestcutoffusage
        inner join
            lowestcutoffusage
            on highestcutoffusage.metagame = lowestcutoffusage.metagame
            and highestcutoffusage.pokemon = lowestcutoffusage.pokemon
    ),

    metagamehighestdiff as (
        select metagame, max(usagediff) as highestdiff from diffusage group by metagame
    )

select
    diffusage.metagame,
    diffusage.pokemon,
    metagamehighestdiff.highestdiff as usagedifference
from diffusage
inner join
    metagamehighestdiff
    on diffusage.metagame = metagamehighestdiff.metagame
    and diffusage.usagediff = metagamehighestdiff.highestdiff
order by diffusage.metagame
;

