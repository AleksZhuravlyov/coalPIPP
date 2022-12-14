#include <Transient.h>
#include <Steady.h>

Transient::Transient(const std::vector<double> &propsVector,
                     const std::vector<std::string> &thetaFiles,
                     const std::vector<double> &time,
                     const std::vector<double> &pressIn,
                     const std::vector<double> &pressOut,
                     const std::vector<double> &consumption) :
        Equation(propsVector, thetaFiles,
                 time, pressIn, pressOut, consumption),
        dt(1) {}


void Transient::setTheta(const std::vector<double> &theta) {
    setThetaPoro(theta);
}

void Transient::calculateInitPress() {

    std::vector<double> _propsVector(props.getPropsVector());
    std::vector<std::string> _thetaFiles(local.getThetaFiles());
    std::vector<double> _time{time[0]};
    std::vector<double> _pressIn{pressIn[0]};
    std::vector<double> _pressOut{pressOut[0]};
    std::vector<double> _consumptionFact{consumptionFact[0]};
    Steady steady(_propsVector, _thetaFiles,
                  _time, _pressIn, _pressOut, _consumptionFact);

    steady.local.loadThetaPerm();
    steady.calculateConsumptions();
    press[iCurr] = steady.getPress();

}

void Transient::calculateMatrix() {
    MatrixIterator(matrix, 0).valueRef() = local.alpha[0];
    for (int i = 1; i < dim - 1; ++i) {
        MatrixIterator it(matrix, i);
        double &betaLeft = convective.beta[Local::left(i)];
        double &betaRight = convective.beta[Local::right(i)];
        double &alpha = local.alpha[i];
        it.valueRef() = -betaLeft;
        ++it;
        it.valueRef() = alpha + betaLeft + betaRight;
        ++it;
        it.valueRef() = -betaRight;
    }
    MatrixIterator(matrix, dim - 1).valueRef() = local.alpha[dim - 1];
}


void Transient::calculateFreeVector(const double &_pressIn,
                                    const double &_pressOut) {
    freeVector[0] = local.alpha[0] * _pressIn;
    for (int i = 1; i < dim - 1; i++)
        freeVector[i] = local.alpha[i] * press[iPrev][i];
    freeVector[dim - 1] = local.alpha[dim - 1] * _pressOut;
}


void Transient::cfdProcedure(const double &_pressIn,
                             const double &_pressOut) {
    std::swap(iCurr, iPrev);
    calculateAlpha(dt);
    calculateBeta();
    calculateGuessVector();
    calculateMatrix();
    calculateFreeVector(_pressIn, _pressOut);
    calculatePress();
}

void Transient::calculateConsumptions() {
    calculateInitPress();
    std::swap(iCurr, iPrev);
    calculateBeta();
    std::swap(iCurr, iPrev);
    consumptionCalc[0] = calculateConsumption();
    for (int i = 1; i < consumptionFact.size(); i++) {
        dt = time[i] - time[i - 1];
        cfdProcedure(pressIn[i], pressOut[i]);
        consumptionCalc[i] = calculateConsumption();
    }
    calculateConsumptionRelErr();
}

double Transient::getDt() const {
    return dt;
}

void Transient::setDt(const double &_dt) {
    dt = _dt;
}
