#ifndef COALPIP_CONVECTIVE_H
#define COALPIP_CONVECTIVE_H

#include <Props.h>

#include <vector>


class Convective {

public:

    explicit Convective(const Props &_props);

    virtual ~Convective() = default;


    friend std::ostream &operator<<(std::ostream &stream,
                                    const Convective &convective);


    static int left(const int &index);

    static int right(const int &index);


    void calculateBeta(const std::vector<double> &lambda);


    Props props;

    std::vector<double> beta;


};


#endif //COALPIP_CONVECTIVE_H
