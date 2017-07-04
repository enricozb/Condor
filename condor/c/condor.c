#include <Python.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "condor_types.h"
#include "glutils.h"

static CondorData condor_data = {
    .window = NULL,
    ._looping = true,
    ._frame_count = 0,
    ._frame_rate = 60,
    ._actual_frame_rate = 0,
    ._redraw = 0,
    ._setup = NULL,
    ._draw = NULL,
};


void condor_loop(void) {
    PyObject_CallObject(condor_data._draw, NULL);
    glfwSwapBuffers(condor_data.window);
}

static PyObject *
condor_begin_c(PyObject *self, PyObject *args) {
    PyObject_CallObject(condor_data._setup, NULL);
    glutils_loop(&condor_loop);
    Py_RETURN_NONE;
}

static PyObject *
condor_setup_funcs(PyObject *self, PyObject *args) {
    PyObject *funcs;
    if (!PyArg_ParseTuple(args, "O!", &PyDict_Type, &funcs)) {
        return NULL;
    }

    condor_data._setup = PyDict_GetItemString(funcs, "setup");

    if (!condor_data._setup) {
        PyErr_SetString(PyExc_RuntimeError, "setup function not found");
        return NULL;
    }

    Py_INCREF(condor_data._setup);

    condor_data._draw = PyDict_GetItemString(funcs, "draw");

    if (!condor_data._draw) {
        PyErr_SetString(PyExc_RuntimeError, "draw function not found");
        return NULL;
    }

    Py_INCREF(condor_data._draw);

    Py_RETURN_NONE;
}

static PyObject *
condor_size(PyObject *self, PyObject *args) {
    const int height;
    const int width;

    if (!PyArg_ParseTuple(args, "ii", &width, &height)) {
        return NULL;
    }

    condor_data.window = glutils_init_window(width, height);

    if (condor_data.window == NULL) {
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyMethodDef condor_methods[] = {
    {"begin_c", condor_begin_c, METH_VARARGS,
        "Specialized 'begin' function for condor.c implementation."},
    {"setup_funcs", condor_setup_funcs, METH_VARARGS,
        "Registers user-defined functions and handlers."},
    {"size", condor_size, METH_VARARGS, "Creates an OpenGL window."},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef condor_module = {
    PyModuleDef_HEAD_INIT,
    "condor",
    NULL,
    -1,
    condor_methods,
};


PyMODINIT_FUNC PyInit_condor(void) {
    glutils_init(&condor_data);
    return PyModule_Create(&condor_module);
}

