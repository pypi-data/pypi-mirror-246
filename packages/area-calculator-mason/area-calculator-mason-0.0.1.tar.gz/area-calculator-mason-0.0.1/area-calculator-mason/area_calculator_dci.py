"""The area calculator module"""
from math import pi


def welcome():
    """Welcomes user to the package."""
    print('Hello, welcome to area calculator package!')


def square(a):
    """Calculates the area of a square and returns the result."""
    return a * a


def rectangle(a, b):
    """Calculates the area of a rectangle and returns the result."""
    return a * b


def triangle(b, h):
    """Calculates the area of a triangle and returns the result."""
    return 0.5 * b * h


def circle(r):
    """Calculates the area of a circle and returns the result."""
    return pi * r**2
