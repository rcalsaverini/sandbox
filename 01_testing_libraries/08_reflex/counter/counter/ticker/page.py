import reflex as rx

from .state import TickerState


def page():
    decrement_btn = rx.button("Decrement", on_click=TickerState.decrement)
    increment_btn = rx.button("Increment", on_click=TickerState.increment)
    state_heading = rx.heading(TickerState.count, font_size="2em")
    return rx.vstack(
        rx.heading("This is the Ticker", align="center"),
        rx.hstack(decrement_btn, state_heading, increment_btn, spacing="4"),
        align_items="center",
    )
