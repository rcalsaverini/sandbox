import reflex as rx
from sqlmodel import select
import asyncio


class Channel(rx.Model, table=True):
    channel_id: str
    title: str
    description: str
    url: str


class PageState(rx.State):
    channels: list[Channel]
    _db_updated: bool = False

    def load_channels(self):
        with rx.session() as session:
            self.channels = session.exec(select(Channel)).all()
        yield PageState.reload_all

    @rx.background
    async def reload_all(self):
        while True:
            await asyncio.sleep(2)
            if self._db_updated:
                async with self:
                    with rx.session() as session:
                        self.channels = session.exec(select(Channel)).all()
                    self._db_updated = False

    @rx.var
    def db_updated(self):
        return self._db_updated

    @rx.var
    def total(self):
        return len(self.channels)


def page():
    return rx.vstack(
        rx.heading("This is the Channels"),
        rx.fragment(rx.foreach(PageState.channels, rx.heading)),
    )
