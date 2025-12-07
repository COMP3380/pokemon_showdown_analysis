select top(%s) p.name, count(distinct plm.move) as num_moves
from pokemon p
join pokemonlearnsmove plm on plm.pokemon = p.id
group by p.id, p.name
order by num_moves desc
;

