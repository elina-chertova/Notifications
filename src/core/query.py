
gen: str = """
select * from notification.email_template
where source='{0}' and message='{1}';
"""

gen_source: str = """
select * from notification.email_template
where source='{0}';
"""

admin_pan: str = """
select * from notification.email_template
where source='Admin' and message='{}';
"""

pending: str = """
select * from notification.user_ntf
where source='{0}' and type='{1}' and status='pending';
"""

pending_admin: str = """
select * from notification.user_ntf
where source='Admin' and status='pending';
"""

users_A = "select id, email, first_name, last_name from public.user where subscription='true';"

users = "select id, email, first_name, last_name from public.user where id='{0}';"

ntf_undone = "select ntf_id, destination, type, subject, title, text, content, priority, time, source " \
             "from notification.notice where status='undone' and source='Auto';"


insert_new_notice = "INSERT INTO notification.notice (ntf_id, destination, type, subject, title, " \
                    "text, content, priority, time, source, status, created, modified) VALUES {};"


insert_us_ntf = "INSERT INTO notification.user_ntf (user_id, email, first_name, last_name, ntf_id, " \
                "destination, type, subject, title, text, content, priority, time, source, status) " \
                "VALUES %s;"

insert_us_ntf_as = "INSERT INTO notification.user_ntf (user_id, email, first_name, last_name, ntf_id, " \
                "destination, type, subject, title, text, content, priority, time, source, status) " \
                "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15);"


update_ntf = "UPDATE notification.notice SET status='done' where status='undone' and source='Auto';"


update_ntf_admin = "UPDATE notification.notice SET status='done' where status='undone' and " \
                   "source='Admin' and time <= now();"

update_usr_nft = "UPDATE notification.user_ntf SET status='success' where user_id='{0}' and " \
                 "status='pending' and ntf_id='{1}';"

check_nft_exists = "select * from notification.notice where ntf_id='{0}' and status='{1}' \
                    and source='{2}'"

check_nft_pending = "select * from notification.user_ntf where ntf_id='{0}' and status='pending'"

check_source = ""

get_admpan_ntf = "select ntf_id, destination, type, subject, title, text, content, priority, time, source " \
                 "from notification.notice where source = 'Admin' and status = 'undone' and time <= now();"


subscribe = "UPDATE public.user SET subscription='true' where id='{0}';"
unsubscribe = "UPDATE public.user SET subscription='false' where id='{0}';"
