from __future__ import annotations
from dataclasses import dataclass

import reflex as rx
from reflex.vars import BaseVar


@dataclass
class CountdownApi:
    ref_name: rx.Var[str]

    def _get_api_spec(self, fn_name) -> rx.Var[rx.EventChain]:
        return BaseVar(
            _var_name=f"{self.ref_name.as_ref()}.current?.getApi().{fn_name}",
            _var_type=rx.EventChain,
            _var_is_local=False,
            _var_is_string=False,
        )

    def start(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("start")

    def pause(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("pause")

    def stop(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("stop")


class Countdown(rx.Component):
    """
    A customizable countdown component for reflex.

    This component wraps `react-countdown`
    https://www.npmjs.com/package/react-countdown
    """

    library = "react-countdown"
    tag = "Countdown"
    is_default = True

    date: rx.Var[str] = "0"
    key: rx.Var[str] = "0"
    days_in_hours: rx.Var[bool] = True
    zero_pad_time: rx.Var[int] = 2
    zero_pad_days: rx.Var[int] = 2
    interval_delay: rx.Var[int] = 1000
    precision: rx.Var[int] = 0
    auto_start: rx.Var[bool] = True
    overtime: rx.Var[bool] = False

    @classmethod
    def get_event_triggers(cls) -> dict[str, rx.Var]:
        """Get the event triggers that pass the component's value to the handler.

        Returns:
            A dict mapping the event trigger to the var that is passed to the handler.
        """
        return {
            "on_start": lambda e: [e],
            "on_pause": lambda e: [e],
            "on_stop": lambda e: [e],
            "on_tick": lambda e: [e],
            "on_complete": lambda e: [e],
        }

    @classmethod
    def get_api(cls, ref_name: str) -> CountdownApi:
        return CountdownApi(
            ref_name=rx.Var.create(rx.utils.format.format_ref(ref_name)),
        )
