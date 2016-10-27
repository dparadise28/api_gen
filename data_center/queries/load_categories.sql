\connect db_v1
create temporary table temp_cats (values text);
\copy temp_cats (values) from 'C:\Users\Admin\Desktop\Folders\apps\ecom\project_setup\categories.json' csv quote e'\x01' delimiter e'\x02'
select
	string_agg(regexp_replace(values, E'[\n\t]+', ' ', 'g'), '')
into
	temporary table unformatted_temp_cats
from
	temp_cats;
drop table temp_cats;
\copy unformatted_temp_cats to 'C:\Users\Admin\Desktop\Folders\apps\ecom\project_setup\unformatted_categories.json'
\copy data_center.categories (ctree) from 'C:\Users\Admin\Desktop\Folders\apps\ecom\project_setup\unformatted_categories.json'
drop table unformatted_temp_cats;