#ifndef COALPIP_EQUATION_H
#define COALPIP_EQUATION_H

#include <vector>
#include <Eigen/Sparse>

#include <Props.h>
#include <Local.h>
#include <Convective.h>


typedef Eigen::Triplet<double> Triplet;
typedef Eigen::SparseMatrix<double, Eigen::RowMajor> Matrix;
typedef Matrix::InnerIterator MatrixIterator;
typedef Eigen::VectorXd Vector;
typedef Eigen::BiCGSTAB<Eigen::SparseMatrix<double>> BiCGSTAB;


class Equation {

public:

    Equation(const std::vector<double> &propsVector,
             const std::vector<std::string> &thetaFiles,
             const std::vector<double> &_time,
             const std::vector<double> &_pressIn,
             const std::vector<double> &_pressOut,
             const std::vector<double> &_consumptionFact);

    virtual ~Equation() = default;


    friend std::ostream &operator<<(std::ostream &stream,
                                    const Equation &equation);

    void loadThetaPerm();

    void loadThetaPoro();

    void calculateAlpha(const double &dt);

    void calculateLambda();

    void calculateBeta();

    virtual void calculateMatrix() = 0;

    void calculateGuessVector();

    virtual void calculateFreeVector(const double &_pressIn,
                                     const double &_pressOut) = 0;

    virtual void cfdProcedure(const double &_pressIn,
                              const double &_pressOut) = 0;

    void calculatePress();

    double calculatePressRelDiff();

    double calculateConsumption();

    void calculateConsumptionRelErr();

    virtual void calculateConsumptions() = 0;

    virtual void setTheta(const std::vector<double> &theta) = 0;

    double calculateEmpiricalRisk(const std::vector<double> &thetaPerm);


    Props props;

    Local local;

    Convective convective;

    int &dim;

    std::vector<double> time;
    std::vector<double> pressIn;
    std::vector<double> pressOut;
    std::vector<double> consumptionFact;
    std::vector<double> consumptionCalc;
    std::vector<double> consumptionRelErr;


    std::vector<std::vector<double>> press;

    int iCurr;
    int iPrev;

    Matrix matrix;

    Vector freeVector;

    Vector guessVector;

    Vector variable;


    std::vector<double> getConsumptionRelErr() const;

    void setConsumptionRelErr(const std::vector<double> &consumptionRelErr);


    std::vector<double> getThetaPerm() const;

    void setThetaPerm(const std::vector<double> &_thetaPerm);

    std::vector<double> getThetaPoro() const;

    void setThetaPoro(const std::vector<double> &_thetaPoro);


    std::vector<double> getTime() const;

    std::vector<double> getPressIn() const;

    std::vector<double> getPressOut() const;

    std::vector<double> getConsumptionFact() const;

    std::vector<double> getConsumptionCalc() const;

    std::vector<double> getPress() const;


    void setTime(const std::vector<double> &_time);

    void setPressIn(const std::vector<double> &_pressIn);

    void setPressOut(const std::vector<double> &_pressOut);

    void setConsumptionFact(const std::vector<double> &_consumptionFact);

    void setConsumptionCalc(const std::vector<double> &_consumptionCalc);

    void setPress(const std::vector<double> &_press);

};


#endif //COALPIP_EQUATION_H
