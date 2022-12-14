#ifndef COALPIP_LOCAL_H
#define COALPIP_LOCAL_H

#include <Props.h>

#include <string>


class Local {

public:

    explicit Local(const Props &_props,
                   const std::vector<std::string> &_thetaFiles);

    virtual ~Local() = default;


    friend std::ostream &operator<<(std::ostream &stream, const Local &local);


    static int left(const int &index);

    static int right(const int &index);


    std::vector<double> loadTxt(const std::string &fileName);

    void loadThetaPerm();

    void loadThetaPoro();


    double dens(const double &press);

    double densDer(const double &press);


    double perm(const double &press);

    double poro(const double &press);

    double poroDer(const double &press);

    void calculateAlpha(const std::vector<double> &press,
                        const double &dt);

    void calculateLambda(const std::vector<double> &press);


    Props props;

    std::string thetaPermFile;
    std::string thetaPoroFile;

    std::vector<double> thetaPerm;
    std::vector<double> thetaPoro;

    std::vector<double> alpha;
    std::vector<double> lambda;


    std::vector<std::string> getThetaFiles() const;


private:

    std::vector<std::string> thetaFiles;


};


#endif //COALPIP_LOCAL_H
