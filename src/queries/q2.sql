select top(%s){cols}
from {input_table} as input_table
join {usage_table} as usage_table on {join_on}
where usage_table.metagame = %s and usage_table.cutoff = %s
group by {group_by}
order by avg(usage_table.usage) desc
;

