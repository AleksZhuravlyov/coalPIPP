#include <Local.h>

#include <fstream>
#include <cmath>

Local::Local(const Props &_props,
             const std::vector<std::string> &_thetaFiles) :
        props(_props),
        thetaPermFile(_thetaFiles[0]),
        thetaPoroFile(_thetaFiles[1]),
        alpha(std::vector<double>(props.gridBlockN, 0)),
        lambda(std::vector<double>(props.gridBlockN, 0)),
        thetaFiles(_thetaFiles) {}


std::ostream &operator<<(std::ostream &stream, const Local &local) {

    stream << local.props << std::endl;
    stream << "thetaPermFile " << local.thetaPermFile << std::endl;
    stream << "thetaPoroFile " << local.thetaPoroFile;

    stream << "thetaPerm";
    for (auto &&element : local.thetaPerm)
        stream << " " << element;
    stream << std::endl;

    stream << "thetaPoro";
    for (auto &&element : local.thetaPoro)
        stream << " " << element;
    stream << std::endl;

    return stream;

}


int Local::left(const int &index) {
    return index;
}

int Local::right(const int &index) {
    return index + 1;
}


std::vector<double> Local::loadTxt(const std::string &fileName) {
    std::ifstream stream;
    stream.open(fileName.c_str());
    std::string word;
    std::vector<double> array;
    while (stream >> word)
        array.push_back(atof(word.c_str()));
    stream.close();
    return array;
}

void Local::loadThetaPerm() {
    thetaPerm = loadTxt(thetaPermFile);
}

void Local::loadThetaPoro() {
    thetaPoro = loadTxt(thetaPoroFile);
}


double Local::dens(const double &press) {
    return props.aDens * press + props.bDens;
}

double Local::densDer(const double &press) {
    return props.aDens;
}


double Local::perm(const double &press) {
    double value = 0;
    for (int i = 0; i < thetaPerm.size(); i++)
        value += thetaPerm[i] * pow(press, i);
    return value;
}

double Local::poro(const double &press) {
    double value = 0;
    for (int i = 0; i < thetaPoro.size(); i++)
        value += thetaPoro[i] * pow(press, i);
    return value;
}

double Local::poroDer(const double &press) {
    double value = 0;
    for (int i = 1; i < thetaPoro.size(); i++)
        value += thetaPoro[i] * pow(press, (i - 1)) / i;
    return value;
}

void Local::calculateAlpha(const std::vector<double> &press,
                           const double &dt) {
    for (int i = 0; i < alpha.size(); i++) {
        alpha[i] = poro(press[i]) * densDer(press[i]);
        alpha[i] += poroDer(press[i]) * dens(press[i]);
        alpha[i] *= props.deltaVolume / dt;
    }
}

void Local::calculateLambda(const std::vector<double> &press) {
    for (int i = 0; i < lambda.size(); i++)
        lambda[i] = dens(press[i]) * perm(press[i]) / props.visc;
}

std::vector<std::string> Local::getThetaFiles() const {
    return thetaFiles;
}


