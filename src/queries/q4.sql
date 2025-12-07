select top(%s) a.id, a.name, ab_out.usage as low_ladder_usage
from ability a
join abilityusage ab_out on ab_out.ability = a.id
where
    ab_out.metagame = %s
    and ab_out.period = %s
    and ab_out.cutoff = %s
    and a.id in (
        select top(%s) ab_in.ability
        from abilityusage ab_in
        where
            ab_in.metagame = ab_out.metagame
            and ab_in.period = ab_out.period
            and ab_in.cutoff = %s
        order by ab_in.usage desc
    )
order by ab_out.usage
;

