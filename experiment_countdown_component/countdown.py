from __future__ import annotations
from dataclasses import dataclass

import pynecone as pc
from pynecone.components.tags.tag import Tag
from pynecone.event import EVENT_ARG
from pynecone.utils.imports import ImportDict
from pynecone.var import BaseVar


@dataclass
class CountdownApi:
    ref_name: str

    def _get_api_spec(self, fn_name) -> pc.Var[pc.EventChain]:
        return BaseVar(
            name=f"{self.ref_name}.current?.getApi().{fn_name}",
            type_=pc.EventChain,
            is_local=False,
            is_string=False,
        )

    def start(self) -> pc.Var[pc.EventChain]:
        return self._get_api_spec("start")

    def pause(self) -> pc.Var[pc.EventChain]:
        return self._get_api_spec("pause")

    def stop(self) -> pc.Var[pc.EventChain]:
        return self._get_api_spec("stop")


class Countdown(pc.Component):
    """
    A customizable countdown component for pynecone.

    This component wraps `react-countdown`
    https://www.npmjs.com/package/react-countdown
    """

    library = "react-countdown"
    tag = "Countdown"

    date: pc.Var[str] = "0"
    key: pc.Var[str] = "0"
    days_in_hours: pc.Var[bool] = True
    zero_pad_time: pc.Var[int] = 2
    zero_pad_days: pc.Var[int] = 2
    interval_delay: pc.Var[int] = 1000
    precision: pc.Var[int] = 0
    auto_start: pc.Var[bool] = True
    overtime: pc.Var[bool] = False
    ref: pc.Var[str] = ""

    def _get_imports(self) -> ImportDict:
        imports = super()._get_imports()
        imports.pop(self.library, None)  # handle the import in _get_custom_code
        if self.ref.name:
            imports.setdefault("react", set()).add("useRef")
        return imports

    def _get_custom_code(self) -> str | None:
        return "import Countdown from 'react-countdown'"

    def _get_hooks(self) -> str | None:
        hooks = super()._get_hooks()
        if self.ref.name:
            return (hooks or "") + f"\nconst {self.ref.name} = useRef(null)"
        return hooks

    def _render(self) -> Tag:
        tag = super()._render()
        tag.add_props(ref=pc.Var.create(self.ref.name, is_local=False))
        return tag

    @classmethod
    def get_controlled_triggers(cls) -> dict[str, pc.Var]:
        """Get the event triggers that pass the component's value to the handler.

        Returns:
            A dict mapping the event trigger to the var that is passed to the handler.
        """
        return {
            "on_start": EVENT_ARG,
            "on_pause": EVENT_ARG,
            "on_stop": EVENT_ARG,
            "on_tick": EVENT_ARG,
            "on_complete": EVENT_ARG,
        }

    @classmethod
    def get_api(cls, ref_name: str) -> CountdownApi:
        return CountdownApi(ref_name=ref_name)
