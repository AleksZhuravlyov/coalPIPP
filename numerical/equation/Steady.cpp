#include <Steady.h>

#include <iostream>


Steady::Steady(const std::vector<double> &propsVector,
               const std::vector<std::string> &thetaFiles,
               const std::vector<double> &time,
               const std::vector<double> &pressIn,
               const std::vector<double> &pressOut,
               const std::vector<double> &consumption) :
        Equation(propsVector, thetaFiles,
                 time, pressIn, pressOut, consumption) {}


void Steady::calculateGuessPress(const double &pressIn,
                                 const double &pressOut) {
    for (int i = 0; i < dim; i++)
        press[iCurr][i] = pressIn * (dim - 1 - i) / (dim - 1) +
                          pressOut * i / (dim - 1);
}


void Steady::calculateMatrix() {

    for (int i = 1; i < matrix.outerSize() - 1; ++i) {

        MatrixIterator it(matrix, i);
        double &betaLeft = convective.beta[Local::left(i)];
        double &betaRight = convective.beta[Local::right(i)];

        it.valueRef() = -betaLeft;
        ++it;
        it.valueRef() = betaLeft + betaRight;
        ++it;
        it.valueRef() = -betaRight;

    }

}

void Steady::calculateFreeVector(const double &_pressIn,
                                 const double &_pressOut) {
    freeVector[0] = _pressIn;
    for (int i = 1; i < dim - 1; i++)
        freeVector[i] = 0;
    freeVector[dim - 1] = _pressOut;
}


void Steady::cfdProcedure(const double &_pressIn,
                          const double &_pressOut) {
    calculateGuessPress(_pressIn, _pressOut);
    calculateFreeVector(_pressIn, _pressOut);
    do {
        std::swap(iCurr, iPrev);
        calculateBeta();
        calculateGuessVector();
        calculateMatrix();
        calculatePress();
    } while (calculatePressRelDiff() > props.iterativeAccuracy);

}


void Steady::calculateConsumptions() {
    for (int i = 0; i < consumptionFact.size(); i++) {
        cfdProcedure(pressIn[i], pressOut[i]);
        consumptionCalc[i] = calculateConsumption();
    }
    calculateConsumptionRelErr();
}

void Steady::setTheta(const std::vector<double> &theta) {
    setThetaPerm(theta);
}

