create_account = '''
	with account as (
		INSERT INTO data_center.users_tbl(
			first_name
			, last_name
			, user_name
			, password
			, email
		) VALUES (
			%(first_name)s
			, %(last_name)s
			, %(user_name)s
			, %(password)s
			, %(email)s
		) RETURNING
			user_id, first_name, last_name, user_name, password, email
	), activation as (
		INSERT INTO data_center.user_activation_tbl(
			user_id
			, activation_code
			, activated
		) VALUES (
			(select user_id from account)
			, %(new_activation_code)s
			, FALSE
		) RETURNING
			user_id, activation_code, activated
	)
	select
		row_to_json(result)
	from
		(select * from account join activation on account.user_id = activation.user_id) result;
'''

activate_account = '''
	with activation as (
		UPDATE 
			data_center.user_activation_tbl
		SET
			activated = True
		where
			user_id = %(user_id)s and activation_code = %(activation_code)s
		RETURNING
			user_id, activated, activation_code
	)
	select
		row_to_json(result)
	from
		(select * from data_center.users_tbl account join activation on account.user_id = activation.user_id) result;
'''

browse_tree = 'select * from data_center.categories'

update_browse_tree = 'INSERT INTO data_center.categories (ctree) VALUES (%(cats)s)'