#include <Props.h>

#include <vector>


Props::Props(const std::vector<double> &_propsVector) :
        aDens(_propsVector[0]),
        bDens(_propsVector[1]),
        visc(_propsVector[2]),
        length(_propsVector[3]),
        area(_propsVector[4]),
        gridBlockN(_propsVector[5]),
        deltaVolume(_propsVector[6]),
        deltaLength(_propsVector[7]),
        iterativeAccuracy(_propsVector[8]),
        propsVector(_propsVector) {}


std::ostream &operator<<(std::ostream &stream, const Props &props) {
    stream << "aDens " << props.aDens << std::endl;
    stream << "bDens " << props.bDens << std::endl;
    stream << "visc " << props.visc << std::endl;
    stream << "length " << props.length << std::endl;
    stream << "area " << props.area << std::endl;
    stream << "gridBlockN " << props.gridBlockN << std::endl;
    stream << "deltaVolume " << props.deltaVolume << std::endl;
    stream << "deltaLength " << props.deltaLength << std::endl;
    stream << "iterativeAccuracy " << props.iterativeAccuracy;
    return stream;
}

std::vector<double> Props::getPropsVector() const {
    return propsVector;
}
