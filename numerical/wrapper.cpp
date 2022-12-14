#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <string>

#include <Steady.h>
#include <Transient.h>

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE (cfd, m) {
    py::class_<Steady>(m, "Steady")
            .def(py::init<const std::vector<double> &,
                         const std::vector<std::string> &,
                         const std::vector<double> &,
                         const std::vector<double> &,
                         const std::vector<double> &,
                         const std::vector<double> &>(),
                 "props_array"_a,
                 "theta_files_array"_a,
                 "time"_a,
                 "press_in"_a,
                 "press_out"_a,
                 "consumption"_a)
                    // .def("__str__", __str__<Steady>)

            .def_property("theta_perm",
                          &Steady::getThetaPerm,
                          &Steady::setThetaPerm)
            .def_property("time",
                          &Steady::getTime,
                          &Steady::setTime)
            .def_property("press_in",
                          &Steady::getPressIn,
                          &Steady::setPressIn)
            .def_property("press_out",
                          &Steady::getPressOut,
                          &Steady::setPressOut)
            .def_property("consumption_fact",
                          &Steady::getConsumptionFact,
                          &Steady::setConsumptionFact)
            .def_property("consumption_calc",
                          &Steady::getConsumptionCalc,
                          &Steady::setConsumptionCalc)
            .def_property("press",
                          &Steady::getPress,
                          &Steady::setPress)
            .def_property("consumption_rel_err",
                          &Steady::getConsumptionRelErr,
                          &Steady::setConsumptionRelErr)


            .def("load_theta_perm",
                 &Steady::loadThetaPerm)

            .def("calculate_consumptions",
                 &Steady::calculateConsumptions)

            .def("calculate_empirical_risk",
                 &Steady::calculateEmpiricalRisk,
                 "theta_perm"_a);


    py::class_<Transient>(m, "Transient")
            .def(py::init<const std::vector<double> &,
                         const std::vector<std::string> &,
                         const std::vector<double> &,
                         const std::vector<double> &,
                         const std::vector<double> &,
                         const std::vector<double> &>(),
                 "props_array"_a,
                 "theta_files_array"_a,
                 "time"_a,
                 "press_in"_a,
                 "press_out"_a,
                 "consumption"_a)
                    // .def("__str__", __str__<Transient>)

            .def_property("theta_perm",
                          &Transient::getThetaPerm,
                          &Transient::setThetaPerm)
            .def_property("theta_poro",
                          &Transient::getThetaPoro,
                          &Transient::setThetaPoro)
            .def_property("time",
                          &Transient::getTime,
                          &Transient::setTime)
            .def_property("press_in",
                          &Transient::getPressIn,
                          &Transient::setPressIn)
            .def_property("press_out",
                          &Transient::getPressOut,
                          &Transient::setPressOut)
            .def_property("consumption_fact",
                          &Transient::getConsumptionFact,
                          &Transient::setConsumptionFact)
            .def_property("consumption_calc",
                          &Transient::getConsumptionCalc,
                          &Transient::setConsumptionCalc)
            .def_property("press",
                          &Transient::getPress,
                          &Transient::setPress)
            .def_property("consumption_rel_err",
                          &Steady::getConsumptionRelErr,
                          &Steady::setConsumptionRelErr)
            .def_property("dt",
                          &Transient::getDt,
                          &Transient::setDt)


            .def("load_theta_perm",
                 &Transient::loadThetaPerm)

            .def("load_theta_poro",
                 &Transient::loadThetaPoro)

            .def("calculate_consumptions",
                 &Transient::calculateConsumptions)

            .def("calculate_empirical_risk",
                 &Transient::calculateEmpiricalRisk,
                 "theta_poro"_a);

}