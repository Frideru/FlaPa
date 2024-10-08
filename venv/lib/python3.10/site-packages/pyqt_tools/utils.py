from PyQt5.QtWidgets import QSizePolicy
from guiqwt.styles import style_generator


def generate_styles(num_curves):
    styles = style_generator()
    return [next(styles) for _ in range(num_curves)]


def set_size_policy(widget, v_policy, h_policy):
    policy = QSizePolicy(v_policy, h_policy)
    widget.setSizePolicy(policy)
