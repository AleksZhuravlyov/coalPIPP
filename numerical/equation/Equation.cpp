#include <Equation.h>

Equation::Equation(const std::vector<double> &propsVector,
                   const std::vector<std::string> &thetaFiles,
                   const std::vector<double> &_time,
                   const std::vector<double> &_pressIn,
                   const std::vector<double> &_pressOut,
                   const std::vector<double> &_consumptionFact) :
        props(propsVector),
        local(props, thetaFiles),
        convective(props),
        dim(props.gridBlockN),
        time(_time),
        pressIn(_pressIn),
        pressOut(_pressOut),
        consumptionFact(_consumptionFact),
        consumptionCalc(_consumptionFact.size(), 0),
        consumptionRelErr(_consumptionFact.size(), 0),
        iCurr(0),
        iPrev(1),
        matrix(dim, dim),
        freeVector(dim),
        guessVector(dim),
        variable(dim) {


    press.emplace_back(std::vector<double>(dim, 0));
    press.emplace_back(std::vector<double>(dim, 0));

    std::vector<Triplet> triplets;
    triplets.reserve(3 * dim - 4);
    triplets.emplace_back(0, 0, 1);
    for (int i = 1; i < dim - 1; i++) {
        triplets.emplace_back(i, i - 1);
        triplets.emplace_back(i, i);
        triplets.emplace_back(i, i + 1);
    }
    triplets.emplace_back(dim - 1, dim - 1, 1);
    matrix.setFromTriplets(triplets.begin(), triplets.end());

    for (int i = 0; i < dim; i++) {
        freeVector[i] = 0;
        guessVector[i] = 0;
        variable[i] = 0;
    }

}


std::ostream &operator<<(std::ostream &stream,
                         const Equation &equation) {
    stream << equation.props;
    return stream;
}


void Equation::loadThetaPerm() {
    local.loadThetaPerm();
}

void Equation::loadThetaPoro() {
    local.loadThetaPoro();
}


void Equation::calculateAlpha(const double &dt) {
    local.calculateAlpha(press[iPrev], dt);
}

void Equation::calculateLambda() {
    local.calculateLambda(press[iPrev]);
}

void Equation::calculateBeta() {
    calculateLambda();
    convective.calculateBeta(local.lambda);
}


void Equation::calculateGuessVector() {
    for (int i = 0; i < dim; i++)
        guessVector[i] = press[iPrev][i];
}


void Equation::calculatePress() {

    BiCGSTAB biCGSTAB;

    biCGSTAB.compute(matrix);

    variable = biCGSTAB.solveWithGuess(freeVector, guessVector);

    for (int i = 0; i < dim; i++)
        press[iCurr][i] = variable[i];

}

double Equation::calculatePressRelDiff() {
    double relDiff = 0;
    for (int i = 0; i < dim; i++)
        relDiff += fabs(press[iCurr][i] - press[iPrev][i]) / press[iCurr][i] /
                   dim;
    return relDiff;
}

double Equation::calculateConsumption() {
    int i = dim - 1;
    return -convective.beta[Local::left(i)] *
           (press[iCurr][i] - press[iCurr][i - 1]);
}

void Equation::calculateConsumptionRelErr() {
    for (int i = 0; i < consumptionFact.size(); i++)
        consumptionRelErr[i] = fabs(consumptionFact[i] - consumptionCalc[i]) /
                               consumptionFact[i];
}


double Equation::calculateEmpiricalRisk(const std::vector<double> &theta) {

    setTheta(theta);
    calculateConsumptions();
    double empiricalRisk = 0;
    for (int i = 0; i < consumptionRelErr.size(); i++)
        empiricalRisk += consumptionRelErr[i] / consumptionRelErr.size();

    return empiricalRisk;

}


std::vector<double> Equation::getThetaPerm() const {
    return local.thetaPerm;
}

void Equation::setThetaPerm(const std::vector<double> &_thetaPerm) {
    local.thetaPerm = _thetaPerm;
}

std::vector<double> Equation::getThetaPoro() const {
    return local.thetaPoro;
}

void Equation::setThetaPoro(const std::vector<double> &_thetaPoro) {
    local.thetaPoro = _thetaPoro;
}


std::vector<double> Equation::getTime() const {
    return time;
}

std::vector<double> Equation::getPressIn() const {
    return pressIn;
}

std::vector<double> Equation::getPressOut() const {
    return pressOut;
}

std::vector<double> Equation::getConsumptionFact() const {
    return consumptionFact;
}

std::vector<double> Equation::getConsumptionCalc() const {
    return consumptionCalc;
}

std::vector<double> Equation::getPress() const {
    return press[iCurr];
}


void Equation::setTime(const std::vector<double> &_time) {
    time = _time;
}

void Equation::setPressIn(const std::vector<double> &_pressIn) {
    pressIn = _pressIn;
}

void Equation::setPressOut(const std::vector<double> &_pressOut) {
    pressOut = _pressOut;
}

void Equation::setConsumptionFact(const std::vector<double> &_consumptionFact) {
    consumptionFact = _consumptionFact;
}

void Equation::setConsumptionCalc(const std::vector<double> &_consumptionCalc) {
    consumptionCalc = _consumptionCalc;
}

void Equation::setPress(const std::vector<double> &_press) {
    press[iCurr] = _press;
}

std::vector<double> Equation::getConsumptionRelErr() const {
    return consumptionRelErr;
}

void Equation::setConsumptionRelErr(const std::vector<double> &_consumptionRelErr) {
    consumptionRelErr = _consumptionRelErr;
}
