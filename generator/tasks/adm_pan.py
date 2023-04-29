import src.core.query as sql_query
from generator.ntf_prep import UserNtfPrep
from schedule.form import FormMSG
from src.storage.postgres import Postgres


class AdminPanel(FormMSG):
    def __init__(self):
        super().__init__()
        self.db = Postgres()
        self.prepare = UserNtfPrep()

    async def send_event(self):
        self.prepare.generate_ntf(nft_query=sql_query.get_admpan_ntf,
                                  update_undone=sql_query.update_ntf_admin)
        events = []
        fields = self.get_users('Admin')
        for field in fields:
            params = self.get_tmpl_params(content=field['content'], field=field)
            events = self.append_event(events=events, field=field, params=params)
        return events



