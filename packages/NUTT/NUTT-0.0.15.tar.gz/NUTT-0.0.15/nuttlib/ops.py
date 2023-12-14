"""Core ops"""

from typing import Union, List, Tuple
from .mat import Mat
from termcolor import colored
import logging

# these are all the operations that can be performed on Mat objects, even thought they're separate from the Mat class itself
# it's just because I want to keep things neat and tidy and sexy



def add(mat1: Mat, mat2: Mat) -> Mat: # element-wise addition
	if mat1.rows != mat2.rows or mat1.cols != mat2.cols:
		raise ValueError("Matrices must be of equal dims")
	elif not isinstance(mat1, Mat) or not isinstance(mat2, Mat):
		raise TypeError("Operand must be a Mat obj")
	else:
		newMat = [[mat1.data[i][j] + mat2.data[i][j] for j in range(mat1.cols)] for i in range(mat1.rows)] # Python makes this so easy
		return Mat(mat1.rows, mat1.cols, newMat)

def subtract(mat1: Mat, mat2: Mat) -> Mat: # elem-wise subtraction
	if mat1.rows != mat2.rows or mat1.cols != mat2.cols:
		raise ValueError("Matrices must be of equal dims")
	elif not isinstance(mat1, Mat) or not isinstance(mat2, Mat):
		raise TypeError("Operand must be a Mat obj")
	else:
		newMat = [[mat1.data[i][j] - mat2.data[i][j] for j in range(mat1.cols)] for i in range(mat1.rows)]
		return Mat(mat1.rows, mat1.cols, newMat)

def hadamard(mat1: Mat, mat2: Mat) -> Mat: # element-wise multiplication
	if mat1.rows != mat2.rows or mat1.cols != mat2.cols:
		raise ValueError("Matrices must be of equal dims")
	if not isinstance(mat1, Mat) or not isinstance(mat2, Mat):
		raise TypeError("Operand must be a Mat obj")
	else:
		newMat = [[mat1.data[i][j] * mat2.data[i][j] for j in range(mat1.cols)] for i in range(mat1.rows)]
		return Mat(mat1.rows, mat1.cols, newMat)

def scalarmul(mat: Mat, scalar: Union[int, float]) -> Mat: # scalar mul
	if not isinstance(mat, Mat) or not isinstance(scalar, (int, float)):
		raise TypeError("Operand must be a Mat obj and a scalar, respectively")
	else:
		newMat = [[mat.data[i][j] * scalar for j in range(mat.cols)] for i in range(mat.rows)]
		logging.debug(f"returning Mat({mat.rows}, {mat.cols}, {newMat} in scalarmul")
		return Mat(mat.rows, mat.cols, newMat)

def sum_mat(mat: Mat) -> Union[int, float]: # sum of all elems
	if not isinstance(mat, Mat):
		raise TypeError(f"Operand must be a Mat obj\n{type(mat)} given\ncontents: {mat}")
	else:
		return sum([sum(row) for row in mat.data])

def transpose(mat: Mat) -> Mat: # just flips the rows and cols
	newMat = [[mat.data[j][i] for j in range(len(mat.data))] for i in range(len(mat.data[0]))]
	return Mat(len(newMat), len(newMat[0]), newMat)

def minor(mat: Mat, coords: Tuple) -> Mat: # computes the minor of a Mat
	if not isinstance(mat, Mat):
		raise TypeError("Operand must be a Mat obj")
	elif not isinstance(coords, tuple):
		raise TypeError("Coords must be a tuple")
	elif len(coords) != 2:
		raise ValueError("Coords must be a tuple of length 2")
	elif not all(isinstance(coord, int) for coord in coords):
		raise TypeError("Coords must be a tuple of ints")
	elif not all(0 <= coord < mat.rows for coord in coords):
		raise IndexError("Coords out of range of Mat")
	else:
		newMat = [[mat.data[i][j] for j in range(mat.cols) if j != coords[1]] for i in range(mat.rows) if i != coords[0]] # this computes the minor of a Mat
		return Mat(mat.rows - 1, mat.cols - 1, newMat) # the minor is a Mat with one less row and one less col than the original Mat

def exponent(mat: Mat) -> Mat: # element-wise exponentiation
	if not isinstance(mat, Mat):
		raise TypeError("Operand must be a Mat obj")
	else:
		newMat = [[mat.data[i][j] ** 2 for j in range(mat.cols)] for i in range(mat.rows)]
		return Mat(mat.rows, mat.cols, newMat)

def logarithm(mat: Mat) -> Mat:
	if not isinstance(mat, Mat):
		raise TypeError("Operand must be a Mat obj")
	else:
		logs = [[ln(mat.data[i][j]) for j in range(mat.cols)] for i in range(mat.rows)] # this computes the natural log of each elem in the Mat
		return Mat(mat.rows, mat.cols, logs)

def log2() -> float:
	return 0.6931471805599453 # ln(2) - now, this may seem stupid, but since this is a constant, it's actually faster to just hardcode it than to compute it every time

def ln(x: float) -> float: # Taylor for ln(x)
	if x <= 0:
		raise ValueError("log of non-positive number is illegal")
	else:
		n = 0
		while x > 2:
			x /= 2
			n += 1

		x -= 1
		term = x
		res = term
		i = 2 # i = 1 is already accounted for

		while i < 200: # 200 is arbitrary and stands for "precision" - the amount of terms in Taylor
			term *= -x * (i - 1) / i
			res += term
			i += 1

		return res + n * log2()

