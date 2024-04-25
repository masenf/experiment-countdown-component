from __future__ import annotations

import datetime

import reflex as rx


class Countdown(rx.Component):
    """
    A customizable countdown component for reflex.

    This component wraps `react-countdown`
    https://www.npmjs.com/package/react-countdown
    """

    library = "react-countdown"
    tag = "Countdown"
    is_default = True

    date: rx.Var[datetime.datetime]
    key: rx.Var[str] = "0"
    days_in_hours: rx.Var[bool] = True
    zero_pad_time: rx.Var[int] = 2
    zero_pad_days: rx.Var[int] = 2
    interval_delay: rx.Var[int] = 1000
    precision: rx.Var[int] = 0
    auto_start: rx.Var[bool] = True
    overtime: rx.Var[bool] = False

    on_start: rx.EventHandler[lambda e: [e]]
    on_pause: rx.EventHandler[lambda e: [e]]
    on_stop: rx.EventHandler[lambda e: [e]]
    on_tick: rx.EventHandler[lambda e: [e]]
    on_complete: rx.EventHandler[lambda e: [e]]

    @classmethod
    def create(cls, *children, **props) -> Countdown:
        # If an id is not specified, generate one automatically to allow API access.
        props.setdefault("id", rx.vars.get_unique_variable_name())

        return super().create(*children, **props)

    def _get_api_spec(self, fn_name) -> rx.event.EventSpec:
        """Returns an EventSpec which accesses the API methods for the Countdown component."""
        return rx.call_script(f"refs['{self.get_ref()}'].current?.getApi().{fn_name}()")

    def start(self) -> rx.event.EventSpec:
        """Start the countdown timer."""
        return self._get_api_spec("start")

    def pause(self) -> rx.event.EventSpec:
        """Pause the countdown timer."""
        return self._get_api_spec("pause")

    def stop(self) -> rx.event.EventSpec:
        """Stop the countdown timer."""
        return self._get_api_spec("stop")


countdown = Countdown.create
