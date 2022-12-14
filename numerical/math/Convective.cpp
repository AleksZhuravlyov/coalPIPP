#include <Convective.h>

#include <Props.h>

Convective::Convective(const Props &_props) :
        props(_props),
        beta(std::vector<double>(props.gridBlockN + 1, 0)) {}


std::ostream &operator<<(std::ostream &stream,
                         const Convective &convective) {
    stream << convective.props;
    return stream;
}


int Convective::left(const int &index) {
    return index - 1;
}

int Convective::right(const int &index) {
    return index;
}


void Convective::calculateBeta(const std::vector<double> &lambda) {
    for (int i = 1; i < beta.size() - 1; i++) {
        beta[i] = (lambda[left(i)] + lambda[right(i)]) / 2;
        beta[i] *= props.area / props.deltaLength;
    }
}