#ifndef COALPIP_STEADY_H
#define COALPIP_STEADY_H

#include <Equation.h>


class Steady : public Equation {

public:

    Steady(const std::vector<double> &propsVector,
           const std::vector<std::string> &thetaFiles,
           const std::vector<double> &time,
           const std::vector<double> &pressIn,
           const std::vector<double> &pressOut,
           const std::vector<double> &consumption);

    ~Steady() override = default;

    void calculateGuessPress(const double &pressIn,
                             const double &pressOut);

    void calculateMatrix() final;

    void calculateFreeVector(const double &_pressIn,
                             const double &_pressOut) final;


    void cfdProcedure(const double &_pressIn,
                      const double &_pressOut) final;

    void calculateConsumptions() final;

    void setTheta(const std::vector<double> &theta) final;


};


#endif //COALPIP_STEADY_H
