#ifndef COALPIP_TRANSIENT_H
#define COALPIP_TRANSIENT_H

#include <Equation.h>

class Transient : public Equation {

public:

    Transient(const std::vector<double> &propsVector,
              const std::vector<std::string> &thetaFiles,
              const std::vector<double> &time,
              const std::vector<double> &pressIn,
              const std::vector<double> &pressOut,
              const std::vector<double> &consumption);

    ~Transient() override = default;

    void setTheta(const std::vector<double> &theta) final;


    void calculateInitPress();

    void calculateMatrix() final;

    void calculateFreeVector(const double &_pressIn,
                             const double &_pressOut) final;

    void cfdProcedure(const double &_pressIn,
                      const double &_pressOut) final;

    void calculateConsumptions() final;


    double getDt() const;

    void setDt(const double &_dt);

private:
    double dt;

};


#endif //COALPIP_TRANSIENT_H
