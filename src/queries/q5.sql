select top (%s) p1.name, p2.name, t_out.usage
from teammateusage t_out
join pokemon p1 on t_out.pokemoncurrent = p1.id
join pokemon p2 on t_out.pokemonteammate = p2.id
where t_out.metagame = %s
  and t_out.cutoff = %s
  and t_out.pokemoncurrent < t_out.pokemonteammate
  and exists (
      select 1
      from teammateusage t_in
      where t_in.metagame = t_out.metagame
        and t_in.cutoff = t_out.cutoff
        and t_in.pokemoncurrent = t_out.pokemoncurrent
        and t_in.pokemonteammate = t_out.pokemonteammate
        and t_in.period != t_out.period
  )
order by t_out.usage desc;
