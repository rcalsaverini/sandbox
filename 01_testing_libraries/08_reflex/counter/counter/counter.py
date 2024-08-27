"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config
import reflex as rx
from .ticker.page import page as ticker_page
from .channels.page import page as channels_page


def link_button(name, tag, href):
    return rx.link(
        rx.flex(rx.icon(tag=tag), margin_right="1rem"),
        rx.heading(name),
        display="inline-flex",
        align_items="center",
        padding="0.75rem",
        href=href,
        border="0px solid #eaeaea",
        font_weight="semibold",
        border_radius="2rem",
    )


def sidebar():
    links = [
        link_button("Home", "home", "/"),
        link_button("Ticker", "menu", "/ticker"),
        link_button("Channels", "menu", "/channels"),
    ]
    return rx.flex(
        rx.box(
            rx.center(
                rx.vstack(
                    rx.heading("Sidebar", margin_bottom="1em"),
                    *links,
                    spacing="2",
                    position="fixed",
                    height="100%",
                    left="0px",
                    top="0px",
                    z_index="5",
                    padding_x="2em",
                    padding_y="1em",
                    background_color="#FFFFEE",
                    align_items="left",
                    width="250px",
                )
            )
        )
    )


def content_area(to_render):
    return rx.center(rx.flex(rx.box(to_render)))


def page(to_render):
    return rx.fragment(
        sidebar(),
        rx.container(
            content_area(to_render),
            margin_left="250px",
            max_width="60em",
            padding="2em",
        ),
    )


def index():
    return page(rx.text("excolhsa ßßßßßßßasjhhds "))


def ticker():
    return page(ticker_page())


def channels():
    return page(channels_page())


app = rx.App()
app.add_page(index)
app.add_page(ticker, "/ticker")
app.add_page(channels, "/channels")
