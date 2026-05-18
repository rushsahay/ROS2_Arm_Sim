#ifndef ARM_SIM__VISIBILITY_CONTROL_H_
#define ARM_SIM__VISIBILITY_CONTROL_H_

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ARM_SIM_EXPORT __attribute__ ((dllexport))
    #define ARM_SIM_IMPORT __attribute__ ((dllimport))
  #else
    #define ARM_SIM_EXPORT __declspec(dllexport)
    #define ARM_SIM_IMPORT __declspec(dllimport)
  #endif
  #ifdef ARM_SIM_BUILDING_LIBRARY
    #define ARM_SIM_PUBLIC ARM_SIM_EXPORT
  #else
    #define ARM_SIM_PUBLIC ARM_SIM_IMPORT
  #endif
  #define ARM_SIM_PUBLIC_TYPE ARM_SIM_PUBLIC
  #define ARM_SIM_LOCAL
#else
  #define ARM_SIM_EXPORT __attribute__ ((visibility("default")))
  #define ARM_SIM_IMPORT
  #if __GNUC__ >= 4
    #define ARM_SIM_PUBLIC __attribute__ ((visibility("default")))
    #define ARM_SIM_LOCAL  __attribute__ ((visibility("default")))
  #else
    #define ARM_SIM_PUBLIC
    #define ARM_SIM_LOCAL
  #endif
  #define ARM_SIM_PUBLIC_TYPE
#endif

#endif  // ARM_SIM__VISIBILITY_CONTROL_H_