def mean(mat: Mat) -> float: # computes the mean of a Mat
	if not isinstance(mat, Mat):
		raise TypeError("Operand must be a Mat obj")
	else:
		return sum([sum(row) for row in mat.data]) / (mat.rows * mat.cols) # this is the mean of a Mat

def singular_value_decomposition(mat: Mat) -> Mat:
	raise NotImplementedError

def determinant(mat: Mat) -> Union[int, float]: # computes the determinant of a Mat
	if mat.rows != mat.cols:
		raise ValueError("Mat must square be") # Yoda speak 😂
	elif mat.rows == 2:
		return mat.data[0][0] * mat.data[1][1] - mat.data[0][1] * mat.data[1][0]
	else:
		det = 0
		for i in range(mat.rows):
			det += ((-1)**i) * mat.data[0][i] * mat.minor((0, i)).det
		return det

def inverse(mat: Mat) -> Mat: # only works for 2x2 mats ('cause I'm a lazy bastard)
	if mat.rows != mat.cols:
		raise ValueError("Mat square must be") # Yoda strikes again!
	elif mat.rows != 2:
		# ! TODO: implement inverse for matrices of arbitrary size
		raise NotImplementedError # ! I'm too lazy to implement this rn lol 
	else:
		det = mat.det
		if det == 0:
			raise ValueError("Mat not invertible (det = 0). Check your Mat next time, doofus!")
		else:
			inv = 1/det
			newMat = [
				[mat.data[1][1] * inv, -mat.data[0][1] * inv],
				[-mat.data[1][0] * inv, mat.data[0][0] * inv]
			
			] # formally: 1/det * [[a, -b], [-c, d]]
			return Mat(mat.rows, mat.cols, newMat)

def matmul(mat1: Mat, mat2: Mat) -> Mat: # dot
	if mat1.cols != mat2.rows:
		raise ValueError(f"Matrices must be of compatible dims\nMat1 dims: {mat1.shape}\nMat2 dims: {mat2.shape}")
	elif not isinstance(mat1, Mat) or not isinstance(mat2, Mat):
		raise TypeError("Operand must be a Mat obj")
	else:
		logging.debug(f"Mat1 dims: {mat1.shape}\nMat2 dims: {mat2.shape}\nmat1.data: {mat1.data}\nmat2.data: {mat2.data}")
		newMat = [[sum([mat1.data[i][k] * mat2.data[k][j] for k in range(mat1.cols)]) for j in range(mat2.cols)] for i in range(mat1.rows)] # holy moly guacamole, that's a lot of Python right there
		return Mat(mat1.rows, mat2.cols, newMat)

def power(mat: Mat, power: int) -> Mat: # power
	if not isinstance(mat, Mat) or not isinstance(power, int):
		raise TypeError("Operand must be a Mat obj and an int, respectively")
	elif mat.rows != mat.cols:
		raise ValueError("Mat must be square")
	else:
		if power == 0:
			return Mat(mat.rows, mat.cols, [[1 if i == j else 0 for j in range(mat.cols)] for i in range(mat.rows)]) # ID mat
		elif power == 1:
			return mat
		else:
			return mat @ power(mat, power - 1)

def equals(mat1: Mat, mat2: Mat) -> bool: # equality
	if mat1.rows != mat2.rows or mat1.cols != mat2.cols: # if the dims are not equal, then the mats are not equal
		return False
	else:
		for i in range(mat1.rows):
			for j in range(mat1.cols):
				if mat1.data[i][j] != mat2.data[i][j]: # if any of the elems are not identical, then the mats are not equal
					return False
		return True

def eigs(mat: Mat) -> List[Union[int, float]]: # eigenvalues
	if mat.rows != mat.cols:
		raise ValueError(colored("Mat must be SqUaRe", "yellow")) # Sponge B.
	else:
		# ! TODO: implement eigenvalues for matrices of arbitrary size
		raise NotImplementedError # ! I'm too f- lazy to get this done right now ...

def eigvecs(mat: Mat) -> List[Union[int, float]]: # eigenvectors
	if mat.rows != mat.cols:
		raise ValueError(colored("Mat must be s... you know what!", "red"))
	else:
		# ! TODO: implement eigenvectors for matrices of arbitrary size
		raise NotImplementedError # I ... am ... too ... lazy ... to ... do ... this ... right ... now ...

def echelon(mat: Mat, bReduced: bool = False) -> Mat: # row echelon form by default, reduced row echelon form if bReduced is True
	if not isinstance(mat, Mat):
		raise TypeError("Operand must be a Mat obj")
	else:
		for i in range(mat.rows):
			if mat.data[i][i] == 0:
				for j in range(i + 1, mat.rows):
					if mat.data[j][i] != 0:
						mat.data[i], mat.data[j] = mat.data[j], mat.data[i]
						break
				else:
					continue

				pivot = mat.data[i][i]
				if bReduced:
						for j in range(i, mat.cols):
							mat.data[i][j] /= pivot

						for j in range(mat.rows):
							if j == i:
								continue
							factor = mat.data[j][i]
							for k in range(i, mat.cols):
								mat.data[j][k] -= factor * mat.data[i][k]
				else:
					for j in range(i + 1, mat.rows):
						factor = mat.data[j][i]
						for k in range(i, mat.cols):
							mat.data[j][k] -= factor * mat.data[i][k]

	return mat