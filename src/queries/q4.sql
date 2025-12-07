select top (%s) a.id, a.name, avg(ab_out.usage) as average_usage
from ability a
join abilityusage ab_out on ab_out.ability = a.id
where ab_out.metagame = %s and ab_out.period = %s
and ab_out.cutoff = %s
and a.id in (
    select ability from (
        select top (%s) ab_in.ability as ability, avg(ab_in.usage) as av_top_usage
        from abilityusage ab_in
        where ab_in.metagame = ab_out.metagame and ab_in.period = ab_out.period
        and ab_in.cutoff = %s
        group by ab_in.ability
        order by av_top_usage desc
    ) as t
)
group by a.id, a.name
order by average_usage;
