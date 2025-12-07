with
    top_pokemon_by_gxe as (
        select top(%s) pokemon as id
        from rawpokemoncount
        where metagame = %s and period = %s
        order by topgxe desc
    ),
    top_stat_av as (
        select avg({stat}) as top_stat_av
        from top_pokemon_by_gxe t
        join pokemon p on p.id = t.id
    ),
    stat_av as (select avg({stat}) as stat_av from pokemon),
    stat_stdev as (select stdevp({stat}) as stat_stdev from pokemon)
select
    '{stat}' as stat,
    top_stat_av.top_stat_av as [top avg],
    stat_av.stat_av as [global avg],
    stat_stdev.stat_stdev as [global stdev],
    (top_stat_av.top_stat_av - stat_av.stat_av)
    / nullif(stat_stdev.stat_stdev, 0) as [z - score]
from top_stat_av, stat_av, stat_stdev
;

