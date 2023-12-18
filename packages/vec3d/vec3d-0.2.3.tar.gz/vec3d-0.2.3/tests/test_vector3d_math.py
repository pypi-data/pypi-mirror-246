"""Testing vector3d_math functions"""
import unittest
from collections import namedtuple

from vec3d.math import add, dot, linear_combination, subtract


class TestVector3DMath(unittest.TestCase):
    """Tests the vector3d_math package functions"""

    def test_add_happy_path(self):
        SubTest = namedtuple("Subtest", ["vectors", "expected"])

        subtests = {
            "2 2D vectors": SubTest(vectors=[(1, 2), (3, 4)], expected=(4, 6)),
            "2 3D vectors": SubTest(
                vectors=[(1, 2, 3), (4, 5, 6)], expected=(5, 7, 9)
            ),
            "2 4D vectors": SubTest(
                vectors=[(1, 2, 3, 4), (5, 6, 7, 8)], expected=(6, 8, 10, 12)
            ),
            "2 10D vectors": SubTest(
                vectors=[
                    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                    (11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
                ],
                expected=(12, 14, 16, 18, 20, 22, 24, 26, 28, 30),
            ),
            "3 2D vectors": SubTest(
                vectors=[(1, 2), (3, 4), (5, 6)], expected=(9, 12)
            ),
            "5 3D vectors": SubTest(
                vectors=[
                    (1, 2, 3),
                    (4, 5, 6),
                    (7, 8, 9),
                    (10, 11, 12),
                    (13, 14, 15),
                ],
                expected=(35, 40, 45),
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            got = add(*subtest_data.vectors)
            self.assertEqual(
                got,
                subtest_data.expected,
                (
                    f"{subtest_name}: "
                    f"expected {subtest_data.expected} but got {got}"
                ),
            )

    def test_add_unhappy_path(self):
        SubTest = namedtuple("Subtest", ["vectors", "expected_ex"])

        subtests = {
            "No args provided": SubTest(vectors=None, expected_ex=TypeError),
            "Single vector": SubTest(vectors=[(1, 2)], expected_ex=ValueError),
            "2 vectors, first vector longer": SubTest(
                vectors=[(1, 2, 3), (4, 5)], expected_ex=TypeError
            ),
            "2 vectors, second vector longer": SubTest(
                vectors=[(1, 2, 3), (4, 5, 6, 7)], expected_ex=TypeError
            ),
            "3 vectors, first is longer": SubTest(
                vectors=[(1, 2, 3), (3, 4), (5, 6)], expected_ex=TypeError
            ),
            "3 vectors, last is longer": SubTest(
                vectors=[(1, 2), (3, 4), (5, 6, 7)], expected_ex=TypeError
            ),
            "3 vectors, mid is longer": SubTest(
                vectors=[(1, 2), (3, 4, 5), (5, 6)], expected_ex=TypeError
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            with self.assertRaises(
                subtest_data.expected_ex, msg=f"Subtest '{subtest_name}' failed"
            ):
                add(*subtest_data.vectors)

    def test_subtract_happy_path(self):
        SubTest = namedtuple("Subtest", ["vectors", "expected"])

        subtests = {
            "2 2D vectors": SubTest(
                vectors=[(1, 2), (3, 4)], expected=(-2, -2)
            ),
            "2 3D vectors": SubTest(
                vectors=[(1, 2, 3), (4, 5, 6)], expected=(-3, -3, -3)
            ),
            "2 4D vectors": SubTest(
                vectors=[(1, 2, 3, 4), (5, 6, 7, 8)], expected=(-4, -4, -4, -4)
            ),
            "2 10D vectors": SubTest(
                vectors=[
                    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                    (11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
                ],
                expected=(-10, -10, -10, -10, -10, -10, -10, -10, -10, -10),
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            got = subtract(subtest_data.vectors[0], subtest_data.vectors[1])
            self.assertEqual(
                got,
                subtest_data.expected,
                (
                    f"{subtest_name}: "
                    f"expected {subtest_data.expected} but got {got}"
                ),
            )

    def test_subtract_unhappy_path(self):
        SubTest = namedtuple("Subtest", ["u", "v", "expected_ex"])

        subtests = {
            "No args provided": SubTest(u=None, v=None, expected_ex=TypeError),
            "First is None": SubTest(u=None, v=(4, 5), expected_ex=TypeError),
            "Second is None": SubTest(u=(4, 5), v=None, expected_ex=TypeError),
            "First vector longer": SubTest(
                u=(1, 2, 3), v=(4, 5), expected_ex=TypeError
            ),
            "Second vector longer": SubTest(
                u=(1, 2, 3), v=(4, 5, 6, 7), expected_ex=TypeError
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            with self.assertRaises(
                subtest_data.expected_ex, msg=f"Subtest '{subtest_name}' failed"
            ):
                subtract(subtest_data.u, subtest_data.v)

    def test_dot_happy_path(self):
        SubTest = namedtuple("Subtest", ["u", "v", "expected"])

        subtests = {
            "2D vectors": SubTest(u=(1, 2), v=(3, 4), expected=11),
            "3D vectors": SubTest(u=(1, 2, 3), v=(4, 5, 6), expected=32),
            "4D vectors": SubTest(u=(1, 2, 3, 4), v=(5, 6, 7, 8), expected=70),
            "10D vectors": SubTest(
                u=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                v=(11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
                expected=935,
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            got = dot(subtest_data.u, subtest_data.v)
            self.assertEqual(
                got,
                subtest_data.expected,
                (
                    f"{subtest_name}: "
                    f"expected {subtest_data.expected} but got {got}"
                ),
            )

    def test_dot_unhappy_path(self):
        SubTest = namedtuple("Subtest", ["u", "v", "expected_ex"])

        subtests = {
            "No args provided": SubTest(u=None, v=None, expected_ex=TypeError),
            "First is None": SubTest(u=None, v=(4, 5), expected_ex=TypeError),
            "Second is None": SubTest(u=(4, 5), v=None, expected_ex=TypeError),
            "First vector longer": SubTest(
                u=(1, 2, 3), v=(4, 5), expected_ex=TypeError
            ),
            "Second vector longer": SubTest(
                u=(1, 2, 3), v=(4, 5, 6, 7), expected_ex=TypeError
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            with self.assertRaises(
                subtest_data.expected_ex, msg=f"Subtest '{subtest_name}' failed"
            ):
                dot(subtest_data.u, subtest_data.v)

    def test_linear_combination_happy_path(self):
        SubTest = namedtuple("Subtest", ["scalars", "vectors", "expected"])

        subtests = {
            "2 scalars and two 2D vectors": SubTest(
                scalars=[2, 3],
                vectors=[(1, 2), (3, 4)],
                expected=(11, 16),
            ),
            "3 scalars and three 3D vectors": SubTest(
                scalars=[1, 2, 3],
                vectors=[(1, 2, 3), (4, 5, 6), (7, 8, 9)],
                expected=(30, 36, 42),
            ),
            "2 scalars and 2 10D vectors": SubTest(
                scalars=[2, 3],
                vectors=[
                    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                    (11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
                ],
                expected=(35, 40, 45, 50, 55, 60, 65, 70, 75, 80),
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            got = linear_combination(
                subtest_data.scalars, *subtest_data.vectors
            )
            self.assertEqual(
                got,
                subtest_data.expected,
                (
                    f"{subtest_name}: "
                    f"expected {subtest_data.expected} but got {got}"
                ),
            )

    def test_linear_combination_unhappy_path(self):
        SubTest = namedtuple("Subtest", ["scalars", "vectors", "expected_ex"])

        subtests = {
            "No args provided": SubTest(
                scalars=None, vectors=None, expected_ex=TypeError
            ),
            "Empty args": SubTest(
                scalars=None, vectors=None, expected_ex=TypeError
            ),
            "Empty scalar, one vector": SubTest(
                scalars=[], vectors=[(1, 2)], expected_ex=ValueError
            ),
            "No scalar, one vector": SubTest(
                scalars=None, vectors=[(1, 2)], expected_ex=TypeError
            ),
            "One scalar, no vector": SubTest(
                scalars=[1], vectors=None, expected_ex=TypeError
            ),
            "One scalar, empty vectors": SubTest(
                scalars=[1], vectors=[], expected_ex=ValueError
            ),
            "One scalar, one vector": SubTest(
                scalars=[1], vectors=[(1, 2)], expected_ex=ValueError
            ),
            "One scalar, two vectors": SubTest(
                scalars=[1], vectors=[(1, 2), (3, 4)], expected_ex=ValueError
            ),
            "Two scalars, one vector": SubTest(
                scalars=[1, 2], vectors=[(1, 2)], expected_ex=ValueError
            ),
            "2 scalars, 2 vectors, first vector longer": SubTest(
                scalars=[1, 2],
                vectors=[(1, 2, 3), (4, 5)],
                expected_ex=TypeError,
            ),
            "2 scalars, 2 vectors, second vector longer": SubTest(
                scalars=[1, 2],
                vectors=[(1, 2, 3), (4, 5, 6, 7)],
                expected_ex=TypeError,
            ),
            "3 scalars, 3 vectors, first is longer": SubTest(
                scalars=[1, 2, 3],
                vectors=[(1, 2, 3), (3, 4), (5, 6)],
                expected_ex=TypeError,
            ),
            "3 scalars, 3 vectors, last is longer": SubTest(
                scalars=[1, 2, 3],
                vectors=[(1, 2), (3, 4), (5, 6, 7)],
                expected_ex=TypeError,
            ),
            "3 scalars, 3 vectors, mid is longer": SubTest(
                scalars=[1, 2, 3],
                vectors=[(1, 2), (3, 4, 5), (5, 6)],
                expected_ex=TypeError,
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            with self.assertRaises(
                subtest_data.expected_ex, msg=f"Subtest '{subtest_name}' failed"
            ):
                linear_combination(subtest_data.scalars, *subtest_data.vectors)


if __name__ == "__main__":
    unittest.main()
