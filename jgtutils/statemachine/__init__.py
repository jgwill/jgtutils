"""
JGT State Machine Framework
============================

A state machine definition, runtime, and code generation framework.
Implements Specs 60-62 from the Caishen RISE specifications.

Modules:
  - model: State machine definition model (dataclasses)
  - parser: JSON/XML parser for .smdf files
  - runtime: Runtime engine (Context, State, Event, Observer)
  - codegen: Code generator (SMCG) producing Python/TypeScript
  - cli: Command-line interface for code generation
"""

__version__ = "0.1.0"

from jgtutils.statemachine.model import (
    StateMachineDefinition,
    SettingsModel,
    EventSourceDef,
    EventDef,
    TimerDef,
    ParameterDef,
    StateDef,
    TransitionDef,
    ActionDef,
    ParallelDef,
    ObjectRef,
    ContextConfig,
    StateKindType,
)

from jgtutils.statemachine.parser import StateMachineParser
from jgtutils.statemachine.runtime import (
    ContextBase,
    Context,
    ContextAsync,
    State,
    StateKind,
    TransitionHelper,
    IObserver,
    ObserverNull,
    ObserverConsole,
)

__all__ = [
    "StateMachineDefinition",
    "SettingsModel",
    "EventSourceDef",
    "EventDef",
    "TimerDef",
    "ParameterDef",
    "StateDef",
    "TransitionDef",
    "ActionDef",
    "ParallelDef",
    "ObjectRef",
    "ContextConfig",
    "StateKindType",
    "StateMachineParser",
    "ContextBase",
    "Context",
    "ContextAsync",
    "State",
    "StateKind",
    "TransitionHelper",
    "IObserver",
    "ObserverNull",
    "ObserverConsole",
]
