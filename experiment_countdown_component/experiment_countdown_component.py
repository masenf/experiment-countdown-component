import datetime
import uuid

import pynecone as pc

from .countdown import Countdown


REF = "countdown_reference"


class State(pc.State):
    _date: datetime.datetime = datetime.datetime.now()
    _timer_complete: bool = False
    timer_secs: int = 60
    timer_key: str = ""
    timer_running: bool = False
    timer_paused: bool = True

    @pc.var
    def date(self) -> str:
        return self._date.isoformat()

    def set_timer_secs(self, ts: int):
        self.timer_secs = ts

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

    @pc.var
    def timer_complete(self) -> bool:
        return self.timer_key and self._timer_complete


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.hstack(
                pc.number_input(value=State.timer_secs, on_change=State.set_timer_secs),
                pc.button("Reset", on_click=State.do_start),
            ),
            pc.heading(
                Countdown.create(
                    date=State.date,
                    ref=REF,
                    on_start=State.on_start,
                    on_pause=State.on_pause,
                    on_stop=State.on_stop,
                    on_complete=State.on_complete,
                ),
                font_size="2em",
            ),
            pc.cond(
                State.timer_key and State.timer_complete,
                pc.text("Countdown Success! 🎉"),
                pc.hstack(
                    pc.cond(
                        State.timer_paused,
                        pc.button("Start", on_click=Countdown.get_api(REF).start()),
                        pc.button("Pause", on_click=Countdown.get_api(REF).pause()),
                    ),
                    pc.button("Stop", on_click=Countdown.get_api(REF).stop()),
                    pc.button("+1m", on_click=lambda: State.add_sec(60)),
                    pc.button("-1m", on_click=lambda: State.add_sec(-60)),
                ),
            ),
        ),
        padding_top="10%",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
