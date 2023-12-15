# ruff: noqa: D100, D101, D102, D103, D104, D105, D107
from __future__ import annotations

import queue
import threading
from collections import defaultdict
from inspect import signature
from threading import Lock
from typing import (
    Callable,
    Generic,
    Protocol,
    cast,
)

from .basic_types import (
    Action,
    AutorunReturnType,
    BaseAction,
    BaseEvent,
    ComparatorOutput,
    Event,
    EventHandler,
    FinishAction,
    Immutable,
    InitAction,
    ReducerType,
    Selector,
    SelectorOutput,
    State,
    State_co,
    is_reducer_result,
    is_state,
)


class CreateStoreOptions(Immutable):
    threads: int = 5
    autorun_initial_run: bool = True
    scheduler: Callable[[Callable], None] | None = None


class EventSubscriptionOptions(Immutable):
    run_async: bool = True


class AutorunType(Protocol, Generic[State_co]):
    def __call__(
        self: AutorunType,
        selector: Callable[[State_co], SelectorOutput],
        comparator: Selector | None = None,
    ) -> Callable[
        [
            Callable[[SelectorOutput], AutorunReturnType]
            | Callable[[SelectorOutput, SelectorOutput], AutorunReturnType],
        ],
        Callable[[], AutorunReturnType],
    ]:
        ...


class EventSubscriber(Protocol):
    def __call__(
        self: EventSubscriber,
        event_type: type[Event],
        handler: Callable[[Event], None],
        options: EventSubscriptionOptions | None = None,
    ) -> Callable[[], None]:  # pyright: ignore[reportGeneralTypeIssues]
        pass


class InitializeStateReturnValue(Immutable, Generic[State, Action, Event]):
    dispatch: Callable[[Action | Event | list[Action | Event]], None]
    subscribe: Callable[[Callable[[State], None]], Callable[[], None]]
    subscribe_event: EventSubscriber
    autorun: AutorunType[State]


class SideEffectRunnerThread(threading.Thread):
    def __init__(self: SideEffectRunnerThread, task_queue: queue.Queue) -> None:
        super().__init__()
        self.task_queue = task_queue
        self.daemon = True

    def run(self: SideEffectRunnerThread) -> None:
        while True:
            try:
                task = self.task_queue.get(timeout=3)
            except queue.Empty:
                continue

            try:
                event_handler, event = task
                event_handler(event)
            finally:
                self.task_queue.task_done()


def create_store(
    reducer: ReducerType[State, Action, Event],
    options: CreateStoreOptions | None = None,
) -> InitializeStateReturnValue[State, Action, Event]:
    _options = CreateStoreOptions() if options is None else options

    state: State
    listeners: set[Callable[[State], None]] = set()
    event_handlers: defaultdict[
        type[Event],
        set[tuple[EventHandler, EventSubscriptionOptions]],
    ] = defaultdict(set)

    actions: list[Action] = []
    events: list[Event] = []

    event_handlers_queue = queue.Queue[tuple[EventHandler, Event]]()
    for _ in range(_options.threads):
        worker = SideEffectRunnerThread(event_handlers_queue)
        worker.start()

    is_running = Lock()

    def run() -> None:
        with is_running:
            nonlocal state
            while len(actions) > 0 or len(events) > 0:
                if len(actions) > 0:
                    action = actions.pop(0)
                    result = reducer(state if 'state' in locals() else None, action)
                    if is_reducer_result(result):
                        state = result.state
                        if result.actions:
                            actions.extend(result.actions)
                        if result.events:
                            events.extend(result.events)
                    elif is_state(result):
                        state = result

                    if len(actions) == 0:
                        for listener in listeners.copy():
                            listener(state)

                if len(events) > 0:
                    event = events.pop(0)
                    for event_handler, options in event_handlers[type(event)].copy():
                        if options.run_async:
                            event_handlers_queue.put((event_handler, event))
                        else:
                            event_handler(event)

    def dispatch(items: Action | Event | list[Action | Event]) -> None:
        should_quit = False
        if isinstance(items, BaseAction):
            items = [items]

        if isinstance(items, BaseEvent):
            items = [items]

        for item in items:
            if isinstance(item, BaseAction):
                if isinstance(item, FinishAction):
                    should_quit = True
                actions.append(item)
            if isinstance(item, BaseEvent):
                events.append(item)

        if _options.scheduler is None and not is_running.locked():
            run()

        if should_quit:
            event_handlers_queue.join()

    def subscribe(listener: Callable[[State], None]) -> Callable[[], None]:
        listeners.add(listener)
        return lambda: listeners.remove(listener)

    def subscribe_event(
        event_type: type[Event],
        handler: EventHandler,
        options: EventSubscriptionOptions | None = None,
    ) -> Callable[[], None]:
        _options = EventSubscriptionOptions() if options is None else options
        event_handlers[event_type].add((handler, _options))
        return lambda: event_handlers[event_type].remove((handler, _options))

    def autorun(
        selector: Callable[[State], SelectorOutput],
        comparator: Callable[[State], ComparatorOutput] | None = None,
    ) -> Callable[
        [
            Callable[[SelectorOutput], AutorunReturnType]
            | Callable[[SelectorOutput, SelectorOutput], AutorunReturnType],
        ],
        Callable[[], AutorunReturnType],
    ]:
        nonlocal state

        def decorator(
            fn: Callable[[SelectorOutput], AutorunReturnType]
            | Callable[[SelectorOutput, SelectorOutput], AutorunReturnType],
        ) -> Callable[[], AutorunReturnType]:
            last_selector_result: SelectorOutput | None = None
            last_comparator_result: ComparatorOutput | None = None
            last_value: AutorunReturnType | None = None

            def check_and_call(state: State) -> None:
                nonlocal last_selector_result, last_comparator_result, last_value
                selector_result = selector(state)
                if comparator is None:
                    comparator_result = cast(ComparatorOutput, selector_result)
                else:
                    comparator_result = comparator(state)
                if comparator_result != last_comparator_result:
                    previous_result = last_selector_result
                    last_selector_result = selector_result
                    last_comparator_result = comparator_result
                    if len(signature(fn).parameters) == 1:
                        last_value = cast(
                            Callable[[SelectorOutput], AutorunReturnType],
                            fn,
                        )(selector_result)
                    else:
                        last_value = cast(
                            Callable[
                                [SelectorOutput, SelectorOutput | None],
                                AutorunReturnType,
                            ],
                            fn,
                        )(
                            selector_result,
                            previous_result,
                        )

            if _options.autorun_initial_run and state is not None:
                check_and_call(state)

            subscribe(check_and_call)

            def call() -> AutorunReturnType:
                if state is not None:
                    check_and_call(state)
                return cast(AutorunReturnType, last_value)

            return call

        return decorator

    dispatch(cast(Action, InitAction()))
    if _options.scheduler is not None:
        _options.scheduler(run)
        run()

    return InitializeStateReturnValue(
        dispatch=dispatch,
        subscribe=subscribe,
        subscribe_event=cast(Callable, subscribe_event),
        autorun=autorun,
    )
