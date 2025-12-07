with
    stat_averages as (
        select
            avg(hp) as hp_av,
            avg(attack) as attack_av,
            avg(defense) as defense_av,
            avg(spattack) as spattack_av,
            avg(spdefense) as spdefense_av,
            avg(speed) as speed_av
        from pokemon
    ),
    stat_stdevs as (
        select
            stdevp(hp) as hp_dev,
            stdevp(attack) as attack_dev,
            stdevp(defense) as defense_dev,
            stdevp(spattack) as spattack_dev,
            stdevp(spdefense) as spdefense_dev,
            stdevp(speed) as speed_dev
        from pokemon
    ),
    top_used_pokemon as (
        select top(%s) pokemon as id
        from pokemonusage
        where metagame = %s and period = %s and cutoff = %s
        order by usage desc
    ),
    top_pokemon_stat_avs as (
        select
            avg(hp) as hp_av_p,
            avg(attack) as attack_av_p,
            avg(defense) as defense_av_p,
            avg(spattack) as spattack_av_p,
            avg(spdefense) as spdefense_av_p,
            avg(speed) as speed_av_p
        from top_used_pokemon
        join pokemon on pokemon.id = top_used_pokemon.id
    ),
    z_scores as (
        select
            (hp_av_p - hp_av) / hp_dev as hp_z,
            (attack_av_p - attack_av) / attack_dev as attack_z,
            (defense_av_p - defense_av) / defense_dev as defense_z,
            (spattack_av_p - spattack_av) / spattack_dev as spattack_z,
            (spdefense_av_p - spdefense_av) / spdefense_dev as spdefense_z,
            (speed_av_p - speed_av) / speed_dev as speed_z
        from top_pokemon_stat_avs, stat_averages, stat_stdevs
    )
select 'HP' as stat, hp_z as z_val
from z_scores
union all
select 'Attack', attack_z
from z_scores
union all
select 'Defense', defense_z
from z_scores
union all
select 'SpAttack', spattack_z
from z_scores
union all
select 'SpDefense', spdefense_z
from z_scores
union all
select 'Speed', speed_z
from z_scores
order by z_val desc
;

