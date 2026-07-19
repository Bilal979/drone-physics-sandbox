from src.vectors import Vector3
import math
import pytest

def test_addition():
    # Arrange
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(4, 5, 6)

    # Act
    result = v1 + v2

    # Assert
    assert result == Vector3(5, 7, 9)


def test_subtraction():
    # Arrange
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(4, 5, 6)

    # Act
    result = v1 - v2

    # Assert
    assert result == Vector3(-3, -3, -3)

def test_multiplication():
    # Arrange
    v1 = Vector3(1, 2, 3)
    scalar = 2

    # Act
    result = v1 * scalar

    # Assert
    assert result == Vector3(2, 4, 6)


def test_division():
    # Arrange
    v1 = Vector3(1, 2, 3)
    scalar = 2

    # Act
    result = v1 / scalar

    # Assert
    assert result == Vector3(0.5, 1, 1.5)


def test_magnitude():
    # Arrange
    v1 = Vector3(1, 2, 3)

    # Act
    result = v1.magnitude()

    # Assert
    assert result == pytest.approx(math.sqrt(14))


def test_normalize_zero_vector():
    # Arrange
    v1 = Vector3(0,0,0)

    # Act
    result = v1.normalize()

    # Assert
    assert result == Vector3(0,0,0)