#ifndef COALPIP_PROPS_H
#define COALPIP_PROPS_H

#include <vector>
#include <iostream>

class Props {

public:

    explicit Props(const std::vector<double> &_propsVector);

    virtual ~Props() {}


    friend std::ostream &operator<<(std::ostream &stream, const Props &props);

    double aDens;
    double bDens;
    double visc;
    double length;
    double area;
    int gridBlockN;
    double deltaVolume;
    double deltaLength;
    double iterativeAccuracy;

    std::vector<double> getPropsVector() const;


private:

    std::vector<double> propsVector;
public:


};


#endif //COALPIP_PROPS_H
