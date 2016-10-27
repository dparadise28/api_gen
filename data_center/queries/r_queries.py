import rethinkdb as r

create_account = lambda args, con: r.table('users').insert(dict(list(args.items()) + list({'id': r.uuid(args["email"])}.items())), conflict = "error", durability='soft').run(con)
activate_account = lambda a, b: ''
browse_tree = lambda a, b: ''
update_browse_tree = lambda a, b: ''