#ifndef __CONDOR_TYPES_H__
#define __CONDOR_TYPES_H__

#include <GLFW/glfw3.h>

#define true 1
#define false 0

typedef int bool;

typedef struct CondorData {
    // Style style;
    // Stack styles;
    // NoiseParams params;

    GLFWwindow *window;

    int _looping;
    int _frame_count;
    int _frame_rate;
    int _actual_frame_rate;
    int _redraw;

    PyObject *_setup;
    PyObject *_draw;
} CondorData;

#endif // __CONDOR_TYPES_H__

