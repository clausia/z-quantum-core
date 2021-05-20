"""Definition of predefined gate matrices and related utility functions."""
import numpy as np
import sympy

# --- non-parametric gates ---


def x_matrix():
    return sympy.Matrix([[0, 1], [1, 0]])


def y_matrix():
    return sympy.Matrix([[0, -1j], [1j, 0]])


def z_matrix():
    return sympy.Matrix([[1, 0], [0, -1]])


def h_matrix():
    return sympy.Matrix(
        [
            [(1 / np.sqrt(2)), (1 / np.sqrt(2))],
            [(1 / np.sqrt(2)), (-1 / np.sqrt(2))],
        ]
    )


def i_matrix():
    return sympy.Matrix([[1, 0], [0, 1]])


def s_matrix():
    return sympy.Matrix(
        [
            [1, 0],
            [0, 1j],
        ]
    )


def t_matrix():
    return sympy.Matrix(
        [
            [1, 0],
            [0, sympy.exp(1j * np.pi / 4)],
        ]
    )


# --- gates with a single param ---


def rx_matrix(angle):
    return sympy.Matrix(
        [
            [sympy.cos(angle / 2), -1j * sympy.sin(angle / 2)],
            [-1j * sympy.sin(angle / 2), sympy.cos(angle / 2)],
        ]
    )


def ry_matrix(angle):
    return sympy.Matrix(
        [
            [
                sympy.cos(angle / 2),
                -1 * sympy.sin(angle / 2),
            ],
            [
                sympy.sin(angle / 2),
                sympy.cos(angle / 2),
            ],
        ]
    )


def rz_matrix(angle):
    return sympy.Matrix(
        [
            [
                sympy.exp(-1 * sympy.I * angle / 2),
                0,
            ],
            [
                0,
                sympy.exp(sympy.I * angle / 2),
            ],
        ]
    )


def rh_matrix(angle):
    phase_factor = sympy.cos(angle / 2) + 1j * sympy.sin(angle / 2)
    return phase_factor * sympy.Matrix(
        [
            [
                sympy.cos(angle / 2) - 1j / sympy.sqrt(2) * sympy.sin(angle / 2),
                -1j / sympy.sqrt(2) * sympy.sin(angle / 2),
            ],
            [
                -1j / sympy.sqrt(2) * sympy.sin(angle / 2),
                sympy.cos(angle / 2) + 1j / sympy.sqrt(2) * sympy.sin(angle / 2),
            ],
        ]
    )


def phase_matrix(angle):
    return sympy.Matrix(
        [
            [1, 0],
            [0, sympy.exp(1j * angle)],
        ]
    )


def u3_matrix(theta, phi, lambda_):
    """Based on
    https://github.com/quantumlib/Cirq/blob/292080453e22e91dc5658a0cfa5043539944a950/cirq/circuits/qasm_output.py#L70
    """
    return (
        rz_matrix(phi % (2 * sympy.pi))
        * ry_matrix(theta % (2 * sympy.pi))
        * rz_matrix(lambda_ % (2 * sympy.pi))
    )


# --- non-parametric two qubit gates ---


def cnot_matrix():
    return sympy.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
    )


def cz_matrix():
    return sympy.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, -1],
        ]
    )


def swap_matrix():
    return sympy.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])


def iswap_matrix():
    return sympy.Matrix([[1, 0, 0, 0], [0, 0, 1j, 0], [0, 1j, 0, 0], [0, 0, 0, 1]])


# --- parametric two qubit gates ---


def cphase_matrix(angle):
    return sympy.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, sympy.exp(1j * angle)],
        ]
    )


def xx_matrix(angle):
    return sympy.Matrix(
        [
            [sympy.cos(angle / 2), 0, 0, -1j * sympy.sin(angle / 2)],
            [0, sympy.cos(angle / 2), -1j * sympy.sin(angle / 2), 0],
            [0, -1j * sympy.sin(angle / 2), sympy.cos(angle / 2), 0],
            [-1j * sympy.sin(angle / 2), 0, 0, sympy.cos(angle / 2)],
        ]
    )


def yy_matrix(angle):
    return sympy.Matrix(
        [
            [sympy.cos(angle / 2), 0, 0, 1j * sympy.sin(angle / 2)],
            [0, sympy.cos(angle / 2), -1j * sympy.sin(angle / 2), 0],
            [0, -1j * sympy.sin(angle / 2), sympy.cos(angle / 2), 0],
            [1j * sympy.sin(angle / 2), 0, 0, sympy.cos(angle / 2)],
        ]
    )


def zz_matrix(angle):
    arg = angle / 2
    return sympy.Matrix(
        [
            [sympy.cos(arg) - 1j * sympy.sin(arg), 0, 0, 0],
            [0, sympy.cos(arg) + 1j * sympy.sin(arg), 0, 0],
            [0, 0, sympy.cos(arg) + 1j * sympy.sin(arg), 0],
            [0, 0, 0, sympy.cos(arg) - 1j * sympy.sin(arg)],
        ]
    )


def xy_matrix(angle):
    return sympy.Matrix(
        [
            [1, 0, 0, 0],
            [0, sympy.cos(angle / 2), 1j * sympy.sin(angle / 2), 0],
            [0, 1j * sympy.sin(angle / 2), sympy.cos(angle / 2), 0],
            [0, 0, 0, 1],
        ]
    )

def iz_matrix(angle):
    return sympy.Matrix(
        [
            [sympy.exp(-1 * sympy.I * angle / 2), 0, 0, 0],
            [0, sympy.exp(sympy.I * angle / 2), 0, 0],
            [0, 0, sympy.exp(-1 * sympy.I * angle / 2), 0],
            [0, 0, 0, sympy.exp(sympy.I * angle / 2)],
        ]
    )

def hz_matrix(angle):
    return cnot_matrix() @ iz_matrix(angle) @ cnot_matrix()