import datetime
import uuid

import reflex as rx

from .countdown import countdown


class State(rx.State):
    _timer_complete: bool = False
    date: datetime.datetime = datetime.datetime.now()
    timer_secs: int = 60
    timer_key: str = ""
    timer_running: bool = False
    timer_paused: bool = True

    def add_sec(self, sec: int | float):
        self.date = self.date + datetime.timedelta(seconds=sec)

    def do_reset(self, form_data):
        try:
            self.timer_secs = int(form_data.get("ts", 0))
        except ValueError:
            return
        self.date = datetime.datetime.now() + datetime.timedelta(
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
    countdown_1 = countdown(
        date=State.date,
        on_start=State.on_start,
        on_pause=State.on_pause,
        on_stop=State.on_stop,
        on_complete=State.on_complete,
    )

    return rx.center(
        rx.vstack(
            rx.form(
                rx.hstack(
                    rx.input(
                        type="number",
                        name="ts",
                        default_value=State.timer_secs.to(str),
                    ),
                    rx.button("Reset"),
                ),
                on_submit=State.do_reset,
            ),
            rx.heading(
                countdown_1,
                size="9",
            ),
            rx.cond(
                State.timer_key & State.timer_complete,
                rx.text("Countdown Success! 🎉"),
                rx.hstack(
                    rx.cond(
                        State.timer_paused,
                        rx.button("Start", on_click=countdown_1.start()),
                        rx.button("Pause", on_click=countdown_1.pause()),
                    ),
                    rx.button("Stop", on_click=countdown_1.stop()),
                    rx.button("+1m", on_click=State.add_sec(60)),
                    rx.button("-1m", on_click=State.add_sec(-60)),
                ),
            ),
            align="center",
        ),
        padding_top="10%",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
