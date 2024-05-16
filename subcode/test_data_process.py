import numpy as np
from data_process import read_data, weighted_rand_choice, generateDravesIFS


def test_read_data():
    # Replace with the path to your test data file if necessary
    param_file = "subcode/est_data.txt"
    tcoeffs, sums, probabilities = read_data(param_file)

    # Assert the shape of the arrays
    assert tcoeffs.shape == (4, 2, 2)
    assert sums.shape == (4, 2)
    assert probabilities.shape == (4,)

    # Assert the values of the arrays
    expected_tcoeffs = np.array([
        [[0.0, 0.0], [0.0, 0.16]],
        [[0.85, 0.04], [-0.04, 0.85]],
        [[0.2, -0.26], [0.23, 0.22]],
        [[-0.15, 0.28], [0.26, 0.24]]
    ])
    expected_sums = np.array([
        [0.0, 0.0],
        [0.0, 1.6],
        [0.0, 1.6],
        [0.0, 0.44]
    ])
    expected_probabilities = np.array([0.01, 0.85, 0.07, 0.07])

    assert np.allclose(tcoeffs, expected_tcoeffs)
    assert np.allclose(sums, expected_sums)
    assert np.allclose(probabilities, expected_probabilities)


def test_weighted_rand_choice():
    prob = np.array([0.1, 0.3, 0.6])
    choices = np.zeros(3)

    for _ in range(10000):
        index = weighted_rand_choice(prob)
        choices[index] += 1

    # Assert that the choices are distributed according to the probabilities
    assert np.isclose(choices[0] / 10000, 0.1, atol=0.01)
    assert np.isclose(choices[1] / 10000, 0.3, atol=0.01)
    assert np.isclose(choices[2] / 10000, 0.6, atol=0.01)


def test_generateDravesIFS():
    coeffs = np.array([
        [[0.0, 0.0], [0.16, 0.0]],
        [[0.85, 0.04], [-0.04, 0.85]],
        [[0.2, -0.26], [0.23, 0.22]],
        [[-0.15, 0.28], [0.26, 0.24]]
    ])
    sums = np.array([
        [0.0, 0.01],
        [0.0, 1.6],
        [0.0, 1.6],
        [0.0, 0.44]
    ])
    probabilities = np.array([0.16, 0.85, 0.07, 0.07])

    x_points, y_points, c_points = generateDravesIFS(coeffs,
                                                     sums,
                                                     probabilities,
                                                     iterations=100)

    # Assert the shape of the arrays
    assert x_points.shape == (100,)
    assert y_points.shape == (100,)
    assert c_points.shape == (100,)

    # Assert that the values are within the 'expected' range
    assert np.all(x_points >= -20) and np.all(x_points <= 20)
    assert np.all(y_points >= -20) and np.all(y_points <= 20)
    assert np.all(c_points >= 0.0) and np.all(c_points <= 1.0)


# Run the tests
test_read_data()
test_weighted_rand_choice()
test_generateDravesIFS()
