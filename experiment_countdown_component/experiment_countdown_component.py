import datetime
import uuid

import reflex as rx

from .countdown import Countdown


REF = "countdown_reference"


class State(rx.State):
    _date: datetime.datetime = datetime.datetime.now()
    _timer_complete: bool = False
    timer_secs: int = 60
    timer_key: str = ""
    timer_running: bool = False
    timer_paused: bool = True

    @rx.var
    def date(self) -> str:
        return self._date.isoformat()

    def set_timer_secs(self, ts: int):
        self.timer_secs = int(ts)

    def add_sec(self, sec: int | float):
        self._date = self._date + datetime.timedelta(seconds=sec)

    def do_start(self):
        self._date = datetime.datetime.now() + datetime.timedelta(
            seconds=int(self.timer_secs)
        )
        self.timer_key = str(uuid.uuid4())
        self._timer_complete = False

    def on_start(self, time_delta):
        self._timer_complete = False
        self.timer_running = True
        self.timer_paused = False

    def on_pause(self, time_delta):
        self.timer_paused = True

    def on_stop(self, time_delta):
        self.timer_running = False
        return self.on_pause(time_delta)

    def on_complete(self, time_delta):
        self._timer_complete = True
        return self.on_stop(time_delta)

    @rx.var
    def timer_complete(self) -> bool:
        return self.timer_key and self._timer_complete


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.input(
                    type="number",
                    value=State.timer_secs.to(str),
                    on_change=State.set_timer_secs,
                ),
                rx.button("Reset", on_click=State.do_start),
            ),
            rx.heading(
                Countdown.create(
                    id=REF,
                    date=State.date,
                    on_start=State.on_start,
                    on_pause=State.on_pause,
                    on_stop=State.on_stop,
                    on_complete=State.on_complete,
                ),
                font_size="2em",
            ),
            rx.cond(
                State.timer_key & State.timer_complete,
                rx.text("Countdown Success! 🎉"),
                rx.hstack(
                    rx.cond(
                        State.timer_paused,
                        rx.button("Start", on_click=Countdown.get_api(REF).start()),
                        rx.button("Pause", on_click=Countdown.get_api(REF).pause()),
                    ),
                    rx.button("Stop", on_click=Countdown.get_api(REF).stop()),
                    rx.button("+1m", on_click=lambda: State.add_sec(60)),
                    rx.button("-1m", on_click=lambda: State.add_sec(-60)),
                ),
            ),
        ),
        padding_top="10%",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
