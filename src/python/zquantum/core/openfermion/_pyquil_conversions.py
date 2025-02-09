############################################################################
#   Copyright 2017 Rigetti Computing, Inc.
#   Modified by Zapata Computing 2020 for the performance reasons.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
############################################################################
"""
Translates OpenFermion Objects to pyQuil objects
"""
from typing import Union

from openfermion.ops import QubitOperator
from pyquil.paulis import PauliSum, PauliTerm


def qubitop_to_pyquilpauli(qubit_operator: QubitOperator) -> PauliSum:
    """
    Convert a OpenFermion QubitOperator to a PauliSum.

    Args:
        qubit_operator: OpenFermion QubitOperator to convert to a pyquil.PauliSum

    Returns:
        PauliSum representing the qubit operator
    """
    if not isinstance(qubit_operator, QubitOperator):
        raise TypeError("qubit_operator must be a OpenFermion " "QubitOperator object")

    terms = []
    for qubit_terms, coefficient in qubit_operator.terms.items():
        base_term: Union[PauliTerm, PauliSum] = PauliTerm("I", 0)
        for tensor_term in qubit_terms:
            base_term *= PauliTerm(tensor_term[1], tensor_term[0])
        terms.append(base_term * coefficient)

    paulisum = PauliSum(terms)

    return paulisum.simplify()


def pyquilpauli_to_qubitop(pyquil_pauli: Union[PauliTerm, PauliSum]) -> QubitOperator:
    """
    Convert a pyQuil PauliSum to a OpenFermion QubitOperator.

    Args:
        pyquil_pauli: pyQuil PauliTerm or PauliSum to convert to an
    OpenFermion QubitOperator

    Returns:
        QubitOperator representing the PauliSum or PauliTerm
    """

    if not isinstance(pyquil_pauli, (PauliSum, PauliTerm)):
        raise TypeError("pyquil_pauli must be a pyquil PauliSum or " "PauliTerm object")

    if isinstance(pyquil_pauli, PauliTerm):
        pyquil_pauli = PauliSum([pyquil_pauli])

    transformed_term = QubitOperator()
    # iterate through the PauliTerms of PauliSum
    for pauli_term in pyquil_pauli.terms:
        transformed_term += QubitOperator(
            term=tuple(zip(pauli_term._ops.keys(), pauli_term._ops.values())),
            coefficient=pauli_term.coefficient,
        )

    return transformed_term
